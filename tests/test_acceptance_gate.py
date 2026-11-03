import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/project-delivery/scripts/acceptance_gate.py"


class AcceptanceGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="acceptance-gate-")
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "src/input.txt").write_text("one\n", encoding="utf-8")
        (self.root / "TASKS.md").write_text(
            "# Work\n\nHistorical accepted row\n\n<!-- delivery:PD-1 --> In progress\n\nLater row\n",
            encoding="utf-8",
        )
        self.counter = "from pathlib import Path; p=Path('count.txt'); n=int(p.read_text()) if p.exists() else 0; p.write_text(str(n+1))"
        self.config = {
            "version": 1,
            "checks": {
                "unit": {
                    "command": [sys.executable, "-c", self.counter],
                    "inputs": ["src/input.txt"],
                    "kind": "command",
                }
            },
            "tasks": {
                "PD-1": {
                    "checks": ["unit"],
                    "completion": {
                        "path": "TASKS.md",
                        "pending": "<!-- delivery:PD-1 --> In progress",
                        "done": "<!-- delivery:PD-1 --> Accepted",
                    },
                }
            },
        }
        self.save_config()

    def tearDown(self):
        self.temp.cleanup()

    def save_config(self):
        path = self.root / ".delivery/gate.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def invoke(self, command, *args, env=None):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), command, "--root", str(self.root), *args],
            cwd=self.root,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
        )
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"CLI did not return JSON: rc={completed.returncode}, stdout={completed.stdout!r}, stderr={completed.stderr!r}")
        return completed, result

    def latest_check(self, check_id="unit"):
        return self.root / ".delivery/evidence/checks" / check_id / "latest.json"

    def receipt_paths(self):
        evidence = self.root / ".delivery/evidence"
        if not evidence.exists():
            return []
        return sorted(path.relative_to(evidence).as_posix() for path in evidence.rglob("receipt.json"))

    def test_plan_does_not_execute_and_run_reuses_exact_pass(self):
        plan, result = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(plan.returncode, 0)
        self.assertEqual(result["checks"][0]["decision"], "missing")
        self.assertFalse((self.root / "count.txt").exists())
        check, check_result = self.invoke("check", "--task", "PD-1")
        self.assertEqual(check.returncode, 1)
        self.assertEqual(check_result["checks"][0]["decision"], "missing")
        self.assertFalse((self.root / "count.txt").exists())

        first, first_result = self.invoke("run", "--task", "PD-1")
        second, second_result = self.invoke("run", "--task", "PD-1")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(second.returncode, 0)
        self.assertEqual(first_result["checks"][0]["decision"], "ran")
        self.assertEqual(second_result["checks"][0]["decision"], "reused")
        self.assertEqual((self.root / "count.txt").read_text(), "1")
        self.assertEqual(json.loads(self.latest_check().read_text())["status"], "passed")

    def test_new_changed_and_deleted_files_in_glob_scope_stale_evidence(self):
        self.config["checks"]["unit"]["inputs"] = ["src/*.txt"]
        (self.root / "src/keep.txt").write_text("keep\n", encoding="utf-8")
        (self.root / "src/remove.txt").write_text("remove\n", encoding="utf-8")
        self.save_config()
        self.assertEqual(self.invoke("run", "--task", "PD-1")[0].returncode, 0)

        (self.root / "src/new.txt").write_text("new\n", encoding="utf-8")
        result, payload = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["checks"][0]["decision"], "stale")

        (self.root / "src/keep.txt").write_text("changed\n", encoding="utf-8")
        self.assertEqual(self.invoke("plan", "--task", "PD-1")[1]["checks"][0]["decision"], "stale")

        (self.root / "src/remove.txt").unlink()
        self.assertEqual(self.invoke("plan", "--task", "PD-1")[1]["checks"][0]["decision"], "stale")

    def test_changed_command_probe_environment_and_expiration_invalidate(self):
        self.assertEqual(self.invoke("run", "--task", "PD-1")[0].returncode, 0)
        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", "pass"]
        self.save_config()
        self.assertEqual(self.invoke("plan", "--task", "PD-1")[1]["checks"][0]["decision"], "stale")

        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", self.counter]
        self.config["checks"]["unit"]["probes"] = {"version": [sys.executable, "-c", "print('v1')"]}
        self.save_config()
        self.assertEqual(self.invoke("run", "--task", "PD-1")[0].returncode, 0)
        self.config["checks"]["unit"]["probes"]["version"] = [sys.executable, "-c", "print('v2')"]
        self.save_config()
        self.assertEqual(self.invoke("plan", "--task", "PD-1")[1]["checks"][0]["decision"], "stale")

        self.config["checks"]["unit"].pop("probes")
        self.config["checks"]["unit"]["env_keys"] = ["GATE_TEST_SECRET"]
        self.save_config()
        env_a = dict(os.environ, GATE_TEST_SECRET="alpha-secret")
        self.assertEqual(self.invoke("run", "--task", "PD-1", env=env_a)[0].returncode, 0)
        env_b = dict(os.environ, GATE_TEST_SECRET="beta-secret")
        current, output = self.invoke("plan", "--task", "PD-1", env=env_b)
        self.assertEqual(current.returncode, 0)
        self.assertEqual(output["checks"][0]["decision"], "stale")
        self.assertNotIn("alpha-secret", current.stdout)
        self.assertNotIn("beta-secret", current.stdout)

        self.config["checks"]["unit"]["max_age_seconds"] = 1
        self.save_config()
        self.assertEqual(self.invoke("run", "--task", "PD-1", env=env_a)[0].returncode, 0)
        latest = self.latest_check()
        pointer = json.loads(latest.read_text())
        receipt_path = latest.parent / "runs" / pointer["run_id"] / "receipt.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["finished_at"] = "2000-01-01T00:00:00+00:00"
        receipt_bytes = (json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()
        receipt_path.write_bytes(receipt_bytes)
        pointer["receipt_sha256"] = __import__("hashlib").sha256(receipt_bytes).hexdigest()
        latest.write_text(json.dumps(pointer), encoding="utf-8")
        expired, expired_result = self.invoke("plan", "--task", "PD-1", env=env_a)
        self.assertEqual(expired.returncode, 0)
        self.assertEqual(expired_result["checks"][0]["decision"], "stale")

    def _make_ui_config(self, command):
        self.config["checks"]["ui"] = {
            "command": command,
            "inputs": ["src/input.txt"],
            "kind": "ui",
            "required_cases": ["cart-empty", "cart-ready"],
        }
        self.config["tasks"]["PD-1"]["checks"] = ["ui"]
        self.save_config()

    def test_exit_zero_missing_case_report_or_nonpass_ui_case_cannot_complete(self):
        commands = [
            [sys.executable, "-c", "pass"],
            [sys.executable, "-c", "import json,os; open(os.environ['DELIVERY_REPORT_PATH'],'w').write(json.dumps({'cases':[{'id':'cart-empty','status':'passed'}]}))"],
            [sys.executable, "-c", "import json,os; open(os.environ['DELIVERY_REPORT_PATH'],'w').write(json.dumps({'cases':[{'id':'cart-empty','status':'passed'},{'id':'cart-ready','status':'unverified','details':'not rendered'}]}))"],
        ]
        for command in commands:
            with self.subTest(command=command[-1]):
                self._make_ui_config(command)
                completed, payload = self.invoke("complete", "--task", "PD-1")
                self.assertEqual(completed.returncode, 1)
                self.assertFalse(payload["ok"])
                self.assertIn("In progress", (self.root / "TASKS.md").read_text())
                self.assertNotIn("Accepted", (self.root / "TASKS.md").read_text())

    def test_ui_details_and_validated_existing_provenance_are_preserved(self):
        report = {
            "cases": [
                {"id": "cart-empty", "status": "passed", "details": {"evidence": "empty-state.png"}},
                {"id": "cart-ready", "status": "passed", "details": {"evidence": "ready-state.png"}},
            ],
            "provenance": "validated-existing",
        }
        script = f"import json,os; open(os.environ['DELIVERY_REPORT_PATH'],'w').write(json.dumps({report!r}))"
        self._make_ui_config([sys.executable, "-c", script])
        completed, payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(completed.returncode, 0, completed.stdout)
        latest = json.loads((self.root / ".delivery/evidence/checks/ui/latest.json").read_text())
        receipt_path = self.root / ".delivery/evidence/checks/ui/runs" / latest["run_id"] / "receipt.json"
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(receipt["provenance"], "validated-existing")
        self.assertEqual(receipt["cases"][0]["details"]["evidence"], "empty-state.png")
        self.assertTrue(payload["ledger_updated"])
        self.assertEqual(self.invoke("audit")[0].returncode, 0)

    def test_timeout_and_input_mutation_during_run_block_completion(self):
        self.config["checks"]["unit"]["timeout_seconds"] = 1
        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", "import time; time.sleep(4)"]
        self.save_config()
        timeout, _ = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(timeout.returncode, 1)
        self.assertIn("In progress", (self.root / "TASKS.md").read_text())

        self.config["checks"]["unit"]["timeout_seconds"] = 30
        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", "from pathlib import Path; Path('src/input.txt').write_text('mutated')"]
        self.save_config()
        changed, payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(changed.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertIn("In progress", (self.root / "TASKS.md").read_text())

    def test_manual_done_without_completion_proof_fails_audit(self):
        ledger = self.root / "TASKS.md"
        ledger.write_text(ledger.read_text().replace("<!-- delivery:PD-1 --> In progress", "<!-- delivery:PD-1 --> Accepted"), encoding="utf-8")
        original_ledger = ledger.read_bytes()
        receipts_before = self.receipt_paths()
        completed, completion_payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(completed.returncode, 1)
        self.assertFalse(completion_payload["ok"])
        self.assertFalse((self.root / "count.txt").exists())
        self.assertEqual(ledger.read_bytes(), original_ledger)
        self.assertEqual(self.receipt_paths(), receipts_before)

        completed, payload = self.invoke("audit")
        self.assertEqual(completed.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertIn("no valid completion proof", payload["tasks"][0]["reason"])

    def test_complete_preserves_ledger_and_historical_audit_survives_later_source_change(self):
        original = (self.root / "TASKS.md").read_bytes()
        completed, payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertTrue(payload["ledger_updated"])
        ledger = (self.root / "TASKS.md").read_bytes()
        self.assertIn(b"Historical accepted row", ledger)
        self.assertIn(b"Later row", ledger)
        self.assertEqual(ledger, original.replace(b"<!-- delivery:PD-1 --> In progress", b"<!-- delivery:PD-1 --> Accepted"))
        self.assertEqual((self.root / "count.txt").read_text(), "1")
        receipts_at_completion = self.receipt_paths()
        latest_completion_path = self.root / ".delivery/evidence/tasks/PD-1/latest.json"
        completion_pointer_at_completion = latest_completion_path.read_bytes()

        audit, audit_payload = self.invoke("audit")
        self.assertEqual(audit.returncode, 0, audit.stdout)
        self.assertTrue(audit_payload["ok"])
        (self.root / "src/input.txt").write_text("unrelated later change\n", encoding="utf-8")
        repeated, repeated_payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(repeated.returncode, 0, repeated.stdout)
        self.assertEqual(repeated_payload["acceptance"], "historical")
        self.assertEqual(repeated_payload["current_readiness"], "not_evaluated")
        self.assertEqual(repeated_payload["checks"], [])
        self.assertFalse(repeated_payload["ledger_updated"])
        self.assertEqual((self.root / "count.txt").read_text(), "1")
        self.assertEqual(self.receipt_paths(), receipts_at_completion)
        self.assertEqual(latest_completion_path.read_bytes(), completion_pointer_at_completion)
        self.assertEqual((self.root / "TASKS.md").read_bytes(), ledger)

        historical, historical_payload = self.invoke("audit")
        self.assertEqual(historical.returncode, 0, historical.stdout)
        self.assertTrue(historical_payload["ok"])
        current, current_payload = self.invoke("check", "--task", "PD-1")
        self.assertEqual(current.returncode, 1)
        self.assertEqual(current_payload["checks"][0]["decision"], "stale")

        reopened_ledger = (self.root / "TASKS.md").read_text().replace(
            "<!-- delivery:PD-1 --> Accepted",
            "<!-- delivery:PD-1 --> In progress",
        )
        (self.root / "TASKS.md").write_text(reopened_ledger, encoding="utf-8")
        reopened, reopened_payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(reopened.returncode, 0, reopened.stdout)
        self.assertEqual(reopened_payload["state_before"], "pending")
        self.assertTrue(reopened_payload["ledger_updated"])
        self.assertEqual((self.root / "count.txt").read_text(), "2")
        self.assertTrue(set(receipts_at_completion).issubset(set(self.receipt_paths())))
        self.assertEqual(len(self.receipt_paths()), len(receipts_at_completion) + 2)
        self.assertEqual(self.invoke("audit")[0].returncode, 0)

    def test_concurrent_done_edit_cannot_leave_a_valid_completion_proof(self):
        tamper = "from pathlib import Path; p=Path('TASKS.md'); p.write_text(p.read_text().replace('In progress','Accepted'))"
        # First attempt, then a reopened task with a genuine older proof.
        for previously_completed in (False, True):
            with self.subTest(previously_completed=previously_completed):
                ledger = self.root / "TASKS.md"
                ledger.write_text(ledger.read_text().replace("Accepted", "In progress"))
                self.config["checks"]["unit"]["command"] = [sys.executable, "-c", self.counter]
                self.save_config()
                if previously_completed:
                    self.assertEqual(self.invoke("complete", "--task", "PD-1")[0].returncode, 0)
                    ledger.write_text(ledger.read_text().replace("Accepted", "In progress"))
                self.config["checks"]["unit"]["command"] = [sys.executable, "-c", tamper]
                self.save_config()
                failed, payload = self.invoke("complete", "--task", "PD-1")
                self.assertEqual(failed.returncode, 1, failed.stdout)
                self.assertIn("ledger changed during completion", payload["error"])
                self.assertEqual(self.invoke("audit")[0].returncode, 1)
                pointer = self.root / ".delivery/evidence/tasks/PD-1/latest.json"
                self.assertEqual(json.loads(pointer.read_text())["status"], "in-progress")
                self.assertEqual(self.invoke("complete", "--task", "PD-1")[0].returncode, 1)

    def test_failed_final_pointer_write_leaves_audit_closed(self):
        driver = (
            "import importlib.util,sys;"
            f"spec=importlib.util.spec_from_file_location('gate_under_test',{str(SCRIPT)!r});"
            "module=importlib.util.module_from_spec(spec);"
            "sys.modules[spec.name]=module;spec.loader.exec_module(module);"
            "original=module._atomic_replace;"
            "exec(\"def fail_final(root, rel, data):\\n "
            "if '/tasks/' in rel and module.json.loads(data).get('status') == 'passed': raise OSError('injected')\\n "
            "return original(root, rel, data)\");"
            "module._atomic_replace=fail_final;sys.exit(module.main(sys.argv[1:]))"
        )
        failed = subprocess.run(
            [sys.executable, "-c", driver, "complete", "--root", str(self.root), "--task", "PD-1"],
            cwd=self.root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        )
        self.assertEqual(failed.returncode, 2, failed.stdout + failed.stderr)
        self.assertFalse(json.loads(failed.stdout)["ok"])
        self.assertIn("<!-- delivery:PD-1 --> Accepted", (self.root / "TASKS.md").read_text())
        self.assertEqual(self.invoke("audit")[0].returncode, 1)
        self.assertEqual(self.invoke("complete", "--task", "PD-1")[0].returncode, 1)

    def test_task_definition_change_invalidates_historical_completion_proof(self):
        self.assertEqual(self.invoke("complete", "--task", "PD-1")[0].returncode, 0)
        self.config["tasks"]["PD-1"]["checks"] = ["unit", "unit"]
        # Keep this malformed change from being accepted as a valid new config.
        self.save_config()
        audit, _ = self.invoke("audit")
        self.assertEqual(audit.returncode, 2)

        self.config["tasks"]["PD-1"]["checks"] = ["unit"]
        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", "pass"]
        self.save_config()
        audit, payload = self.invoke("audit")
        self.assertEqual(audit.returncode, 1)
        self.assertIn("definition changed", payload["tasks"][0]["reason"])

    def test_latest_failure_cannot_fall_back_to_an_older_green_receipt(self):
        self.assertEqual(self.invoke("run", "--task", "PD-1")[0].returncode, 0)
        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", "raise SystemExit(7)"]
        self.save_config()
        failed, failed_payload = self.invoke("run", "--task", "PD-1")
        self.assertEqual(failed.returncode, 1)
        self.assertEqual(failed_payload["checks"][0]["status"], "failed")

        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", self.counter]
        self.save_config()
        plan, payload = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(plan.returncode, 0)
        self.assertEqual(payload["checks"][0]["decision"], "failed")
        rerun, result = self.invoke("run", "--task", "PD-1")
        self.assertEqual(rerun.returncode, 0)
        self.assertEqual(result["checks"][0]["decision"], "ran")

    def test_separate_unaffected_checks_are_reused(self):
        (self.root / "src/other.txt").write_text("other\n", encoding="utf-8")
        self.config["checks"]["other"] = {
            "command": [sys.executable, "-c", "from pathlib import Path; p=Path('other-count.txt'); p.write_text(str(int(p.read_text())+1) if p.exists() else '1')"],
            "inputs": ["src/other.txt"],
        }
        self.config["tasks"]["PD-1"]["checks"] = ["unit", "other"]
        self.save_config()
        first, first_payload = self.invoke("run", "--task", "PD-1")
        self.assertEqual(first.returncode, 0)
        self.assertEqual([item["decision"] for item in first_payload["checks"]], ["ran", "ran"])
        (self.root / "src/input.txt").write_text("new input\n", encoding="utf-8")
        second, second_payload = self.invoke("run", "--task", "PD-1")
        self.assertEqual(second.returncode, 0)
        self.assertEqual([item["decision"] for item in second_payload["checks"]], ["ran", "reused"])
        self.assertEqual((self.root / "other-count.txt").read_text(), "1")

    def test_config_task_and_path_errors_fail_closed(self):
        self.config["checks"]["unit"]["inputs"] = ["../outside.txt"]
        self.save_config()
        bad_input, _ = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(bad_input.returncode, 2)

        self.config["checks"]["unit"]["inputs"] = [".." + chr(92) + "outside.txt"]
        self.save_config()
        backslash_path, _ = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(backslash_path.returncode, 2)

        self.config["checks"]["unit"]["inputs"] = ["src/input.txt"]
        self.save_config()
        unknown, _ = self.invoke("check", "--task", "NO-SUCH-TASK")
        self.assertEqual(unknown.returncode, 2)

        self.config["tasks"]["PD-1"]["checks"] = ["missing"]
        self.save_config()
        unknown_check, _ = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(unknown_check.returncode, 2)

        self.config["tasks"]["PD-1"]["checks"] = ["unit"]
        self.config["tasks"]["PD-1"]["completion"]["path"] = "../TASKS.md"
        self.save_config()
        unsafe_ledger, _ = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(unsafe_ledger.returncode, 2)

    def test_mutating_commands_refuse_without_fcntl_and_help_names_platform_limit(self):
        driver = (
            "import importlib.util,sys;"
            f"spec=importlib.util.spec_from_file_location('gate_under_test',{str(SCRIPT)!r});"
            "module=importlib.util.module_from_spec(spec);"
            "sys.modules[spec.name]=module;"
            "spec.loader.exec_module(module);"
            "module.fcntl=None;"
            "sys.exit(module.main(sys.argv[1:]))"
        )
        refused = subprocess.run(
            [sys.executable, "-c", driver, "run", "--root", str(self.root), "--task", "PD-1"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        payload = json.loads(refused.stdout)
        self.assertEqual(refused.returncode, 2)
        self.assertIn("require POSIX fcntl locking", payload["error"])
        self.assertFalse((self.root / ".delivery/evidence").exists())
        self.assertFalse((self.root / "count.txt").exists())

        help_result = subprocess.run(
            [sys.executable, str(SCRIPT), "run", "--help"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("POSIX fcntl locking (macOS or Linux)", help_result.stdout)

    def test_symlinked_input_and_evidence_paths_are_rejected(self):
        (self.root / "outside.txt").write_text("outside\n", encoding="utf-8")
        (self.root / "src/link.txt").symlink_to(self.root / "outside.txt")
        self.config["checks"]["unit"]["inputs"] = ["src/*.txt"]
        self.save_config()
        linked_input, _ = self.invoke("plan", "--task", "PD-1")
        self.assertEqual(linked_input.returncode, 2)

        self.config["checks"]["unit"]["inputs"] = ["src/input.txt"]
        self.save_config()
        evidence = self.root / ".delivery/evidence"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.symlink_to(self.root / "outside.txt")
        unsafe_output, _ = self.invoke("run", "--task", "PD-1")
        self.assertEqual(unsafe_output.returncode, 2)

    def test_mutating_commands_refuse_a_concurrent_project_run(self):
        self.config["checks"]["unit"]["command"] = [sys.executable, "-c", "import time; time.sleep(1.5)"]
        self.save_config()
        first = subprocess.Popen(
            [sys.executable, str(SCRIPT), "run", "--root", str(self.root), "--task", "PD-1"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        pointer = self.latest_check()
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if pointer.exists() and json.loads(pointer.read_text()).get("status") == "running":
                break
            time.sleep(0.02)
        else:
            first.kill()
            self.fail("first run did not publish running state")
        concurrent, payload = self.invoke("run", "--task", "PD-1")
        stdout, stderr = first.communicate(timeout=10)
        self.assertEqual(first.returncode, 0, stdout + stderr)
        self.assertEqual(concurrent.returncode, 2)
        self.assertIn("another acceptance gate run is active", payload["error"])

    def test_audit_detects_modified_historical_logs_and_does_not_claim_unmapped_tasks(self):
        self.config["tasks"]["PD-2"] = {"checks": ["unit"]}
        self.save_config()
        completed, payload = self.invoke("complete", "--task", "PD-1")
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("completion_receipt", payload)
        audit, report = self.invoke("audit")
        self.assertEqual(audit.returncode, 0, audit.stdout)
        self.assertEqual(report["scope"], "configured tasks only")
        self.assertEqual(report["tasks"][1]["state"], "unmapped")

        pointer = json.loads(self.latest_check().read_text())
        log = self.latest_check().parent / "runs" / pointer["run_id"] / "stdout.log"
        log.write_text("edited\n", encoding="utf-8")
        invalid, invalid_payload = self.invoke("audit")
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("artifact digest", invalid_payload["tasks"][0]["reason"])


if __name__ == "__main__":
    unittest.main()

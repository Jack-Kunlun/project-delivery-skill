# Executable Acceptance and Evidence Reuse

Use this reference when initializing the executable gate, verifying task readiness, or closing work. The bundled [gate runner](../scripts/acceptance_gate.py) uses Python 3.9+ standard library only; mutating commands currently support macOS/Linux (POSIX locking). Unsupported locking environments fail explicitly. It runs reviewed project commands, validates their evidence, and controls a declared status fragment in the existing authoritative ledger. It does not provide the project's browser assertions, design baseline, or remote branch protection by itself.

## Decide what must run

Evaluate each required check separately; do not equate “a record exists” with “the record is reusable.”

| Existing evidence | Action |
| --- | --- |
| Passing receipt, intact artifacts, matching inputs/design/check definition/tools/environment, still within any validity window | Reuse it; do not execute the test again |
| Some required checks missing or stale | Run those checks only; keep unaffected passing evidence |
| Failed, interrupted, incomplete, skipped or unverified required cases | Keep the gate closed; execute or resolve the affected checks |
| No trustworthy acceptance evidence for the task | Execute its full applicable acceptance scope; this does not mean the whole repository suite |
| Legacy reports from another system | Validate their original candidate, environment, scope, results and artifacts through a project adapter; preserve provenance as validated-existing |
| Legacy report lacks a required binding | Record the precise gap and rerun that affected check; do not discard unrelated valid evidence |

Inputs must cover the implementation and its affected dependencies, design/specification, tests, fixtures, configuration and lockfiles that can change the result. Globs track matching paths as well as contents, so added and removed files matter. Lightweight probes identify actual browser/tool versions, environment, or a separately authorized source checkout. Declare relevant environment keys; values are hashed. A scope that omits a dependency cannot detect that dependency changing. Review the scope and acceptance cases before relying on reuse.

## Install during project adoption

1. Reuse the project's existing acceptance command and status authority. Copy the runner into a project-owned path such as `scripts/delivery/acceptance_gate.py`, so later tasks do not depend on an installed personal skill. Preserve local changes when upgrading; compare the maintained runner before replacing it.
2. Create a project-local config, normally `.delivery/gate.json`. Register the current task and actual applicable commands/cases. Do not replace real checks with `echo`, an always-successful script, or assertions that merely search source text. UI cases need actual rendered assertions and the design comparison required by [Delivery gates](delivery-gates.md).
3. Bind each managed task to its existing ledger entry using one unique completion marker. Keep this ledger as the sole task-status authority. Run receipts and completion proofs are evidence, not a second task board. Do not rewrite historical tasks as newly verified; enroll legacy tasks incrementally when needed.
4. Wire `complete` into the project's normal task-closeout entry point, and `audit` into its existing check/CI entry point when within scope. Preserve existing checks. Verify both integrations with a rejected completion and a valid completion/reuse exercise. If an external tracker owns status, use its supported guarded transition instead; do not create a local competing status. The bundled runner directly supports the declared local ledger only.
5. Put the actual gate/config/design/record paths in effective project instructions. Require new substantive tasks to be registered before execution, current readiness to be checked before closeout, and completion to go through the gate. Report exactly which entry points are wired. An unwired script is available tooling, not an enforced project workflow.

Creating remote workflows, required branch checks, access controls or tracker rules follows the project's authorization. A local gate cannot stop someone with write access from manually changing both code and evidence. Detect unsupported completion through the installed audit; stronger independent enforcement requires protected CI or the task system. Do not claim such protection is enabled unless actually configured and verified.

## Config and commands

Commands are argument arrays executed without a shell. Treat configuration as executable project code and review it before running. Use isolated or read-only checks; never silently run production writes, paid services or migrations to fill an evidence gap. All ordinary paths are relative to the selected project root and must stay inside it.

```json
{
  "version": 1,
  "evidence_dir": "artifacts/delivery-gate",
  "checks": {
    "notice-layout": {
      "kind": "ui",
      "command": ["node", "scripts/check-notice-layout.mjs"],
      "inputs": ["src/components/Notice.vue", "src/theme.css", "docs/design/notice.md", "scripts/check-notice-layout.mjs", "package-lock.json"],
      "required_cases": ["desktop-base", "desktop-notice", "narrow-notice"],
      "probes": {"version": ["node", "scripts/browser-version.mjs"]},
      "timeout_seconds": 120
    }
  },
  "tasks": {
    "UI-001": {
      "checks": ["notice-layout"],
      "completion": {
        "path": "docs/PROJECT.md",
        "pending": "<!-- delivery:UI-001 --> In progress",
        "done": "<!-- delivery:UI-001 --> Accepted (internal)"
      }
    }
  }
}
```

Adapt the example to real paths, cases and project states. The exact pending/done fragment must appear once in the existing ledger; include the same task marker in both. `env_keys` can declare additional environment inputs and `max_age_seconds` can restrict evidence reuse when the project requires a time window. Do not impose a universal expiration interval.

```sh
python3 scripts/delivery/acceptance_gate.py plan --root . --task UI-001
python3 scripts/delivery/acceptance_gate.py run --root . --task UI-001
python3 scripts/delivery/acceptance_gate.py check --root . --task UI-001
python3 scripts/delivery/acceptance_gate.py complete --root . --task UI-001
python3 scripts/delivery/acceptance_gate.py audit --root .
```

- `plan` reports reusable versus missing/stale/failed evidence. `check` validates current readiness and returns nonzero when required evidence is invalid; neither runs full test commands. Both may run declared lightweight probes.
- `run` runs only checks without valid passing evidence. `complete` does the same, revalidates, then updates only the declared status fragment. A failed check leaves the ledger unchanged. There is no force-pass switch.
- Repeating `complete` for an already completed task validates its existing proof and returns historical acceptance without rerunning checks or replacing that proof. A done marker without valid proof is rejected. Check a new candidate separately, use a new task, or explicitly reopen the existing entry.
- `audit` detects completed managed entries without an intact completion proof. It validates historical evidence against its accepted candidate, not today's unrelated changes. Changing a task's required checks/definition invalidates its proof. For readiness of a new candidate use `check`/`complete`, not a historical `audit` pass.

Completion publishes its passing proof only after the guarded ledger update. A concurrent ledger edit, interrupted transition, or final proof-write failure leaves the audit closed. If the marker changed but no valid proof was published, inspect the failure and explicitly reopen the entry before retrying; never manufacture a passing receipt.

Use the JSON result and process exit status in callers; do not ignore failure and write “done” afterward. Completion proves the configured acceptance scope, not release, user approval, full coverage or all product behavior. Acceptance dates/candidate identities remain part of the evidence.

## Check adapter contract

The runner supplies a fresh `DELIVERY_RUN_DIR` and `DELIVERY_REPORT_PATH`. Tests can write logs/artifacts there; structured reporters write JSON to the report path. UI checks must supply all configured case IDs exactly once and pass their actual assertions:

```json
{
  "provenance": "executed",
  "cases": [
    {"id": "desktop-notice", "status": "passed", "details": {"expected_gap": 12, "observed_gap": 12}}
  ]
}
```

The single row illustrates the format, not a complete report for the three-case config above. Missing, duplicate, failed, skipped or unverified required cases block even if the command exits zero. Ordinary command checks may use their exit code, but that alone is insufficient for a UI check. Preserve meaningful assertions: a reporter that fabricates results cannot establish correctness.

An adapter that verifies complete historical evidence reports `provenance: "validated-existing"`, links the original evidence and explains the matching inputs/environment. It must validate original results and identity, not manufacture a fresh passing report from prose saying “passed.” Missing historical metadata remains a gap. Direct visual review is separate from automated geometry; reuse a recorded review only for the same relevant candidate, baseline and environment. Required manual evidence must be validated by an explicit project adapter or remain unverified.

The runner binds receipts to input/check/environment fingerprints and log/report hashes, refuses stale evidence, records failed/in-progress runs before execution, and creates a completion proof only after success. It checks for input changes during execution and serializes its own mutating commands. File hashes detect drift and accidental corruption; they are not a signature proving honesty against an actor who can rewrite every local file. Preserve the project's artifact retention and privacy rules, and never commit secrets or all temporary evidence just to make an audit pass.

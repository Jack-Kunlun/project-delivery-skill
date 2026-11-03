#!/usr/bin/env python3
"""A small, evidence-backed acceptance gate for project delivery tasks.

Configuration commands are trusted code. Review them before running this tool.
The local evidence store detects accidental drift and incomplete execution; it is
not a security boundary against a person who can edit the project files.
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import platform
import re
import signal
import stat
import subprocess
import sys
import time
import uuid
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None


PRODUCER = "project-delivery-acceptance-gate"
PRODUCER_VERSION = "1"
SCHEMA_VERSION = 1
DEFAULT_CONFIG = ".delivery/gate.json"
DEFAULT_EVIDENCE_DIR = ".delivery/evidence"
MAX_TIMEOUT_SECONDS = 3600
MAX_REPORT_BYTES = 5 * 1024 * 1024
TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
CHECK_ID_RE = TASK_ID_RE
CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
ENV_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PROBE_NAMES = {"version", "candidate", "environment"}
CHECK_KEYS = {
    "command",
    "inputs",
    "required_cases",
    "kind",
    "probes",
    "env_keys",
    "timeout_seconds",
    "max_age_seconds",
}
TASK_KEYS = {"checks", "completion"}
CONFIG_KEYS = {"version", "evidence_dir", "checks", "tasks"}


class GateError(Exception):
    """Invalid configuration, unsafe paths, or a runtime setup failure."""


class GateFailure(Exception):
    """A policy or evidence condition that blocks acceptance."""


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_digest(value: Any) -> str:
    return _digest(_json_bytes(value))


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _parse_time(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str):
        raise GateFailure(f"{label} is missing or invalid")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GateFailure(f"{label} is invalid") from exc
    if parsed.tzinfo is None:
        raise GateFailure(f"{label} must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _require_object(value: Any, label: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise GateError(f"{label} must be an object")
    return value


def _check_keys(value: Dict[str, Any], allowed: Iterable[str], label: str) -> None:
    extras = sorted(set(value) - set(allowed))
    if extras:
        raise GateError(f"{label} has unsupported field(s): {', '.join(extras)}")


def _safe_id(value: Any, label: str, pattern: re.Pattern[str] = CHECK_ID_RE) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise GateError(f"{label} must be a safe identifier")
    return value


def _relative_path(value: Any, label: str, *, allow_glob: bool = False) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise GateError(f"{label} must be a non-empty project-relative path")
    if "\\" in value:
        raise GateError(f"{label} must use forward slashes")
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise GateError(f"{label} must be project-relative")
    if ".." in PurePosixPath(value).parts:
        raise GateError(f"{label} must not contain '..'")
    if not allow_glob and any(char in value for char in "*?["):
        raise GateError(f"{label} must not contain glob syntax")
    if not value.strip("."):
        raise GateError(f"{label} must name a path")
    return value


def _lstat(path: Path) -> Optional[os.stat_result]:
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None


def _check_components(root: Path, relative: str, *, allow_missing: bool) -> Path:
    rel = _relative_path(relative, "path")
    current = root
    parts = PurePosixPath(rel).parts
    for index, part in enumerate(parts):
        current = current / part
        info = _lstat(current)
        if info is None:
            if allow_missing:
                return root.joinpath(*parts)
            raise FileNotFoundError(current)
        if stat.S_ISLNK(info.st_mode):
            raise GateError(f"symlinks are not allowed in project paths: {relative}")
        if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise GateError(f"a parent path component is not a directory: {relative}")
    return current


def _safe_read_bytes(root: Path, relative: str, label: str) -> Tuple[bytes, os.stat_result]:
    try:
        path = _check_components(root, relative, allow_missing=False)
    except FileNotFoundError as exc:
        raise GateError(f"{label} does not exist: {relative}") from exc
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise GateError(f"cannot safely read {label}: {relative}") from exc
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise GateError(f"{label} must be a regular file: {relative}")
        data = stream.read()
        after = os.fstat(stream.fileno())
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ):
        raise GateError(f"{label} changed while being read: {relative}")
    return data, after


def _ensure_directory(root: Path, relative: str) -> Path:
    rel = _relative_path(relative, "output directory")
    current = root
    for part in PurePosixPath(rel).parts:
        current = current / part
        info = _lstat(current)
        if info is None:
            try:
                os.mkdir(current, 0o700)
            except FileExistsError:
                info = _lstat(current)
            else:
                info = _lstat(current)
        if info is None or stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise GateError(f"unsafe output directory: {relative}")
    return current


def _write_exclusive(path: Path, data: bytes, *, mode: int = 0o600) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags, mode)
    except OSError as exc:
        raise GateError(f"cannot create evidence file: {path.name}") from exc
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _atomic_replace(root: Path, relative: str, data: bytes, *, mode: int = 0o600) -> None:
    path = _check_components(root, relative, allow_missing=True)
    parent_rel = str(PurePosixPath(relative).parent)
    if parent_rel != ".":
        _ensure_directory(root, parent_rel)
    info = _lstat(path)
    if info is not None and (stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode)):
        raise GateError(f"refusing to replace unsafe output: {relative}")
    temp_rel = str(PurePosixPath(relative).with_name(PurePosixPath(relative).name + "." + uuid.uuid4().hex + ".tmp"))
    temp_path = root.joinpath(*PurePosixPath(temp_rel).parts)
    _write_exclusive(temp_path, data, mode=mode)
    try:
        current = _check_components(root, relative, allow_missing=True)
        current_info = _lstat(current)
        if current_info is not None and (stat.S_ISLNK(current_info.st_mode) or not stat.S_ISREG(current_info.st_mode)):
            raise GateError(f"refusing to replace unsafe output: {relative}")
        os.replace(temp_path, path)
        _fsync_directory(path.parent)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def _fsync_directory(path: Path) -> None:
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass


def _load_config(root: Path, config_rel: str) -> Dict[str, Any]:
    config_rel = _relative_path(config_rel, "--config")
    data, _ = _safe_read_bytes(root, config_rel, "configuration")
    try:
        raw = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("configuration must be valid UTF-8 JSON") from exc
    raw = _require_object(raw, "configuration")
    _check_keys(raw, CONFIG_KEYS, "configuration")
    if raw.get("version") != SCHEMA_VERSION or isinstance(raw.get("version"), bool):
        raise GateError(f"configuration version must be {SCHEMA_VERSION}")
    evidence_dir = _relative_path(raw.get("evidence_dir", DEFAULT_EVIDENCE_DIR), "evidence_dir")
    raw_checks = _require_object(raw.get("checks"), "checks")
    if not raw_checks:
        raise GateError("checks must contain at least one check")
    checks: Dict[str, Dict[str, Any]] = {}
    for check_id, raw_check in raw_checks.items():
        check_id = _safe_id(check_id, "check ID")
        item = _require_object(raw_check, f"check {check_id}")
        _check_keys(item, CHECK_KEYS, f"check {check_id}")
        command = item.get("command")
        if not isinstance(command, list) or not command or any(not isinstance(arg, str) or not arg or "\x00" in arg for arg in command):
            raise GateError(f"check {check_id} command must be a non-empty argv array of non-empty strings")
        raw_inputs = item.get("inputs")
        if not isinstance(raw_inputs, list) or not raw_inputs:
            raise GateError(f"check {check_id} inputs must be a non-empty array")
        inputs = [_relative_path(value, f"check {check_id} input", allow_glob=True) for value in raw_inputs]
        if len(set(inputs)) != len(inputs):
            raise GateError(f"check {check_id} inputs must not contain duplicates")
        kind = item.get("kind", "command")
        if not isinstance(kind, str) or kind not in {"command", "ui"}:
            raise GateError(f"check {check_id} kind must be 'command' or 'ui'")
        required_cases = item.get("required_cases", [])
        if not isinstance(required_cases, list) or any(not isinstance(case, str) or not CASE_ID_RE.fullmatch(case) for case in required_cases):
            raise GateError(f"check {check_id} required_cases must be an array of safe case IDs")
        if len(set(required_cases)) != len(required_cases):
            raise GateError(f"check {check_id} required_cases must be unique")
        if kind == "ui" and not required_cases:
            raise GateError(f"UI check {check_id} must define non-empty required_cases")
        raw_probes = item.get("probes", {})
        raw_probes = _require_object(raw_probes, f"check {check_id} probes")
        if set(raw_probes) - PROBE_NAMES:
            raise GateError(f"check {check_id} probes may use only version, candidate, and environment")
        probes: Dict[str, List[str]] = {}
        for name, argv in raw_probes.items():
            if not isinstance(argv, list) or not argv or any(not isinstance(arg, str) or not arg or "\x00" in arg for arg in argv):
                raise GateError(f"check {check_id} probe {name} must be a non-empty argv array")
            probes[name] = list(argv)
        env_keys = item.get("env_keys", [])
        if not isinstance(env_keys, list) or any(not isinstance(key, str) or not ENV_KEY_RE.fullmatch(key) for key in env_keys):
            raise GateError(f"check {check_id} env_keys must be an array of environment variable names")
        if len(set(env_keys)) != len(env_keys):
            raise GateError(f"check {check_id} env_keys must be unique")
        timeout = item.get("timeout_seconds", 300)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT_SECONDS:
            raise GateError(f"check {check_id} timeout_seconds must be from 1 to {MAX_TIMEOUT_SECONDS}")
        max_age = item.get("max_age_seconds")
        if max_age is not None and (isinstance(max_age, bool) or not isinstance(max_age, int) or max_age <= 0):
            raise GateError(f"check {check_id} max_age_seconds must be a positive integer")
        checks[check_id] = {
            "command": list(command),
            "inputs": inputs,
            "required_cases": list(required_cases),
            "kind": kind,
            "probes": probes,
            "env_keys": list(env_keys),
            "timeout_seconds": timeout,
            "max_age_seconds": max_age,
        }
    raw_tasks = _require_object(raw.get("tasks"), "tasks")
    tasks: Dict[str, Dict[str, Any]] = {}
    for task_id, raw_task in raw_tasks.items():
        task_id = _safe_id(task_id, "task ID")
        item = _require_object(raw_task, f"task {task_id}")
        _check_keys(item, TASK_KEYS, f"task {task_id}")
        refs = item.get("checks")
        if not isinstance(refs, list) or not refs:
            raise GateError(f"task {task_id} checks must be a non-empty array")
        if any(not isinstance(ref, str) for ref in refs):
            raise GateError(f"task {task_id} checks must contain check IDs")
        refs = [_safe_id(ref, f"task {task_id} check reference") for ref in refs]
        if len(set(refs)) != len(refs):
            raise GateError(f"task {task_id} checks must not contain duplicates")
        unknown = sorted(set(refs) - set(checks))
        if unknown:
            raise GateError(f"task {task_id} references unknown check(s): {', '.join(unknown)}")
        completion = item.get("completion")
        if completion is not None:
            completion = _require_object(completion, f"task {task_id} completion")
            _check_keys(completion, {"path", "pending", "done"}, f"task {task_id} completion")
            path = _relative_path(completion.get("path"), f"task {task_id} completion path")
            pending = completion.get("pending")
            done = completion.get("done")
            marker = f"<!-- delivery:{task_id} -->"
            if not isinstance(pending, str) or not isinstance(done, str) or not pending or not done:
                raise GateError(f"task {task_id} pending and done fragments must be non-empty strings")
            if pending == done or pending in done or done in pending:
                raise GateError(f"task {task_id} pending and done fragments must be distinct")
            if pending.count(marker) != 1 or done.count(marker) != 1:
                raise GateError(f"task {task_id} pending and done fragments must each include {marker!r} exactly once")
            if pending.count("<!-- delivery:") != 1 or done.count("<!-- delivery:") != 1:
                raise GateError(f"task {task_id} status fragments must include only their task marker")
            completion = {"path": path, "pending": pending, "done": done}
        tasks[task_id] = {"checks": refs, "completion": completion}
    return {
        "version": SCHEMA_VERSION,
        "evidence_dir": evidence_dir,
        "checks": checks,
        "tasks": tasks,
    }


def _selected_checks(config: Dict[str, Any], task_id: Optional[str]) -> List[str]:
    if task_id is None:
        return sorted(config["checks"])
    task_id = _safe_id(task_id, "task ID")
    if task_id not in config["tasks"]:
        raise GateError(f"unknown task: {task_id}")
    return list(config["tasks"][task_id]["checks"])


def _hash_file(path: Path) -> str:
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise GateError(f"cannot safely read input file: {path.name}") from exc
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise GateError(f"input is not a regular file: {path.name}")
        hasher = hashlib.sha256()
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
        after = os.fstat(stream.fileno())
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ):
        raise GateError(f"input changed while being fingerprinted: {path.name}")
    return hasher.hexdigest()


def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _input_fingerprints(root: Path, check: Dict[str, Any], evidence_dir: str) -> List[Dict[str, str]]:
    evidence_abs = root.joinpath(*PurePosixPath(evidence_dir).parts)
    selected: Dict[str, Path] = {}
    for pattern in check["inputs"]:
        matches = glob.glob(str(root / pattern), recursive=True)
        pattern_files = 0
        for raw_path in matches:
            path = Path(raw_path)
            try:
                rel = path.relative_to(root)
            except ValueError as exc:
                raise GateError(f"input pattern escaped the project root: {pattern}") from exc
            rel_text = rel.as_posix()
            _relative_path(rel_text, "matched input")
            try:
                safe_path = _check_components(root, rel_text, allow_missing=False)
            except FileNotFoundError:
                continue
            if _is_under(safe_path, evidence_abs):
                continue
            info = _lstat(safe_path)
            if info is None:
                continue
            if stat.S_ISLNK(info.st_mode):
                raise GateError(f"input matches a symlink: {rel_text}")
            if stat.S_ISREG(info.st_mode):
                pattern_files += 1
                selected[rel_text] = safe_path
        if pattern_files == 0:
            raise GateError(f"input pattern matched no files: {pattern}")
    return [{"path": name, "sha256": _hash_file(selected[name])} for name in sorted(selected)]


def _cleanup_process_group(pid: int) -> None:
    if os.name != "posix":
        return
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except OSError:
        return
    deadline = time.monotonic() + 0.2
    while time.monotonic() < deadline:
        try:
            os.killpg(pid, 0)
        except ProcessLookupError:
            return
        except OSError:
            return
        time.sleep(0.02)
    try:
        os.killpg(pid, signal.SIGKILL)
    except OSError:
        pass


def _capture_probe(argv: Sequence[str], root: Path, timeout: int, name: str) -> Tuple[int, bytes]:
    try:
        process = subprocess.Popen(
            list(argv),
            cwd=str(root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=(os.name == "posix"),
            close_fds=True,
        )
    except OSError as exc:
        raise GateError(f"probe {name} could not start") from exc
    try:
        try:
            stdout, _ = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    pass
            else:  # pragma: no cover - Windows fallback
                process.kill()
            process.communicate()
            raise GateError(f"probe {name} timed out") from exc
        if process.returncode != 0:
            raise GateError(f"probe {name} exited with status {process.returncode}")
        return process.returncode, stdout
    finally:
        _cleanup_process_group(process.pid)


def _fingerprint(root: Path, config: Dict[str, Any], check_id: str) -> Tuple[str, str]:
    check = config["checks"][check_id]
    inputs = _input_fingerprints(root, check, config["evidence_dir"])
    probe_results: Dict[str, Any] = {}
    for name in sorted(check["probes"]):
        argv = check["probes"][name]
        code, stdout = _capture_probe(argv, root, min(check["timeout_seconds"], 60), name)
        probe_results[name] = {
            "argv": argv,
            "returncode": code,
            "stdout_sha256": _digest(stdout),
        }
    env_hashes = {}
    for key in sorted(check["env_keys"]):
        marker = os.environ.get(key)
        value = b"<unset>" if marker is None else marker.encode("utf-8", "surrogateescape")
        env_hashes[key] = _digest(value)
    try:
        runner_hash = _digest(Path(__file__).read_bytes())
    except OSError as exc:
        raise GateError("cannot fingerprint the acceptance gate runner") from exc
    definition_hash = _canonical_digest(check)
    data = {
        "schema_version": SCHEMA_VERSION,
        "producer_version": PRODUCER_VERSION,
        "runner_sha256": runner_hash,
        "project_root_sha256": _digest(str(root).encode("utf-8", "surrogateescape")),
        "check_id": check_id,
        "check_definition_sha256": definition_hash,
        "inputs": inputs,
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "executable_sha256": _digest(str(Path(sys.executable).resolve()).encode("utf-8", "surrogateescape")),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "environment_sha256": env_hashes,
        "probes": probe_results,
    }
    return _canonical_digest(data), definition_hash


def _safe_json_file(root: Path, relative: str, label: str, *, max_bytes: Optional[int] = None) -> Tuple[Optional[Any], Optional[bytes]]:
    try:
        data, _ = _safe_read_bytes(root, relative, label)
    except GateError as exc:
        if "does not exist" in str(exc):
            return None, None
        raise
    if max_bytes is not None and len(data) > max_bytes:
        raise GateFailure(f"{label} exceeds the {max_bytes}-byte limit")
    try:
        return json.loads(data.decode("utf-8")), data
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateFailure(f"{label} is not valid UTF-8 JSON") from exc


def _latest_relative(check_id: str) -> str:
    return f"checks/{check_id}/latest.json"


def _run_receipt_relative(check_id: str, run_id: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{32}", run_id):
        raise GateFailure("run ID is invalid")
    return f"checks/{check_id}/runs/{run_id}/receipt.json"


def _verify_artifacts(root: Path, evidence_dir: str, check_id: str, receipt: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[bytes]]:
    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, dict) or "stdout.log" not in artifacts or "stderr.log" not in artifacts:
        raise GateFailure("run receipt does not list both log artifacts")
    allowed = {"stdout.log", "stderr.log", "results.json"}
    if set(artifacts) - allowed:
        raise GateFailure("run receipt lists an unsupported artifact")
    run_id = receipt.get("run_id")
    run_rel = f"checks/{check_id}/runs/{run_id}"
    for name, expected in artifacts.items():
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise GateFailure(f"run receipt has an invalid digest for {name}")
        relative = f"{evidence_dir}/{run_rel}/{name}"
        try:
            data, _ = _safe_read_bytes(root, relative, f"run artifact {name}")
        except GateError as exc:
            raise GateFailure(f"run artifact is missing or unsafe: {name}") from exc
        if _digest(data) != expected:
            raise GateFailure(f"run artifact digest does not match: {name}")
        if name == "results.json" and len(data) > MAX_REPORT_BYTES:
            raise GateFailure("results report exceeds the size limit")
    report_data = None
    report_obj = None
    if "results.json" in artifacts:
        report_data, _ = _safe_read_bytes(root, f"{evidence_dir}/{run_rel}/results.json", "results report")
        try:
            report_obj = json.loads(report_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            report_obj = None
    return report_obj, report_data


def _validate_cases(check: Dict[str, Any], report_obj: Any) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str], str]:
    if not check["required_cases"]:
        return True, None, None, ""
    if not isinstance(report_obj, dict) or not isinstance(report_obj.get("cases"), list):
        return False, None, None, "required case report is missing or malformed"
    raw_cases = report_obj["cases"]
    cases: List[Dict[str, Any]] = []
    found: Dict[str, int] = {}
    for case in raw_cases:
        if not isinstance(case, dict):
            return False, None, None, "case report contains a malformed case"
        case_id = case.get("id")
        status = case.get("status")
        if not isinstance(case_id, str) or not CASE_ID_RE.fullmatch(case_id):
            return False, None, None, "case report contains an invalid case ID"
        if not isinstance(status, str) or status not in {"passed", "failed", "skipped", "unverified"}:
            return False, None, None, f"case {case_id} has an invalid status"
        found[case_id] = found.get(case_id, 0) + 1
        if found[case_id] > 1:
            return False, None, None, f"case report contains duplicate ID {case_id}"
        cases.append(case)
        if status != "passed":
            return False, cases, report_obj.get("provenance"), f"case {case_id} is {status}"
    for required in check["required_cases"]:
        if found.get(required) != 1:
            return False, cases, report_obj.get("provenance"), f"required case is missing: {required}"
    provenance = report_obj.get("provenance")
    if provenance is not None and (not isinstance(provenance, str) or provenance not in {"executed", "validated-existing"}):
        return False, cases, provenance if isinstance(provenance, str) else None, "case report provenance is invalid"
    return True, cases, provenance, ""


def _verify_run_receipt(
    root: Path,
    evidence_dir: str,
    check_id: str,
    run_id: str,
    receipt_digest: str,
    check: Dict[str, Any],
    definition_hash: str,
    *,
    expected_fingerprint: Optional[str] = None,
    max_age_seconds: Optional[int] = None,
) -> Dict[str, Any]:
    relative = f"{evidence_dir}/{_run_receipt_relative(check_id, run_id)}"
    try:
        data, _ = _safe_read_bytes(root, relative, "run receipt")
    except GateError as exc:
        raise GateFailure("run receipt is missing or unsafe") from exc
    if _digest(data) != receipt_digest:
        raise GateFailure("run receipt digest does not match")
    try:
        receipt = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateFailure("run receipt is not valid UTF-8 JSON") from exc
    if not isinstance(receipt, dict):
        raise GateFailure("run receipt is not an object")
    if (
        receipt.get("schema_version") != SCHEMA_VERSION
        or receipt.get("producer") != PRODUCER
        or receipt.get("producer_version") != PRODUCER_VERSION
        or receipt.get("check_id") != check_id
        or receipt.get("run_id") != run_id
    ):
        raise GateFailure("run receipt identity or producer version does not match")
    created = _parse_time(receipt.get("finished_at"), "run receipt finished_at")
    now = dt.datetime.now(dt.timezone.utc)
    if created > now + dt.timedelta(minutes=5):
        raise GateFailure("run receipt time is in the future")
    if receipt.get("check_definition_sha256") != definition_hash:
        raise GateFailure("run receipt check definition does not match")
    if expected_fingerprint is not None and receipt.get("fingerprint") != expected_fingerprint:
        raise GateFailure("run receipt fingerprint is stale")
    if max_age_seconds is not None and (now - created).total_seconds() > max_age_seconds:
        raise GateFailure("run receipt has expired")
    if receipt.get("status") != "passed" or receipt.get("exit_code") != 0 or receipt.get("timed_out") is not False:
        raise GateFailure("latest run did not pass")
    if receipt.get("fingerprint_after") != receipt.get("fingerprint"):
        raise GateFailure("inputs changed during the run")
    report_obj, _ = _verify_artifacts(root, evidence_dir, check_id, receipt)
    case_ok, cases, provenance, reason = _validate_cases(check, report_obj)
    if not case_ok:
        raise GateFailure(reason or "required cases did not pass")
    if receipt.get("cases") != cases or receipt.get("provenance") != provenance:
        raise GateFailure("run receipt case evidence does not match the report")
    return receipt


def _read_latest(root: Path, config: Dict[str, Any], check_id: str, fingerprint: str, definition_hash: str) -> Dict[str, Any]:
    evidence_dir = config["evidence_dir"]
    latest_rel = f"{evidence_dir}/{_latest_relative(check_id)}"
    try:
        latest, latest_bytes = _safe_json_file(root, latest_rel, "latest check pointer")
    except GateFailure as exc:
        return {"decision": "failed", "reason": str(exc), "fingerprint": fingerprint}
    except GateError as exc:
        if "does not exist" in str(exc):
            return {"decision": "missing", "reason": "no run receipt exists", "fingerprint": fingerprint}
        return {"decision": "failed", "reason": str(exc), "fingerprint": fingerprint}
    if latest is None:
        return {"decision": "missing", "reason": "no run receipt exists", "fingerprint": fingerprint}
    if not isinstance(latest, dict) or latest.get("schema_version") != SCHEMA_VERSION or latest.get("producer") != PRODUCER or latest.get("producer_version") != PRODUCER_VERSION or latest.get("check_id") != check_id:
        return {"decision": "failed", "reason": "latest check pointer identity is invalid", "fingerprint": fingerprint}
    status = latest.get("status")
    if status == "running":
        return {"decision": "failed", "reason": "latest check run was interrupted or is still running", "fingerprint": fingerprint}
    if status == "failed":
        return {"decision": "failed", "reason": "latest check run failed", "fingerprint": fingerprint}
    if status != "passed":
        return {"decision": "failed", "reason": "latest check pointer status is invalid", "fingerprint": fingerprint}
    run_id = latest.get("run_id")
    receipt_digest = latest.get("receipt_sha256")
    if not isinstance(run_id, str) or not re.fullmatch(r"[0-9a-f]{32}", run_id):
        return {"decision": "failed", "reason": "latest check pointer run ID is invalid", "fingerprint": fingerprint}
    if not isinstance(receipt_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", receipt_digest):
        return {"decision": "failed", "reason": "latest check pointer receipt digest is invalid", "fingerprint": fingerprint}
    try:
        receipt = _verify_run_receipt(
            root,
            evidence_dir,
            check_id,
            run_id,
            receipt_digest,
            config["checks"][check_id],
            definition_hash,
            expected_fingerprint=fingerprint,
            max_age_seconds=config["checks"][check_id]["max_age_seconds"],
        )
        return {
            "decision": "reusable",
            "reason": "current passing receipt and artifacts match",
            "fingerprint": fingerprint,
            "run_id": run_id,
            "receipt_sha256": receipt_digest,
            "receipt": receipt,
        }
    except GateFailure as exc:
        reason = str(exc)
        stale_terms = ("fingerprint is stale", "expired", "check definition does not match", "producer version does not match")
        decision = "stale" if any(term in reason for term in stale_terms) else "failed"
        return {"decision": decision, "reason": reason, "fingerprint": fingerprint}


def _evaluate(root: Path, config: Dict[str, Any], check_id: str) -> Dict[str, Any]:
    fingerprint, definition_hash = _fingerprint(root, config, check_id)
    result = _read_latest(root, config, check_id, fingerprint, definition_hash)
    result["check_id"] = check_id
    result["definition_hash"] = definition_hash
    return result


def _open_log(path: Path):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    return os.fdopen(fd, "wb")


def _safe_report(root: Path, run_dir_rel: str, run_dir: Path) -> Tuple[Optional[bytes], Optional[Any]]:
    rel = f"{run_dir_rel}/results.json"
    info = _lstat(run_dir / "results.json")
    if info is None:
        return None, None
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise GateError("command created an unsafe results report")
    try:
        data, _ = _safe_read_bytes(root, rel, "results report")
    except GateError as exc:
        raise GateError("cannot safely read results report") from exc
    if len(data) > MAX_REPORT_BYTES:
        return data, None
    try:
        return data, json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return data, None


def _execute_check(root: Path, config: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
    check_id = evaluation["check_id"]
    check = config["checks"][check_id]
    evidence_dir = config["evidence_dir"]
    base_rel = f"{evidence_dir}/checks/{check_id}"
    _ensure_directory(root, f"{evidence_dir}/checks/{check_id}/runs")
    run_id = uuid.uuid4().hex
    run_dir_rel = f"{evidence_dir}/checks/{check_id}/runs/{run_id}"
    run_dir = _ensure_directory(root, run_dir_rel)
    started_at = _utc_now()
    state = {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "producer_version": PRODUCER_VERSION,
        "check_id": check_id,
        "run_id": run_id,
        "status": "running",
        "started_at": started_at,
        "fingerprint": evaluation["fingerprint"],
    }
    _write_exclusive(run_dir / "running.json", _json_bytes(state))
    latest = {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "producer_version": PRODUCER_VERSION,
        "check_id": check_id,
        "run_id": run_id,
        "status": "running",
        "updated_at": started_at,
    }
    _atomic_replace(root, f"{base_rel}/latest.json", _json_bytes(latest))
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    env = os.environ.copy()
    env["DELIVERY_RUN_DIR"] = str(run_dir)
    env["DELIVERY_REPORT_PATH"] = str(run_dir / "results.json")
    exit_code: Optional[int] = None
    timed_out = False
    spawn_error: Optional[str] = None
    try:
        with _open_log(stdout_path) as stdout_log, _open_log(stderr_path) as stderr_log:
            try:
                process = subprocess.Popen(
                    check["command"],
                    cwd=str(root),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_log,
                    stderr=stderr_log,
                    start_new_session=(os.name == "posix"),
                    close_fds=True,
                )
            except OSError as exc:
                spawn_error = f"check command could not start: {type(exc).__name__}"
                stderr_log.write((spawn_error + "\n").encode("utf-8"))
            else:
                try:
                    exit_code = process.wait(timeout=check["timeout_seconds"])
                except subprocess.TimeoutExpired:
                    timed_out = True
                    if os.name == "posix":
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except OSError:
                            pass
                    else:  # pragma: no cover - Windows fallback
                        process.kill()
                    exit_code = process.wait()
                finally:
                    _cleanup_process_group(process.pid)
    except OSError as exc:
        spawn_error = f"could not create check logs: {type(exc).__name__}"
    artifacts: Dict[str, str] = {}
    for name, path in (("stdout.log", stdout_path), ("stderr.log", stderr_path)):
        try:
            log_data, _ = _safe_read_bytes(root, f"{run_dir_rel}/{name}", f"check log {name}")
            artifacts[name] = _digest(log_data)
        except (OSError, GateError) as exc:
            raise GateError(f"could not read check log {name}") from exc
    report_bytes, report_obj = _safe_report(root, run_dir_rel, run_dir)
    if report_bytes is not None:
        artifacts["results.json"] = _digest(report_bytes)
    cases_ok, cases, provenance, cases_reason = _validate_cases(check, report_obj)
    post_fingerprint: Optional[str]
    try:
        post_fingerprint, _ = _fingerprint(root, config, check_id)
    except GateError as exc:
        post_fingerprint = None
        cases_reason = cases_reason or f"could not revalidate inputs after run: {exc}"
    same_inputs = post_fingerprint == evaluation["fingerprint"]
    failure = spawn_error
    if timed_out:
        failure = "check command timed out"
    elif exit_code != 0:
        failure = failure or f"check command exited with status {exit_code}"
    elif not same_inputs:
        failure = failure or "inputs or environment changed during the run"
    elif not cases_ok:
        failure = failure or cases_reason
    passed = failure is None
    finished_at = _utc_now()
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "producer_version": PRODUCER_VERSION,
        "check_id": check_id,
        "run_id": run_id,
        "status": "passed" if passed else "failed",
        "started_at": started_at,
        "finished_at": finished_at,
        "fingerprint": evaluation["fingerprint"],
        "fingerprint_after": post_fingerprint,
        "check_definition_sha256": evaluation["definition_hash"],
        "exit_code": exit_code,
        "timed_out": timed_out,
        "failure": failure,
        "cases": cases,
        "provenance": provenance,
        "artifacts": artifacts,
    }
    receipt_bytes = _json_bytes(receipt)
    _write_exclusive(run_dir / "receipt.json", receipt_bytes)
    latest = {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "producer_version": PRODUCER_VERSION,
        "check_id": check_id,
        "run_id": run_id,
        "status": "passed" if passed else "failed",
        "receipt_sha256": _digest(receipt_bytes),
        "updated_at": finished_at,
    }
    _atomic_replace(root, f"{base_rel}/latest.json", _json_bytes(latest))
    return {
        "check_id": check_id,
        "run_id": run_id,
        "status": "passed" if passed else "failed",
        "decision": "ran",
        "reason": "check passed" if passed else failure,
        "fingerprint": evaluation["fingerprint"],
        "receipt_sha256": _digest(receipt_bytes),
    }


class _ProjectLock:
    def __init__(self, root: Path, evidence_dir: str):
        self.root = root
        self.evidence_dir = evidence_dir
        self.path: Optional[Path] = None
        self.fd: Optional[int] = None

    def __enter__(self):
        if fcntl is None:
            raise GateError("mutating commands require POSIX fcntl locking (macOS or Linux)")
        evidence_path = _ensure_directory(self.root, self.evidence_dir)
        lock_path = evidence_path / ".acceptance-gate.lock"
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        try:
            self.fd = os.open(lock_path, flags, 0o600)
        except OSError as exc:
            raise GateError("cannot open project acceptance lock safely") from exc
        info = os.fstat(self.fd)
        if not stat.S_ISREG(info.st_mode):
            os.close(self.fd)
            self.fd = None
            raise GateError("project acceptance lock is not a regular file")
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(self.fd)
            self.fd = None
            raise GateError("another acceptance gate run is active") from exc
        self.path = lock_path
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            os.close(self.fd)
            self.fd = None


def _run_selected(root: Path, config: Dict[str, Any], check_ids: Sequence[str]) -> List[Dict[str, Any]]:
    # Preflight every fingerprint and probe before executing any configured check.
    evaluations = [_evaluate(root, config, check_id) for check_id in check_ids]
    results: List[Dict[str, Any]] = []
    for evaluation in evaluations:
        if evaluation["decision"] == "reusable":
            results.append({
                "check_id": evaluation["check_id"],
                "status": "passed",
                "decision": "reused",
                "reason": evaluation["reason"],
                "fingerprint": evaluation["fingerprint"],
                "run_id": evaluation.get("run_id"),
                "receipt_sha256": evaluation.get("receipt_sha256"),
            })
            continue
        # A prior failed, interrupted, stale, or corrupt attempt is replaced first.
        result = _execute_check(root, config, evaluation)
        results.append(result)
    return results


def _task_definition_hash(config: Dict[str, Any], task_id: str) -> str:
    task = config["tasks"][task_id]
    return _canonical_digest({
        "task_id": task_id,
        "task": task,
        "check_definitions": {check_id: config["checks"][check_id] for check_id in task["checks"]},
    })


def _task_marker_state(root: Path, task_id: str, task: Dict[str, Any]) -> Tuple[str, bytes, os.stat_result]:
    completion = task["completion"]
    if completion is None:
        raise GateError(f"task {task_id} has no completion ledger mapping")
    content_bytes, info = _safe_read_bytes(root, completion["path"], f"task {task_id} ledger")
    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GateError(f"task {task_id} ledger must be UTF-8") from exc
    marker = f"<!-- delivery:{task_id} -->"
    if content.count(marker) != 1:
        raise GateFailure(f"task {task_id} marker must occur exactly once in its ledger")
    has_pending = content.count(completion["pending"]) == 1
    has_done = content.count(completion["done"]) == 1
    if has_pending and not has_done:
        return "pending", content_bytes, info
    if has_done and not has_pending:
        return "done", content_bytes, info
    raise GateFailure(f"task {task_id} ledger must contain exactly one pending or done fragment")


def _atomic_ledger_update(root: Path, task_id: str, task: Dict[str, Any], original: bytes, original_info: os.stat_result) -> None:
    completion = task["completion"]
    path_rel = completion["path"]
    try:
        content = original.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GateError(f"task {task_id} ledger must be UTF-8") from exc
    if content.count(completion["pending"]) != 1 or content.count(completion["done"]) != 0:
        raise GateFailure(f"task {task_id} is no longer pending")
    updated = content.replace(completion["pending"], completion["done"], 1).encode("utf-8")
    path = _check_components(root, path_rel, allow_missing=False)
    temp_rel = str(PurePosixPath(path_rel).with_name(PurePosixPath(path_rel).name + "." + uuid.uuid4().hex + ".tmp"))
    temp_path = root.joinpath(*PurePosixPath(temp_rel).parts)
    mode = stat.S_IMODE(original_info.st_mode)
    _write_exclusive(temp_path, updated, mode=mode)
    try:
        current, current_info = _safe_read_bytes(root, path_rel, f"task {task_id} ledger")
        if current != original or (current_info.st_dev, current_info.st_ino) != (original_info.st_dev, original_info.st_ino):
            raise GateFailure(f"task {task_id} ledger changed during completion")
        current_path = _check_components(root, path_rel, allow_missing=False)
        os.replace(temp_path, current_path)
        _fsync_directory(current_path.parent)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def _latest_run_reference(root: Path, config: Dict[str, Any], check_id: str, expected_fingerprint: str) -> Dict[str, Any]:
    current = _evaluate(root, config, check_id)
    if current["decision"] != "reusable" or current["fingerprint"] != expected_fingerprint:
        raise GateFailure(f"check {check_id} did not remain current and passing")
    return {
        "check_id": check_id,
        "run_id": current["run_id"],
        "receipt_path": _run_receipt_relative(check_id, current["run_id"]),
        "receipt_sha256": current["receipt_sha256"],
        "fingerprint": current["fingerprint"],
    }


def _prepare_completion_receipt(root: Path, config: Dict[str, Any], task_id: str, references: List[Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
    evidence_dir = config["evidence_dir"]
    completion_id = uuid.uuid4().hex
    task_base = f"{evidence_dir}/tasks/{task_id}"
    run_rel = f"{task_base}/completions/{completion_id}"
    run_dir = _ensure_directory(root, run_rel)
    finished = _utc_now()
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "producer_version": PRODUCER_VERSION,
        "task_id": task_id,
        "completion_id": completion_id,
        "status": "passed",
        "completed_at": finished,
        "task_definition_sha256": _task_definition_hash(config, task_id),
        "checks": references,
    }
    receipt_bytes = _json_bytes(receipt)
    _write_exclusive(run_dir / "receipt.json", receipt_bytes)
    pointer = {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "producer_version": PRODUCER_VERSION,
        "task_id": task_id,
        "completion_id": completion_id,
        "status": "passed",
        "receipt_sha256": _digest(receipt_bytes),
        "updated_at": finished,
    }
    # A prepared receipt is not a proof until the guarded ledger transition succeeds.
    return f"{task_base}/completions/{completion_id}/receipt.json", pointer


def _validate_completion_proof(root: Path, config: Dict[str, Any], task_id: str) -> Dict[str, Any]:
    evidence_dir = config["evidence_dir"]
    pointer_rel = f"{evidence_dir}/tasks/{task_id}/latest.json"
    try:
        pointer, _ = _safe_json_file(root, pointer_rel, "completion proof pointer")
    except (GateError, GateFailure) as exc:
        raise GateFailure(f"task {task_id} has no valid completion proof: {exc}") from exc
    if not isinstance(pointer, dict):
        raise GateFailure(f"task {task_id} has no valid completion proof")
    if (
        pointer.get("schema_version") != SCHEMA_VERSION
        or pointer.get("producer") != PRODUCER
        or pointer.get("producer_version") != PRODUCER_VERSION
        or pointer.get("task_id") != task_id
        or pointer.get("status") != "passed"
    ):
        raise GateFailure(f"task {task_id} completion proof pointer is invalid")
    completion_id = pointer.get("completion_id")
    if not isinstance(completion_id, str) or not re.fullmatch(r"[0-9a-f]{32}", completion_id):
        raise GateFailure(f"task {task_id} completion proof ID is invalid")
    relative = f"{evidence_dir}/tasks/{task_id}/completions/{completion_id}/receipt.json"
    try:
        data, _ = _safe_read_bytes(root, relative, "completion receipt")
    except GateError as exc:
        raise GateFailure(f"task {task_id} completion receipt is missing or unsafe") from exc
    if _digest(data) != pointer.get("receipt_sha256"):
        raise GateFailure(f"task {task_id} completion receipt digest does not match")
    try:
        receipt = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateFailure(f"task {task_id} completion receipt is invalid JSON") from exc
    if not isinstance(receipt, dict) or (
        receipt.get("schema_version") != SCHEMA_VERSION
        or receipt.get("producer") != PRODUCER
        or receipt.get("producer_version") != PRODUCER_VERSION
        or receipt.get("task_id") != task_id
        or receipt.get("completion_id") != completion_id
        or receipt.get("status") != "passed"
    ):
        raise GateFailure(f"task {task_id} completion receipt identity is invalid")
    completed_at = _parse_time(receipt.get("completed_at"), "completion receipt completed_at")
    if completed_at > dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5):
        raise GateFailure(f"task {task_id} completion receipt time is in the future")
    if receipt.get("task_definition_sha256") != _task_definition_hash(config, task_id):
        raise GateFailure(f"task {task_id} definition changed after completion")
    check_refs = receipt.get("checks")
    expected_ids = config["tasks"][task_id]["checks"]
    if not isinstance(check_refs, list) or [item.get("check_id") if isinstance(item, dict) else None for item in check_refs] != expected_ids:
        raise GateFailure(f"task {task_id} completion proof check list does not match")
    for item in check_refs:
        check_id = item["check_id"]
        if not isinstance(item.get("run_id"), str) or not isinstance(item.get("receipt_sha256"), str):
            raise GateFailure(f"task {task_id} has an invalid check receipt reference")
        expected_path = _run_receipt_relative(check_id, item["run_id"])
        if item.get("receipt_path") != expected_path:
            raise GateFailure(f"task {task_id} has an unsafe check receipt path")
        check = config["checks"][check_id]
        definition_hash = _canonical_digest(check)
        run_receipt = _verify_run_receipt(
            root,
            evidence_dir,
            check_id,
            item["run_id"],
            item["receipt_sha256"],
            check,
            definition_hash,
        )
        if item.get("fingerprint") != run_receipt.get("fingerprint"):
            raise GateFailure(f"task {task_id} check fingerprint reference does not match")
        if _parse_time(run_receipt.get("finished_at"), "run receipt finished_at") > completed_at + dt.timedelta(minutes=5):
            raise GateFailure(f"task {task_id} references a check that ran after completion")
    return receipt


def _lock_context(root: Path, config: Dict[str, Any]):
    return _ProjectLock(root, config["evidence_dir"])


def _render_check_results(root: Path, config: Dict[str, Any], check_ids: Sequence[str]) -> List[Dict[str, Any]]:
    results = []
    for check_id in check_ids:
        evaluated = _evaluate(root, config, check_id)
        results.append({key: evaluated[key] for key in ("check_id", "decision", "reason", "fingerprint")})
    return results


def _task_completion_state(root: Path, config: Dict[str, Any], task_id: str) -> str:
    task = config["tasks"][task_id]
    state, _, _ = _task_marker_state(root, task_id, task)
    return state


def _audit(root: Path, config: Dict[str, Any], task_ids: Sequence[str]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    failures: List[str] = []
    for task_id in task_ids:
        task = config["tasks"][task_id]
        if task["completion"] is None:
            results.append({"task_id": task_id, "state": "unmapped", "ok": True, "reason": "no authoritative ledger mapping configured"})
            continue
        try:
            state, _, _ = _task_marker_state(root, task_id, task)
            if state == "pending":
                results.append({"task_id": task_id, "state": "pending", "ok": True, "reason": "not a completed ledger row"})
                continue
            proof = _validate_completion_proof(root, config, task_id)
            results.append({"task_id": task_id, "state": "done", "ok": True, "completion_id": proof["completion_id"], "reason": "historical completion proof and artifacts are intact"})
        except (GateError, GateFailure) as exc:
            failures.append(task_id)
            results.append({"task_id": task_id, "state": "invalid", "ok": False, "reason": str(exc)})
    return {"ok": not failures, "command": "audit", "scope": "configured tasks only", "tasks": results, "failed_tasks": failures}


def _command_result(args: argparse.Namespace) -> Dict[str, Any]:
    try:
        root = Path(args.root).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise GateError("--root must name an existing project directory") from exc
    if not root.is_dir():
        raise GateError("--root must name an existing project directory")
    config_rel = _relative_path(args.config, "--config")
    config = _load_config(root, config_rel)
    task_id = args.task
    if task_id is not None:
        task_id = _safe_id(task_id, "task ID")
        if task_id not in config["tasks"]:
            raise GateError(f"unknown task: {task_id}")
    command = args.command
    if command == "plan":
        checks = _selected_checks(config, task_id)
        results = _render_check_results(root, config, checks)
        return {"ok": True, "ready": all(item["decision"] == "reusable" for item in results), "command": command, "task_id": task_id, "checks": results}
    if command == "check":
        checks = _selected_checks(config, task_id)
        results = _render_check_results(root, config, checks)
        return {"ok": all(item["decision"] == "reusable" for item in results), "command": command, "task_id": task_id, "checks": results}
    if command == "run":
        checks = _selected_checks(config, task_id)
        with _lock_context(root, config):
            results = _run_selected(root, config, checks)
        return {"ok": all(item["status"] == "passed" for item in results), "command": command, "task_id": task_id, "checks": results}
    if command == "complete":
        if task_id is None:
            raise GateError("complete requires --task")
        task = config["tasks"][task_id]
        if task["completion"] is None:
            raise GateError(f"task {task_id} has no completion ledger mapping")
        with _lock_context(root, config):
            state, original, original_info = _task_marker_state(root, task_id, task)
            if state == "done":
                proof = _validate_completion_proof(root, config, task_id)
                return {
                    "ok": True,
                    "command": command,
                    "task_id": task_id,
                    "state_before": "done",
                    "state_after": "done",
                    "acceptance": "historical",
                    "current_readiness": "not_evaluated",
                    "ledger_updated": False,
                    "checks": [],
                    "completion_receipt": f"{config['evidence_dir']}/tasks/{task_id}/completions/{proof['completion_id']}/receipt.json",
                    "reason": "existing historical completion proof is intact; current readiness was not evaluated",
                    "guidance": "Use check to assess current readiness; create a new task for new scope or explicitly reopen this ledger row before a new complete.",
                }
            # Invalidate any previous proof before starting a pending/reopened transition.
            # Immutable historical receipts remain, but a failed attempt cannot fall back
            # to them after a concurrent/manual done-marker edit.
            task_base = f"{config['evidence_dir']}/tasks/{task_id}"
            _ensure_directory(root, task_base)
            _atomic_replace(root, f"{task_base}/latest.json", _json_bytes({
                "schema_version": SCHEMA_VERSION,
                "producer": PRODUCER,
                "producer_version": PRODUCER_VERSION,
                "task_id": task_id,
                "status": "in-progress",
                "updated_at": _utc_now(),
            }))
            checks = task["checks"]
            run_results = _run_selected(root, config, checks)
            if any(item["status"] != "passed" for item in run_results):
                return {"ok": False, "command": command, "task_id": task_id, "state_before": state, "ledger_updated": False, "checks": run_results, "reason": "one or more required checks did not pass"}
            references = []
            for check_id in checks:
                evaluation = _evaluate(root, config, check_id)
                if evaluation["decision"] != "reusable":
                    return {"ok": False, "command": command, "task_id": task_id, "state_before": state, "ledger_updated": False, "checks": run_results, "reason": f"check {check_id} became stale before completion"}
                references.append({
                    "check_id": check_id,
                    "run_id": evaluation["run_id"],
                    "receipt_path": _run_receipt_relative(check_id, evaluation["run_id"]),
                    "receipt_sha256": evaluation["receipt_sha256"],
                    "fingerprint": evaluation["fingerprint"],
                })
            completion_path, completion_pointer = _prepare_completion_receipt(root, config, task_id, references)
            _atomic_ledger_update(root, task_id, task, original, original_info)
            # Publish last. A crash/write failure in between leaves audit closed,
            # never a valid proof for an unsuccessful guarded transition.
            _atomic_replace(root, f"{task_base}/latest.json", _json_bytes(completion_pointer))
            return {"ok": True, "command": command, "task_id": task_id, "state_before": state, "state_after": "done", "ledger_updated": state == "pending", "checks": run_results, "completion_receipt": completion_path}
    if command == "audit":
        task_ids = [task_id] if task_id is not None else sorted(config["tasks"])
        return _audit(root, config, task_ids)
    raise GateError(f"unsupported command: {command}")


def _build_parser() -> argparse.ArgumentParser:
    epilog = (
        "Commands and probes come from trusted project configuration; review them before use. "
        "plan/check/audit never run full test commands; configured lightweight probes may run to fingerprint the environment. "
        "Mutating run/complete commands require POSIX fcntl locking (macOS or Linux). "
        "audit validates historical completion proofs for configured tasks only; current-source readiness is checked by check. "
        "The local evidence directory is not a hostile-user security boundary, does not prevent manual file edits, and does not provide CI or branch protection."
    )
    parser = argparse.ArgumentParser(description="Plan, run, check, audit, and guard project task completion.", epilog=epilog)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "run", "check", "complete", "audit"):
        sub = subparsers.add_parser(name, help=f"{name} acceptance checks", description=epilog)
        sub.add_argument("--root", required=True, help="project root directory")
        sub.add_argument("--config", default=DEFAULT_CONFIG, help=f"project-relative config path (default: {DEFAULT_CONFIG})")
        sub.add_argument("--task", help="configured task ID; complete requires it")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = _command_result(args)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result.get("ok", True) else 1
    except GateFailure as exc:
        print(json.dumps({"ok": False, "command": args.command, "error": str(exc), "exit_code": 1}, ensure_ascii=False, sort_keys=True))
        return 1
    except GateError as exc:
        print(json.dumps({"ok": False, "command": args.command, "error": str(exc), "exit_code": 2}, ensure_ascii=False, sort_keys=True))
        return 2
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"ok": False, "command": args.command, "error": f"runtime error: {type(exc).__name__}", "exit_code": 2}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())

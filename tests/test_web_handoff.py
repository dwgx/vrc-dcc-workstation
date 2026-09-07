# -*- coding: utf-8 -*-
"""Offline web handoff validation fixtures.

These tests deliberately exercise the CLI boundary with small files instead of
mocking the file system.  The validator is expected to read only the supplied
bundle and to emit one JSON report for every invocation.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_web_handoff.py"
PY = sys.executable


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _asset(root: Path, name: str, data: bytes) -> dict[str, object]:
    path = root / Path(name)
    _write(path, data)
    return {
        "path": name.replace("\\", "/"),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _bundle(
    root: Path,
    *,
    status: str = "completed",
    task_id: str = "task-1",
    dispatch_id: str = "dispatch-1",
    artifact_class: str = "research",
    include_assets: bool = True,
    include_prompt: bool = True,
    chat_urls: list[str] | None = None,
) -> dict[str, object]:
    assets: list[dict[str, object]] = []
    prompt_data = b"# Prompt\n\nInspect the current documentation.\n"
    if include_assets:
        assets.append(_asset(root, "research.md", b"# Finding\n\nA small cited result.\n"))
    if include_prompt:
        _write(root / "prompts.md", prompt_data)
    if status == "completed":
        _write(root / "REVIEW.md", b"# Review\n\nStructural handoff review is pending owner approval.\n")
        _write(
            root / "STATUS.json",
            (
                json.dumps(
                    {
                        "task_id": task_id,
                        "dispatch_id": dispatch_id,
                        "producer_session": "session-1",
                        "status": status,
                        "next_action": "Owner review remains pending.",
                    },
                    indent=2,
                )
                + "\n"
            ).encode("utf-8"),
        )
    result: dict[str, object] = {
        "schema_version": 1,
        "task_id": task_id,
        "dispatch_id": dispatch_id,
        "artifact_class": artifact_class,
        "status": status,
        "producer_session": "session-1",
        "chat_urls": chat_urls if chat_urls is not None else ["https://chat.example.invalid/task-1"],
        "web_model": {
            "requested": "gpt-6-astra",
            "visible_selection": "Astra",
            "visible_reasoning_setting": "high",
            "observation_time": "2026-09-08T00:00:00Z",
        },
        "actual_prompts_file": "prompts.md" if include_prompt else None,
        "actual_prompts_bytes": len(prompt_data) if include_prompt else None,
        "actual_prompts_sha256": hashlib.sha256(prompt_data).hexdigest() if include_prompt else None,
        "owner_review": "pending",
        "engine_status": "not_tested",
        "assets": assets,
        "blocked_reason": None,
        "next_action": None,
    }
    return result


def _run(root: Path, result: dict[str, object], *, task: str = "task-1", dispatch: str = "dispatch-1", kind: str = "research") -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    result_path = root / "RESULT.json"
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    proc = subprocess.run(
        [
            PY,
            str(CHECKER),
            str(result_path),
            "--root",
            str(root),
            "--task",
            task,
            "--dispatch",
            dispatch,
            "--kind",
            kind,
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:  # make a failed CLI output easy to inspect
        raise AssertionError(f"checker did not emit one JSON report: {proc.stdout!r}; {proc.stderr!r}") from exc
    if not isinstance(report, dict):
        raise AssertionError("checker report must be a JSON object")
    return proc, report


class WebHandoffTests(unittest.TestCase):
    def test_complete_bundle_passes_and_reports_structure_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            proc, report = _run(root, _bundle(root))

            self.assertEqual(proc.returncode, 0)
            self.assertIs(report["ok"], True)
            self.assertEqual(report["status"], "completed")
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["artifact_class"], "research")
            self.assertIs(report["content_or_owner_approval"], False)

    def test_completed_requires_real_producer_and_model_observation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root)
            result["producer_session"] = None
            result["web_model"]["requested"] = None  # type: ignore[index]
            result["web_model"]["visible_selection"] = None  # type: ignore[index]
            result["web_model"]["observation_time"] = None  # type: ignore[index]
            result["web_model"]["visible_reasoning_setting"] = None  # type: ignore[index]
            proc, report = _run(root, result)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("producer_session" in error for error in report["errors"]))
            self.assertTrue(any("web_model.requested" in error for error in report["errors"]))
            self.assertTrue(any("visible_reasoning_setting" in error for error in report["errors"]))

    def test_expected_batch_and_kind_are_trusted_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root, task_id="task-from-result", dispatch_id="dispatch-from-result")
            proc, report = _run(root, result, task="task-from-controller", dispatch="dispatch-from-result", kind="research")

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("task_id" in error for error in report["errors"]))

            result = _bundle(root, task_id="task-1", dispatch_id="dispatch-1", artifact_class="model_reference")
            proc, report = _run(root, result, kind="research")
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("artifact_class" in error for error in report["errors"]))

    def test_completed_requires_nonempty_assets_and_prompts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root)
            empty = _asset(root, "research.md", b"")
            result["assets"] = [empty]
            proc, report = _run(root, result)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("non-empty" in error for error in report["errors"]))

            result = _bundle(root, include_assets=True, include_prompt=False)
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("actual_prompts_file" in error for error in report["errors"]))

    def test_tampering_is_caught_from_streamed_bytes_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root)
            _write(root / "research.md", b"tampered\n")
            proc, report = _run(root, result)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("sha256" in error or "bytes" in error for error in report["errors"]))
            self.assertEqual(report["verified_assets"], [])
            self.assertTrue(any("observed" in error for error in report["errors"]))

    def test_prompt_tampering_is_caught_from_streamed_bytes_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root)
            _write(root / "prompts.md", b"tampered prompt\n")
            proc, report = _run(root, result)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("actual_prompts_bytes" in error for error in report["errors"]))
            self.assertTrue(any("actual_prompts_sha256" in error for error in report["errors"]))

    def test_parent_escape_and_symlink_escape_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as parent_temp:
            parent = Path(parent_temp)
            root = parent / "bundle"
            outside = parent / "outside.txt"
            _write(outside, b"outside\n")
            result = _bundle(root, include_assets=False)
            result["assets"] = [{"path": "../web-handoff-outside.txt", "bytes": 8, "sha256": hashlib.sha256(b"outside\n").hexdigest()}]
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("root" in error or "relative" in error for error in report["errors"]))

            link = root / "escape.md"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable on this Windows runner")
            result = _bundle(root, include_assets=False)
            result["assets"] = [{"path": "escape.md", "bytes": outside.stat().st_size, "sha256": hashlib.sha256(outside.read_bytes()).hexdigest()}]
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("root" in error or "symlink" in error for error in report["errors"]))

    def test_unicode_asset_path_is_safe_in_single_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root, include_assets=False)
            result["assets"] = [_asset(root, "研究.md", "研究结果\n".encode("utf-8"))]
            proc, report = _run(root, result)

            self.assertEqual(proc.returncode, 0)
            self.assertIs(report["ok"], True)
            proc.stdout.encode("ascii")

    def test_completed_requires_root_receipts_and_matching_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root)
            (root / "REVIEW.md").unlink()
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("REVIEW.md" in error for error in report["errors"]))

            result = _bundle(root)
            status_data = json.loads((root / "STATUS.json").read_text(encoding="utf-8"))
            status_data["dispatch_id"] = "wrong-dispatch"
            (root / "STATUS.json").write_text(json.dumps(status_data) + "\n", encoding="utf-8")
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("STATUS.json.dispatch_id" in error for error in report["errors"]))

            result = _bundle(root)
            (root / "STATUS.json").write_text("{not json\n", encoding="utf-8")
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("STATUS.json is not valid JSON" in error for error in report["errors"]))

    def test_result_manifest_must_be_inside_bundle_root(self) -> None:
        with tempfile.TemporaryDirectory() as parent_temp:
            parent = Path(parent_temp)
            root = parent / "bundle"
            result = _bundle(root)
            external = parent / "RESULT.json"
            external.write_text(json.dumps(result) + "\n", encoding="utf-8")
            proc = subprocess.run(
                [PY, str(CHECKER), str(external), "--root", str(root), "--task", "task-1", "--dispatch", "dispatch-1", "--kind", "research"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            report = json.loads(proc.stdout)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("inside the allowed root" in error for error in report["errors"]))

    def test_duplicate_assets_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root)
            assets = result["assets"]
            assert isinstance(assets, list)
            result["assets"] = [assets[0], assets[0]]
            proc, report = _run(root, result)

            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("duplicate" in error for error in report["errors"]))

    def test_incomplete_status_never_reports_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root, status="partial", include_assets=False, include_prompt=False, chat_urls=[])
            proc, report = _run(root, result)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertEqual(report["status"], "partial")
            self.assertTrue(any("completed" in error for error in report["errors"]))

    def test_bad_json_and_bad_types_are_readable_nonzero_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bad_json = root / "bad.json"
            bad_json.write_text("{ definitely not json", encoding="utf-8")
            proc = subprocess.run(
                [PY, str(CHECKER), str(bad_json), "--root", str(root), "--task", "task-1", "--dispatch", "dispatch-1", "--kind", "research"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            report = json.loads(proc.stdout)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertEqual(report["status"], "error")
            self.assertNotIn("Traceback", proc.stdout + proc.stderr)

            result = _bundle(root)
            assets = result["assets"]
            assert isinstance(assets, list)
            assets[0]["bytes"] = True
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            self.assertTrue(any("integer" in error or "bytes" in error for error in report["errors"]))

    def test_windows_absolute_drive_and_unc_paths_are_not_relative(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = _bundle(root, include_assets=False)
            result["assets"] = [{"path": r"C:\outside.md", "bytes": 1, "sha256": "0" * 64}]
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("relative" in error or "drive" in error for error in report["errors"]))

            result["assets"] = [{"path": r"\\server\share\outside.md", "bytes": 1, "sha256": "0" * 64}]
            proc, report = _run(root, result)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("relative" in error or "UNC" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()

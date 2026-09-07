#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a bounded, offline web-research artifact handoff.

The checker is intentionally narrow.  It reads the supplied RESULT.json and
files below ``--root``; it never executes a producer, downloads a URL, writes
the bundle, or treats this structural check as content, pixel, Unity, or owner
approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import ntpath
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterable
from urllib.parse import urlsplit


SCHEMA_VERSION = 1
KINDS = frozenset({"research", "design_reference", "base_color_candidate", "model_reference"})
STATUSES = frozenset({"completed", "partial", "blocked_external", "running"})
WEB_MODEL_FIELDS = (
    "requested",
    "visible_selection",
    "visible_reasoning_setting",
    "observation_time",
)
TOP_LEVEL_FIELDS = (
    "schema_version",
    "task_id",
    "dispatch_id",
    "artifact_class",
    "status",
    "producer_session",
    "chat_urls",
    "web_model",
    "actual_prompts_file",
    "actual_prompts_bytes",
    "actual_prompts_sha256",
    "owner_review",
    "engine_status",
    "assets",
    "blocked_reason",
    "next_action",
)
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
CHUNK_SIZE = 1024 * 1024


class _CliError(Exception):
    """An expected command-line error that should become a JSON report."""


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise _CliError(message)


def _is_string(value: Any, *, nonempty: bool = False) -> bool:
    return isinstance(value, str) and (not nonempty or bool(value.strip()))


def _is_optional_string(value: Any) -> bool:
    return value is None or isinstance(value, str)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON number: {value}")


def _load_json(result_path: Path) -> Any:
    with result_path.open("r", encoding="utf-8-sig") as stream:
        return json.load(
            stream,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )


def _error_report(message: str, *, status: str = "error") -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "errors": [message],
        "warnings": [],
        "verified_assets": [],
        "content_or_owner_approval": False,
        "scope": "structural file and hash checks only",
        "limitations": [
            "This report does not establish research citation correctness.",
            "This report does not inspect image dimensions, format, or pixels.",
            "This report does not test a model UI, Unity import, engine, or owner review.",
        ],
    }


def _base_report(result: dict[str, Any]) -> dict[str, Any]:
    status = result.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        status = "error"
    return {
        "ok": False,
        "status": status,
        "schema_version": result.get("schema_version"),
        "task_id": result.get("task_id"),
        "dispatch_id": result.get("dispatch_id"),
        "artifact_class": result.get("artifact_class"),
        "errors": [],
        "warnings": [],
        "verified_assets": [],
        "content_or_owner_approval": False,
        "scope": "structural file and hash checks only",
        "limitations": [
            "This report does not establish research citation correctness.",
            "This report does not inspect image dimensions, format, or pixels.",
            "This report does not test a model UI, Unity import, engine, or owner review.",
        ],
    }


def _validate_relative_file(root: Path, raw: Any, label: str) -> tuple[Path | None, str | None]:
    """Resolve one untrusted member path and keep it below the resolved root."""
    if not _is_string(raw, nonempty=True):
        return None, f"{label} must be a non-empty relative path"
    assert isinstance(raw, str)
    if "\x00" in raw:
        return None, f"{label} contains a NUL byte"

    # pathlib on POSIX does not regard a Windows drive or UNC path as absolute;
    # reject both syntaxes explicitly so the same RESULT.json is safe on either
    # host.  A drive-relative path such as C:foo is also not a bundle member.
    windows_form = raw.replace("/", "\\")
    drive, _ = ntpath.splitdrive(windows_form)
    if drive:
        return None, f"{label} must be relative; drive/UNC path is forbidden"
    if ntpath.isabs(windows_form) or Path(raw).is_absolute():
        return None, f"{label} must be relative; absolute/UNC path is forbidden"

    # Parent components are rejected even when they would normalize back inside
    # root.  This makes the manifest auditable and removes platform-specific
    # ambiguity around separators.
    components = [part for part in re.split(r"[\\/]+", raw) if part]
    if ".." in components:
        return None, f"{label} contains a parent (..) component and is not a permitted root-relative path"

    candidate_unresolved = root / Path(raw)
    try:
        candidate = candidate_unresolved.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        return None, f"{label} cannot be resolved below root: {exc}"

    try:
        candidate.relative_to(root)
    except ValueError:
        return None, f"{label} resolves outside the allowed root (symlink escape)"
    if not candidate.is_file():
        return None, f"{label} must identify a regular file"
    return candidate, None


def _stream_file(path: Path, *, hash_file: bool) -> tuple[int, str | None]:
    """Read once, counting bytes and optionally hashing that exact stream."""
    digest = hashlib.sha256() if hash_file else None
    count = 0
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(CHUNK_SIZE)
            if not chunk:
                break
            count += len(chunk)
            if digest is not None:
                digest.update(chunk)
    return count, digest.hexdigest() if digest is not None else None


def _resolve_result_path(root: Path, raw: str) -> Path:
    """Resolve RESULT.json and require the manifest itself to be in root."""
    try:
        candidate = Path(raw).resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        raise _CliError(f"RESULT.json cannot be resolved: {exc}") from None
    if not candidate.is_file():
        raise _CliError("RESULT.json must identify a regular file")
    try:
        candidate.relative_to(root)
    except ValueError:
        raise _CliError("RESULT.json must resolve inside the allowed root") from None
    return candidate


def _validate_completed_receipts(root: Path, result: dict[str, Any], errors: list[str]) -> None:
    """Require the two human/recovery receipts at the bundle root."""
    review_path, review_error = _validate_relative_file(root, "REVIEW.md", "REVIEW.md")
    if review_error:
        errors.append("completed results require " + review_error)
    elif review_path is not None:
        try:
            review_bytes, _ = _stream_file(review_path, hash_file=False)
        except OSError as exc:
            errors.append(f"REVIEW.md cannot be read: {exc}")
        else:
            if review_bytes == 0:
                errors.append("completed results require a non-empty REVIEW.md")

    status_path, status_error = _validate_relative_file(root, "STATUS.json", "STATUS.json")
    if status_error:
        errors.append("completed results require " + status_error)
        return
    if status_path is None:
        return
    try:
        status_bytes, _ = _stream_file(status_path, hash_file=False)
    except OSError as exc:
        errors.append(f"STATUS.json cannot be read: {exc}")
        return
    if status_bytes == 0:
        errors.append("completed results require a non-empty STATUS.json")
        return
    try:
        status_result = _load_json(status_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"STATUS.json is not valid JSON: {exc}")
        return
    if not isinstance(status_result, dict):
        errors.append("STATUS.json must contain a JSON object")
        return
    for field in ("task_id", "dispatch_id", "producer_session", "status"):
        value = status_result.get(field)
        expected = result.get(field)
        if field not in status_result:
            errors.append(f"STATUS.json missing required field: {field}")
        elif not _is_string(value, nonempty=True):
            errors.append(f"STATUS.json.{field} must be a non-empty string")
        elif value != expected:
            errors.append(f"STATUS.json.{field} does not match RESULT.json")


def _validate_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _validate_result(result: Any, root: Path, task: str, dispatch: str, kind: str) -> dict[str, Any]:
    if not isinstance(result, dict):
        return _error_report("RESULT.json top level must be a JSON object")

    report = _base_report(result)
    errors: list[str] = report["errors"]

    missing = [field for field in TOP_LEVEL_FIELDS if field not in result]
    if missing:
        errors.append("missing required field(s): " + ", ".join(missing))

    unknown = sorted(set(result) - set(TOP_LEVEL_FIELDS))
    if unknown:
        errors.append("unknown top-level field(s): " + ", ".join(map(str, unknown)))

    schema_version = result.get("schema_version")
    if type(schema_version) is not int or schema_version != SCHEMA_VERSION:
        errors.append("schema_version must be integer 1 (boolean is not an integer)")

    for field, expected in (("task_id", task), ("dispatch_id", dispatch)):
        value = result.get(field)
        if not _is_string(value, nonempty=True):
            errors.append(f"{field} must be a non-empty string")
        elif value != expected:
            errors.append(f"{field} does not match the controller expectation")

    artifact_class = result.get("artifact_class")
    if not _is_string(artifact_class, nonempty=True):
        errors.append("artifact_class must be a non-empty string")
    elif artifact_class != kind:
        errors.append("artifact_class does not match the controller kind")

    status = result.get("status")
    if not _is_string(status, nonempty=True):
        errors.append("status must be one of completed, partial, blocked_external, running")
    elif status not in STATUSES:
        errors.append("status must be one of completed, partial, blocked_external, running")
    elif status != "completed":
        errors.append(f"status is {status}; only completed results can pass")

    producer_session = result.get("producer_session")
    if not _is_optional_string(producer_session):
        errors.append("producer_session must be a string or null")
    elif status == "completed" and not _is_string(producer_session, nonempty=True):
        errors.append("completed results require a non-empty producer_session")

    urls = result.get("chat_urls")
    if not isinstance(urls, list):
        errors.append("chat_urls must be an array of HTTP(S) URL strings")
        urls = []
    else:
        seen_urls: set[str] = set()
        for index, url in enumerate(urls):
            if not _is_string(url, nonempty=True):
                errors.append(f"chat_urls[{index}] must be a non-empty string")
                continue
            assert isinstance(url, str)
            if not _validate_url(url):
                errors.append(f"chat_urls[{index}] must be an absolute http(s) URL")
            if url in seen_urls:
                errors.append(f"chat_urls[{index}] is a duplicate URL")
            seen_urls.add(url)
        if status == "completed" and not urls:
            errors.append("completed results require at least one chat URL")

    web_model = result.get("web_model")
    if not isinstance(web_model, dict):
        errors.append("web_model must be an object")
    else:
        missing_model = [field for field in WEB_MODEL_FIELDS if field not in web_model]
        if missing_model:
            errors.append("web_model missing required field(s): " + ", ".join(missing_model))
        unknown_model = sorted(set(web_model) - set(WEB_MODEL_FIELDS))
        if unknown_model:
            errors.append("unknown web_model field(s): " + ", ".join(map(str, unknown_model)))
        for field in WEB_MODEL_FIELDS:
            if field in web_model and not _is_optional_string(web_model[field]):
                errors.append(f"web_model.{field} must be a string or null")
            elif status == "completed" and field in {"requested", "visible_selection", "observation_time"} and not _is_string(web_model.get(field), nonempty=True):
                errors.append(f"completed results require a non-empty web_model.{field}")
            elif status == "completed" and field == "visible_reasoning_setting" and not _is_string(web_model.get(field), nonempty=True):
                errors.append("completed results require web_model.visible_reasoning_setting (use 'not_visible' when it was not shown)")

    owner_review = result.get("owner_review")
    if owner_review != "pending":
        errors.append("owner_review must remain pending")
    engine_status = result.get("engine_status")
    if engine_status != "not_tested":
        errors.append("engine_status must remain not_tested")
    for field in ("blocked_reason", "next_action"):
        if not _is_optional_string(result.get(field)):
            errors.append(f"{field} must be a string or null")

    prompt_claimed_bytes = result.get("actual_prompts_bytes")
    if prompt_claimed_bytes is not None and (type(prompt_claimed_bytes) is not int or prompt_claimed_bytes < 0):
        errors.append("actual_prompts_bytes must be a non-negative integer or null (boolean is not an integer)")
    if status == "completed" and (type(prompt_claimed_bytes) is not int or prompt_claimed_bytes < 0):
        errors.append("completed results require actual_prompts_bytes")
    prompt_claimed_hash = result.get("actual_prompts_sha256")
    if prompt_claimed_hash is not None and (not _is_string(prompt_claimed_hash, nonempty=True) or not SHA256_RE.fullmatch(prompt_claimed_hash)):
        errors.append("actual_prompts_sha256 must be a 64-character hexadecimal string or null")
    if status == "completed" and (not isinstance(prompt_claimed_hash, str) or not SHA256_RE.fullmatch(prompt_claimed_hash)):
        errors.append("completed results require actual_prompts_sha256")

    assets = result.get("assets")
    if not isinstance(assets, list):
        errors.append("assets must be an array")
        assets = []
    if status == "completed" and not assets:
        errors.append("completed results require at least one asset")

    seen_paths: set[str] = set()
    verified_assets: list[dict[str, Any]] = report["verified_assets"]
    research_markdown = False
    for index, asset in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{label} must be an object")
            continue
        required_asset = ("path", "bytes", "sha256")
        missing_asset = [field for field in required_asset if field not in asset]
        if missing_asset:
            errors.append(f"{label} missing required field(s): " + ", ".join(missing_asset))
            continue
        asset_path = asset.get("path")
        expected_bytes = asset.get("bytes")
        expected_hash = asset.get("sha256")
        if type(expected_bytes) is not int or expected_bytes < 0:
            errors.append(f"{label}.bytes must be a non-negative integer (boolean is not an integer)")
        if not _is_string(expected_hash, nonempty=True) or not SHA256_RE.fullmatch(expected_hash):
            errors.append(f"{label}.sha256 must be a 64-character hexadecimal string")
        resolved, path_error = _validate_relative_file(root, asset_path, f"{label}.path")
        if path_error:
            errors.append(path_error)
            continue
        assert resolved is not None
        key = os.path.normcase(os.fspath(resolved))
        if key in seen_paths:
            errors.append(f"{label}.path is a duplicate asset")
            continue
        seen_paths.add(key)
        if isinstance(asset_path, str) and asset_path.lower().endswith(".md"):
            research_markdown = True
        try:
            actual_bytes, actual_hash = _stream_file(resolved, hash_file=True)
        except OSError as exc:
            errors.append(f"{label}.path cannot be read: {exc}")
            continue
        bytes_match = type(expected_bytes) is int and expected_bytes == actual_bytes
        hash_match = isinstance(expected_hash, str) and SHA256_RE.fullmatch(expected_hash) and expected_hash.lower() == actual_hash
        if not bytes_match:
            errors.append(f"{label}.bytes does not match the streamed file byte count (claimed {expected_bytes!r}, observed {actual_bytes})")
        if not hash_match:
            errors.append(f"{label}.sha256 does not match the streamed file hash (claimed {expected_hash!r}, observed {actual_hash})")
        if bytes_match and hash_match:
            verified_assets.append({"path": asset_path, "bytes": actual_bytes, "sha256": actual_hash})
        if status == "completed" and actual_bytes == 0:
            errors.append(f"{label} must reference a non-empty file for completed status")

    actual_prompts_file = result.get("actual_prompts_file")
    if actual_prompts_file is not None or status == "completed":
        resolved_prompt, prompt_error = _validate_relative_file(root, actual_prompts_file, "actual_prompts_file")
        if prompt_error:
            errors.append(prompt_error)
        elif resolved_prompt is not None:
            try:
                prompt_bytes, prompt_hash = _stream_file(resolved_prompt, hash_file=True)
            except OSError as exc:
                errors.append(f"actual_prompts_file cannot be read: {exc}")
            else:
                if prompt_bytes == 0:
                    errors.append("actual_prompts_file must be non-empty for a completed handoff")
                bytes_match = type(prompt_claimed_bytes) is int and prompt_claimed_bytes == prompt_bytes
                hash_match = isinstance(prompt_claimed_hash, str) and SHA256_RE.fullmatch(prompt_claimed_hash) and prompt_claimed_hash.lower() == prompt_hash
                if not bytes_match:
                    errors.append(f"actual_prompts_bytes does not match the streamed prompt byte count (claimed {prompt_claimed_bytes!r}, observed {prompt_bytes})")
                if not hash_match:
                    errors.append(f"actual_prompts_sha256 does not match the streamed prompt hash (claimed {prompt_claimed_hash!r}, observed {prompt_hash})")

    if status == "completed" and kind == "research" and not research_markdown:
        errors.append("completed research results require a non-empty Markdown asset")
    if status == "completed":
        _validate_completed_receipts(root, result, errors)

    report["ok"] = not errors and status == "completed"
    return report


def _make_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(
        prog="check_web_handoff.py",
        description="Validate an offline web handoff bundle without executing or downloading anything.",
    )
    parser.add_argument("result", metavar="RESULT.json", help="result manifest to inspect")
    parser.add_argument("--root", required=True, help="allowed artifact bundle root")
    parser.add_argument("--task", required=True, help="controller-trusted expected task id")
    parser.add_argument("--dispatch", required=True, help="controller-trusted expected dispatch id")
    parser.add_argument("--kind", required=True, choices=sorted(KINDS), help="controller-trusted expected artifact class")
    return parser


def _resolve_root(raw: str) -> Path:
    if not _is_string(raw, nonempty=True):
        raise _CliError("--root must be a non-empty directory path")
    try:
        root = Path(raw).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise _CliError(f"--root cannot be resolved: {exc}") from None
    if not root.is_dir():
        raise _CliError("--root must identify a directory")
    return root


def _emit(report: dict[str, Any]) -> None:
    # Escape non-ASCII so a Windows console using a legacy code page cannot
    # turn a valid report (for example, a Japanese asset path) into a traceback.
    json.dump(report, sys.stdout, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


def main(argv: Iterable[str] | None = None) -> int:
    try:
        args = _make_parser().parse_args(list(argv) if argv is not None else None)
        root = _resolve_root(args.root)
        try:
            result_path = _resolve_result_path(root, args.result)
        except _CliError as exc:
            _emit(_error_report(str(exc)))
            return 1
        try:
            result = _load_json(result_path)
        except FileNotFoundError:
            _emit(_error_report("RESULT.json was not found"))
            return 1
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            _emit(_error_report(f"RESULT.json could not be read as valid JSON: {exc}"))
            return 1
        report = _validate_result(result, root, args.task, args.dispatch, args.kind)
        _emit(report)
        return 0 if report["ok"] else 1
    except _CliError as exc:
        _emit(_error_report(f"command line error: {exc}"))
        return 2
    except Exception as exc:  # no traceback should escape this offline checker
        _emit(_error_report(f"validator error: {type(exc).__name__}: {exc}"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only, byte-consistent image inspection for explicit input files.

The command reads each named file once into an immutable byte snapshot.  The
SHA-256 digest, byte count, Pillow verification, and Pillow load all describe
that same snapshot.  It never walks directories, writes an input, or creates a
preview.  A successful report is a file/decode observation only; it says
nothing about atlases, PBR suitability, seamless tiling, or an engine import.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable
import warnings


try:
    import PIL
    from PIL import Image, ImageFile
except ImportError as exc:  # dependency errors are reported as JSON by main()
    PIL = None  # type: ignore[assignment]
    Image = None  # type: ignore[assignment]
    ImageFile = None  # type: ignore[assignment]
    _PIL_IMPORT_ERROR: Exception | None = exc
else:
    _PIL_IMPORT_ERROR = None


FRAME_SCOPES = ("first", "all")
SIZE_RE = re.compile(r"^(\d+)[xX](\d+)$")
LIMITATIONS = [
    "Pillow verify() and load() are decoder observations; success does not prove every container byte, trailer, or CRC is intact.",
    "Pillow may tolerate trailing bytes or small tail truncation; this tool does not certify strict full-file container integrity.",
    "No custom PNG, GIF, JPEG, or other container parser is used.",
    "This is a file and decode observation only; it does not establish atlas, PBR, seamless-tiling, or engine suitability.",
    "Only the requested frame scope is decoded; an explicit first-frame scope does not certify other frames.",
]
VALIDATION_OPERATIONS = [
    "read one immutable in-memory byte snapshot",
    "Pillow Image.open followed by verify",
    "fresh Pillow Image.open followed by load for the requested frame scope",
]


class _CliError(Exception):
    """An expected CLI error that should be returned as one JSON report."""


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise _CliError(message)


@contextmanager
def _strict_truncated_images() -> Iterable[None]:
    """Keep Pillow's truncated-image behavior strict during this inspection."""
    if ImageFile is None:
        yield
        return
    previous = ImageFile.LOAD_TRUNCATED_IMAGES
    ImageFile.LOAD_TRUNCATED_IMAGES = False
    try:
        yield
    finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = previous


def _describe_exception(exc: Exception) -> str:
    text = str(exc).strip()
    return f"{type(exc).__name__}: {text}" if text else type(exc).__name__


def _empty_transparency() -> dict[str, Any]:
    return {
        "channel_or_metadata_present": None,
        "kind": None,
        "alpha_band": None,
        "metadata": False,
        "pixel_transparency_observed": None,
    }


def _empty_record(path: Path, frame_scope: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "filename_extension": path.suffix.lower().lstrip(".") or None,
        "bytes": None,
        "sha256": None,
        "format": None,
        "width": None,
        "height": None,
        "mode": None,
        "bands": [],
        "transparency": _empty_transparency(),
        "frame_check": {
            "scope": frame_scope,
            "frame_count": None,
            "frames_checked": [],
            "complete": False,
        },
        "decode": {
            "verify": False,
            "load": False,
        },
        "snapshot": "single_in_memory_read",
        "warnings": [],
        "errors": [],
        "ok": False,
    }


def _metadata_from_image(image: Any) -> dict[str, Any]:
    bands = list(image.getbands())
    alpha_band = next((band for band in bands if band in {"A", "a"}), None)
    has_transparency_metadata = "transparency" in image.info
    has_transparency = bool(alpha_band or has_transparency_metadata)
    if alpha_band == "a":
        transparency_kind = "premultiplied_alpha_channel"
    elif alpha_band:
        transparency_kind = "alpha_channel"
    elif has_transparency_metadata:
        transparency_kind = "transparency_metadata"
    else:
        transparency_kind = "none"
    frame_count = getattr(image, "n_frames", 1)
    if type(frame_count) is not int or frame_count < 1:
        frame_count = 1
    return {
        "format": image.format,
        "width": int(image.size[0]),
        "height": int(image.size[1]),
        "mode": image.mode,
        "bands": bands,
        "transparency": {
            "channel_or_metadata_present": has_transparency,
            "kind": transparency_kind,
            "alpha_band": alpha_band,
            "metadata": has_transparency_metadata,
            "pixel_transparency_observed": None,
        },
        "frame_count": frame_count,
    }


def _parse_expected_size(value: str | None) -> tuple[int, int] | None:
    if value is None:
        return None
    match = SIZE_RE.fullmatch(value.strip())
    if match is None:
        raise _CliError("--expect-size must use WIDTHxHEIGHT with positive integers")
    width, height = int(match.group(1)), int(match.group(2))
    if width < 1 or height < 1:
        raise _CliError("--expect-size must use positive WIDTH and HEIGHT")
    return width, height


def _inspect_one(
    raw_path: str,
    *,
    expected_size: tuple[int, int] | None,
    expected_format: str | None,
    frame_scope: str,
) -> dict[str, Any]:
    path = Path(raw_path)
    record = _empty_record(path, frame_scope)
    errors: list[str] = record["errors"]
    try:
        snapshot = path.read_bytes()
    except OSError as exc:
        errors.append(f"input cannot be read: {_describe_exception(exc)}")
        return record

    record["bytes"] = len(snapshot)
    record["sha256"] = hashlib.sha256(snapshot).hexdigest()
    observed_frame_count: int | None = None
    warnings_seen: list[str] = record["warnings"]

    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.simplefilter("always")
        with _strict_truncated_images():
            # This first open reads metadata only.  It is deliberately followed
            # by verify() and a fresh open/load below; Image.open is lazy.
            try:
                with Image.open(io.BytesIO(snapshot)) as image:  # type: ignore[union-attr]
                    metadata = _metadata_from_image(image)
                record["format"] = metadata["format"]
                record["width"] = metadata["width"]
                record["height"] = metadata["height"]
                record["mode"] = metadata["mode"]
                record["bands"] = metadata["bands"]
                record["transparency"] = metadata["transparency"]
                observed_frame_count = metadata["frame_count"]
                record["frame_check"]["frame_count"] = observed_frame_count
            except Exception as exc:
                errors.append(f"metadata read failed: {_describe_exception(exc)}")

            try:
                with Image.open(io.BytesIO(snapshot)) as image:  # type: ignore[union-attr]
                    image.verify()
                record["decode"]["verify"] = True
            except Exception as exc:
                errors.append(f"verify failed: {_describe_exception(exc)}")

            if record["decode"]["verify"]:
                frame_count = observed_frame_count or 1
                frames_checked = list(range(frame_count)) if frame_scope == "all" else [0]
                try:
                    with Image.open(io.BytesIO(snapshot)) as image:  # type: ignore[union-attr]
                        for frame_index in frames_checked:
                            image.seek(frame_index)
                            image.load()
                    record["decode"]["load"] = True
                    record["frame_check"]["frames_checked"] = frames_checked
                    record["frame_check"]["complete"] = frames_checked == list(range(frame_count))
                except Exception as exc:
                    errors.append(f"load failed for frame scope {frame_scope!r}: {_describe_exception(exc)}")

        for captured in captured_warnings:
            warnings_seen.append(f"{captured.category.__name__}: {captured.message}")

    actual_format = record["format"]
    if expected_format is not None and actual_format != expected_format:
        errors.append(f"expect-format mismatch: expected {expected_format}, observed {actual_format}")
    if expected_size is not None:
        observed_size = (record["width"], record["height"])
        if observed_size != expected_size:
            errors.append(f"expect-size mismatch: expected {expected_size[0]}x{expected_size[1]}, observed {record['width']}x{record['height']}")
    record["ok"] = not errors and record["decode"]["verify"] and record["decode"]["load"]
    return record


def _make_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(
        prog="inspect_image_assets.py",
        description="Read-only Pillow verification for explicitly named image files.",
    )
    parser.add_argument("files", metavar="FILE", nargs="+", help="image file(s) to inspect; directories are never scanned")
    parser.add_argument("--expect-size", metavar="WIDTHxHEIGHT", help="require the observed dimensions")
    parser.add_argument("--expect-format", metavar="FORMAT", help="require the observed Pillow format, for example PNG or JPEG")
    parser.add_argument("--frames", choices=FRAME_SCOPES, default="first", help="decode the first frame (default) or every frame")
    return parser


def _base_report(*, expected_size: tuple[int, int] | None, expected_format: str | None, frame_scope: str) -> dict[str, Any]:
    return {
        "ok": False,
        "pillow_version": getattr(PIL, "__version__", None),
        "validation_method": {
            "library": "Pillow",
            "operations": VALIDATION_OPERATIONS,
            "frame_scope": frame_scope,
            "result_scope": "decoder_observation_only",
            "strict_full_file_integrity": False,
        },
        "expectations": {
            "size": list(expected_size) if expected_size is not None else None,
            "format": expected_format,
            "frames": frame_scope,
        },
        "files": [],
        "errors": [],
        "limitations": LIMITATIONS,
    }


def _emit(report: dict[str, Any]) -> None:
    # ASCII escaping keeps JSON safe when stdout uses a legacy Windows code page.
    json.dump(report, sys.stdout, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


def main(argv: Iterable[str] | None = None) -> int:
    try:
        args = _make_parser().parse_args(list(argv) if argv is not None else None)
        expected_size = _parse_expected_size(args.expect_size)
        expected_format = args.expect_format.strip().upper() if args.expect_format is not None else None
        if expected_format == "":
            raise _CliError("--expect-format must be a non-empty format name")
        report = _base_report(expected_size=expected_size, expected_format=expected_format, frame_scope=args.frames)
        if _PIL_IMPORT_ERROR is not None:
            report["errors"].append(
                "Pillow is unavailable; install the pinned dependency with "
                "'python -m pip install -r scripts/requirements-images.txt' "
                f"({_describe_exception(_PIL_IMPORT_ERROR)})"
            )
            _emit(report)
            return 2

        for raw_path in args.files:
            record = _inspect_one(
                raw_path,
                expected_size=expected_size,
                expected_format=expected_format,
                frame_scope=args.frames,
            )
            report["files"].append(record)
            for error in record["errors"]:
                report["errors"].append(f"{record['path']}: {error}")
        report["ok"] = bool(report["files"]) and all(record["ok"] for record in report["files"])
        _emit(report)
        return 0 if report["ok"] else 1
    except _CliError as exc:
        _emit({
            "ok": False,
            "pillow_version": getattr(PIL, "__version__", None),
            "validation_method": {
                "library": "Pillow",
                "operations": VALIDATION_OPERATIONS,
                "frame_scope": None,
                "result_scope": "decoder_observation_only",
                "strict_full_file_integrity": False,
            },
            "expectations": {},
            "files": [],
            "errors": [f"command line error: {exc}"],
            "limitations": LIMITATIONS,
        })
        return 2
    except Exception as exc:  # keep malformed input and dependency failures traceback-free
        _emit({
            "ok": False,
            "pillow_version": getattr(PIL, "__version__", None),
            "validation_method": {
                "library": "Pillow",
                "operations": VALIDATION_OPERATIONS,
                "frame_scope": None,
                "result_scope": "decoder_observation_only",
                "strict_full_file_integrity": False,
            },
            "expectations": {},
            "files": [],
            "errors": [f"inspector error: {_describe_exception(exc)}"],
            "limitations": LIMITATIONS,
        })
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

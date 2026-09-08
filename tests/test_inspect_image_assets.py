# -*- coding: utf-8 -*-
"""CLI fixtures for the read-only Pillow image inspector."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "inspect_image_assets.py"
PY = sys.executable


def _save(path: Path, *, image_format: str, mode: str = "RGB", size: tuple[int, int] = (4, 3)) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new(mode, size, color=(12, 34, 56, 128) if mode == "RGBA" else (12, 34, 56))
    try:
        image.save(path, format=image_format)
    finally:
        image.close()
    return path.read_bytes()


def _run(*paths: Path, expect_size: str | None = None, expect_format: str | None = None, frames: str | None = None) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    command = [PY, str(CHECKER), *(str(path) for path in paths)]
    if expect_size is not None:
        command.extend(["--expect-size", expect_size])
    if expect_format is not None:
        command.extend(["--expect-format", expect_format])
    if frames is not None:
        command.extend(["--frames", frames])
    proc = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"inspector did not emit one JSON report: {proc.stdout!r}; {proc.stderr!r}") from exc
    if not isinstance(report, dict):
        raise AssertionError("inspector report must be a JSON object")
    return proc, report


class InspectImageAssetsTests(unittest.TestCase):
    def test_png_metadata_uses_real_format_and_reports_alpha(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "looks-like-jpeg.jpg"
            raw = _save(path, image_format="PNG", mode="RGBA", size=(3, 2))
            proc, report = _run(path, expect_size="3x2", expect_format="png")

            self.assertEqual(proc.returncode, 0)
            self.assertEqual(proc.stderr, "")
            self.assertIs(report["ok"], True)
            self.assertEqual(len(report["files"]), 1)
            observed = report["files"][0]
            self.assertEqual(observed["format"], "PNG")
            self.assertEqual(observed["filename_extension"], "jpg")
            self.assertEqual(observed["width"], 3)
            self.assertEqual(observed["height"], 2)
            self.assertEqual(observed["mode"], "RGBA")
            self.assertEqual(observed["bands"], ["R", "G", "B", "A"])
            self.assertEqual(observed["transparency"]["channel_or_metadata_present"], True)
            self.assertEqual(observed["transparency"]["alpha_band"], "A")
            self.assertIsNone(observed["transparency"]["pixel_transparency_observed"])
            self.assertEqual(observed["bytes"], len(raw))
            self.assertEqual(observed["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(observed["decode"]["verify"], True)
            self.assertEqual(observed["decode"]["load"], True)
            self.assertEqual(observed["frame_check"]["frames_checked"], [0])

    def test_jpeg_metadata_is_real_even_when_extension_is_png(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "photo.png"
            _save(path, image_format="JPEG", mode="RGB", size=(5, 4))
            proc, report = _run(path, expect_size="5x4", expect_format="JPEG")

            self.assertEqual(proc.returncode, 0)
            observed = report["files"][0]
            self.assertEqual(observed["format"], "JPEG")
            self.assertEqual(observed["mode"], "RGB")
            self.assertEqual(observed["bands"], ["R", "G", "B"])
            self.assertEqual(observed["transparency"]["channel_or_metadata_present"], False)

    def test_opaque_rgba_reports_channel_presence_without_pixel_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "opaque-alpha.png"
            image = Image.new("RGBA", (2, 2), (10, 20, 30, 255))
            try:
                image.save(path, format="PNG")
            finally:
                image.close()
            proc, report = _run(path)

            self.assertEqual(proc.returncode, 0)
            transparency = report["files"][0]["transparency"]
            self.assertTrue(transparency["channel_or_metadata_present"])
            self.assertEqual(transparency["kind"], "alpha_channel")
            self.assertIsNone(transparency["pixel_transparency_observed"])

    def test_truncated_file_fails_after_verify_or_load_with_observation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "truncated.png"
            raw = _save(path, image_format="PNG", mode="RGB", size=(8, 7))
            path.write_bytes(raw[:-12])
            truncated = path.read_bytes()
            proc, report = _run(path)

            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(proc.stderr, "")
            self.assertIs(report["ok"], False)
            observed = report["files"][0]
            self.assertEqual(observed["bytes"], len(truncated))
            self.assertEqual(observed["sha256"], hashlib.sha256(truncated).hexdigest())
            self.assertTrue(observed["errors"])
            self.assertNotIn("Traceback", proc.stdout + proc.stderr)

    def test_pillow_tail_tolerance_is_explicitly_not_full_container_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "one-byte-tail-truncation.png"
            raw = _save(path, image_format="PNG", mode="RGB", size=(3, 2))
            path.write_bytes(raw[:-1])
            proc, report = _run(path)

            # Pillow 12.3.0 can verify/load this one-byte tail truncation.  The
            # tool must preserve that observation without overclaiming integrity.
            self.assertEqual(proc.returncode, 0)
            self.assertIs(report["ok"], True)
            self.assertTrue(report["files"][0]["decode"]["verify"])
            self.assertTrue(report["files"][0]["decode"]["load"])
            self.assertFalse(report["validation_method"]["strict_full_file_integrity"])
            self.assertTrue(any("small tail truncation" in item for item in report["limitations"]))

    def test_expectation_mismatch_is_nonzero_but_keeps_actual_observation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "image.bin"
            _save(path, image_format="PNG", mode="RGB", size=(6, 5))
            proc, report = _run(path, expect_size="9x9", expect_format="JPEG")

            self.assertNotEqual(proc.returncode, 0)
            self.assertIs(report["ok"], False)
            observed = report["files"][0]
            self.assertEqual(observed["format"], "PNG")
            self.assertEqual(observed["width"], 6)
            self.assertEqual(observed["height"], 5)
            self.assertTrue(any("expect-size" in error or "expect-format" in error for error in observed["errors"]))

    def test_input_bytes_are_unchanged_and_files_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "first.png"
            nested = root / "nested" / "second.png"
            first_before = _save(first, image_format="PNG", size=(2, 2))
            _save(nested, image_format="PNG", size=(2, 2))
            proc, report = _run(first)
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(len(report["files"]), 1)
            self.assertEqual(first.read_bytes(), first_before)
            self.assertEqual(proc.stderr, "")

    def test_multiframe_scope_is_explicit_and_all_can_be_requested(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "animated.gif"
            frames = [Image.new("RGBA", (3, 2), (255, 0, 0, 255)), Image.new("RGBA", (3, 2), (0, 0, 255, 255))]
            try:
                frames[0].save(path, format="GIF", save_all=True, append_images=frames[1:], duration=20, loop=0)
            finally:
                for frame in frames:
                    frame.close()

            proc, report = _run(path)
            self.assertEqual(proc.returncode, 0)
            observed = report["files"][0]
            self.assertEqual(observed["frame_check"]["scope"], "first")
            self.assertEqual(observed["frame_check"]["frames_checked"], [0])
            self.assertFalse(observed["frame_check"]["complete"])

            proc, report = _run(path, frames="all")
            self.assertEqual(proc.returncode, 0)
            observed = report["files"][0]
            self.assertEqual(observed["frame_check"]["scope"], "all")
            self.assertEqual(observed["frame_check"]["frames_checked"], [0, 1])
            self.assertTrue(observed["frame_check"]["complete"])

    def test_missing_file_is_readable_json_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing.png"
            proc, report = _run(path)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(proc.stderr, "")
            self.assertIs(report["ok"], False)
            self.assertTrue(report["files"][0]["errors"])

    def test_python_s_reports_actionable_missing_pillow_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "image.png"
            _save(path, image_format="PNG", size=(2, 2))
            proc = subprocess.run(
                [PY, "-S", str(CHECKER), str(path)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            report = json.loads(proc.stdout)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(proc.stderr, "")
            self.assertIs(report["ok"], False)
            self.assertTrue(any("Pillow is unavailable" in error for error in report["errors"]))
            self.assertTrue(any("requirements-images.txt" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()

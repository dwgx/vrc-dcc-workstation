# -*- coding: utf-8 -*-
"""Regression tests for the pure-Python Blender mesh measurement helper.

These tests deliberately exercise the public ``measure_points`` contract with
plain Python values.  They do not import ``bpy`` or require a Blender install;
the Blender-facing fixture is covered by the separate runtime smoke test.
"""
from __future__ import annotations

import sys
from pathlib import Path
import unittest
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from measure_blender_mesh import MeasurementError, build_report, measure_points  # noqa: E402


def _corners(minimum: tuple[float, float, float], maximum: tuple[float, float, float]) -> list[tuple[float, float, float]]:
    """Return all eight corners of an axis-aligned box."""
    return [
        (x, y, z)
        for x in (minimum[0], maximum[0])
        for y in (minimum[1], maximum[1])
        for z in (minimum[2], maximum[2])
    ]


class BlenderMeasurementTests(unittest.TestCase):
    def test_identity_accepts_bytes_or_text_build_hash_before_geometry(self):
        for build_hash in (b"abc123", "abc123"):
            with self.subTest(build_hash=build_hash):
                scene = SimpleNamespace(name="Scene", frame_current=1, frame_subframe=0.0,
                                        unit_settings=SimpleNamespace())
                fake_bpy = SimpleNamespace(
                    app=SimpleNamespace(version_string="test fixture", build_hash=build_hash),
                    data=SimpleNamespace(filepath="", is_saved=False, is_dirty=False),
                    context=SimpleNamespace(scene=scene, view_layer=SimpleNamespace(name="Layer")),
                )
                report = build_report(fake_bpy, ["uninspected"], expected_file="/expected.blend")
                self.assertFalse(report["ok"])
                self.assertEqual(report["objects"], [])
                self.assertEqual(report["errors"][0]["code"], "FILE_MISMATCH")
                self.assertEqual(report["identity"]["blender_build_hash"], "abc123")

    def assert_vector(self, actual: object, expected: tuple[float, float, float]) -> None:
        self.assertIsInstance(actual, (list, tuple))
        self.assertEqual(len(actual), 3)
        for observed, wanted in zip(actual, expected):
            self.assertAlmostEqual(float(observed), wanted, places=7)

    def assert_aabb(
        self,
        actual: object,
        minimum: tuple[float, float, float],
        maximum: tuple[float, float, float],
    ) -> None:
        self.assertIsInstance(actual, dict)
        assert isinstance(actual, dict)
        self.assert_vector(actual["min"], minimum)
        self.assert_vector(actual["max"], maximum)
        self.assert_vector(
            actual["dimensions"],
            tuple(high - low for low, high in zip(minimum, maximum)),
        )

    def assert_measurement_error(self, callback) -> None:
        with self.assertRaises(MeasurementError) as raised:
            callback()
        # ``code`` is part of the machine-readable public failure contract;
        # keep the test independent of the particular code vocabulary.
        self.assertIsInstance(raised.exception.code, str)
        self.assertTrue(raised.exception.code)

    def test_rotated_cuboid_reports_local_and_world_aabbs(self) -> None:
        points = _corners((-1.0, -2.0, -0.5), (1.0, 2.0, 0.5))
        rotate_and_translate = [
            [0.0, -1.0, 0.0, 10.0],
            [1.0, 0.0, 0.0, -2.0],
            [0.0, 0.0, 1.0, 0.5],
            [0.0, 0.0, 0.0, 1.0],
        ]

        measured = measure_points(points, rotate_and_translate)

        self.assertEqual(measured["vertex_count"], 8)
        self.assert_aabb(measured["local_aabb_bu"], (-1.0, -2.0, -0.5), (1.0, 2.0, 0.5))
        self.assert_aabb(measured["world_aabb_bu"], (8.0, -3.0, 0.0), (12.0, -1.0, 1.0))
        self.assertIsNone(measured["world_aabb_m"])

    def test_parent_translation_and_shear_transform_all_points(self) -> None:
        # A parent-like affine transform with non-uniform scale, X/Y shear,
        # and translation.  The world AABB must be computed from transformed
        # points, rather than by independently scaling local dimensions.
        points = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 1.0, 0.0), (2.0, 1.0, 0.0)]
        parent_and_shear = [
            [2.0, 0.5, 0.0, 1.0],
            [0.0, 3.0, 0.0, -2.0],
            [0.0, 0.0, 1.0, 0.25],
            [0.0, 0.0, 0.0, 1.0],
        ]

        measured = measure_points(points, parent_and_shear)

        self.assertEqual(measured["vertex_count"], 4)
        self.assert_aabb(measured["local_aabb_bu"], (0.0, 0.0, 0.0), (2.0, 1.0, 0.0))
        self.assert_aabb(measured["world_aabb_bu"], (1.0, -2.0, 0.25), (5.5, 1.0, 0.25))

    def test_negative_nonuniform_scale_preserves_axis_extents(self) -> None:
        points = _corners((-1.0, -2.0, -0.5), (1.0, 2.0, 0.5))
        reflected_and_scaled = [
            [-2.0, 0.0, 0.0, 3.0],
            [0.0, 0.5, 0.0, -4.0],
            [0.0, 0.0, -3.0, 1.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

        measured = measure_points(points, reflected_and_scaled, meters_per_unit=0.01)

        self.assert_aabb(measured["world_aabb_bu"], (1.0, -5.0, -0.5), (5.0, -3.0, 2.5))
        self.assert_aabb(measured["world_aabb_m"], (0.01, -0.05, -0.005), (0.05, -0.03, 0.025))

    def test_unknown_units_stay_unknown_and_centimeter_scale_is_explicit(self) -> None:
        points = [(0.0, 0.0, 0.0), (100.0, 20.0, 5.0)]
        identity = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

        unknown = measure_points(points, identity)
        centimetres = measure_points(points, identity, meters_per_unit=0.01)

        self.assertIsNone(unknown["world_aabb_m"])
        self.assert_aabb(centimetres["world_aabb_m"], (0.0, 0.0, 0.0), (1.0, 0.2, 0.05))

    def test_zero_extent_plane_is_valid(self) -> None:
        points = ((x, y, 0.0) for x, y in ((0.0, 0.0), (1.0, 0.0), (0.0, 2.0), (1.0, 2.0)))
        identity = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

        measured = measure_points(points, identity)

        self.assertEqual(measured["vertex_count"], 4)
        self.assert_aabb(measured["local_aabb_bu"], (0.0, 0.0, 0.0), (1.0, 2.0, 0.0))
        self.assert_aabb(measured["world_aabb_bu"], (0.0, 0.0, 0.0), (1.0, 2.0, 0.0))

    def test_rejects_empty_points_and_nonfinite_points(self) -> None:
        identity = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

        self.assert_measurement_error(lambda: measure_points([], identity))
        self.assert_measurement_error(lambda: measure_points([(0.0, 1.0, float("nan"))], identity))
        self.assert_measurement_error(lambda: measure_points([(0.0, 1.0, float("inf"))], identity))
        self.assert_measurement_error(lambda: measure_points([(0.0, 1.0)], identity))
        self.assert_measurement_error(lambda: measure_points(["123"], identity))
        self.assert_measurement_error(lambda: measure_points([b"123"], identity))

    def test_rejects_malformed_nonfinite_and_non_affine_matrices(self) -> None:
        valid_points = [(0.0, 0.0, 0.0)]
        identity = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

        cases = [
            ["1000", "0100", "0010", "0001"],
            [],
            identity[:3],
            [row[:3] for row in identity],
            [identity[0], identity[1], identity[2], [0.0, 0.0, 0.0]],
            [*identity[:3], [0.0, 0.0, 0.0, 2.0]],
            [*identity[:3], [0.0, 0.0, 1.0, 1.0]],
            [[float("nan"), 0.0, 0.0, 0.0], *identity[1:]],
            [[float("inf"), 0.0, 0.0, 0.0], *identity[1:]],
        ]
        for matrix in cases:
            with self.subTest(matrix=matrix):
                self.assert_measurement_error(lambda matrix=matrix: measure_points(valid_points, matrix))

    def test_rejects_invalid_unit_scales_including_bool(self) -> None:
        identity = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
        points = [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)]

        for scale in (0.0, -0.01, float("nan"), float("inf"), True, False):
            with self.subTest(scale=scale):
                self.assert_measurement_error(lambda scale=scale: measure_points(points, identity, scale))


if __name__ == "__main__":
    unittest.main()

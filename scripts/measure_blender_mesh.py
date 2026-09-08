#!/usr/bin/env python3
"""Read named evaluated meshes in Blender; write a new measurement receipt.

No operators, file saves, scene edits, network calls or MCP connection are used.
Run inside the already-authorized target Blender, or an isolated background
process. Pure coordinate helpers are also importable without Blender.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import sys
import uuid


class MeasurementError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def _number(value):
    if isinstance(value, (bool, str, bytes, bytearray)):
        raise MeasurementError("INVALID_NUMBER", "Expected a number, not a boolean or text")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise MeasurementError("INVALID_NUMBER", "Expected a finite number") from exc
    if not math.isfinite(result):
        raise MeasurementError("NONFINITE_NUMBER", "Expected a finite number")
    return result


def _scale(value):
    result = _number(value)
    if result <= 0:
        raise MeasurementError("INVALID_UNIT_SCALE", "Meters per unit must be positive")
    return result


def _bounds(low, high, scale=1.0):
    return {
        "min": [_number(x * scale) for x in low],
        "max": [_number(x * scale) for x in high],
        "dimensions": [_number((b - a) * scale) for a, b in zip(low, high)],
    }


def measure_points(points, matrix_world, meters_per_unit=None):
    """Single-pass bounds of mesh vertices in local and transformed world space.

    Matrix includes parent, rotation, scale and shear. These are vertex extents,
    not actual volume or collision/walkability measurements. Units are Blender
    units unless an explicit conversion factor is supplied.
    """
    try:
        matrix = []
        for row in matrix_world:
            if isinstance(row, (str, bytes, bytearray)):
                raise MeasurementError("INVALID_MATRIX", "Expected numeric matrix rows, not text")
            matrix.append(list(row))
    except TypeError as exc:
        raise MeasurementError("INVALID_MATRIX", "Expected four affine matrix rows") from exc
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise MeasurementError("INVALID_MATRIX", "Expected a 4x4 affine matrix")
    matrix = [[_number(x) for x in row] for row in matrix]
    if matrix[3] != [0.0, 0.0, 0.0, 1.0]:
        raise MeasurementError("INVALID_MATRIX", "Perspective transforms are unsupported")
    factor = None if meters_per_unit is None else _scale(meters_per_unit)
    local_low = [math.inf] * 3
    local_high = [-math.inf] * 3
    world_low = [math.inf] * 3
    world_high = [-math.inf] * 3
    count = 0
    for point in points:
        if isinstance(point, (str, bytes, bytearray)):
            raise MeasurementError("INVALID_POINT", "Expected a numeric coordinate triple, not text")
        try:
            xyz = list(point)
        except TypeError as exc:
            raise MeasurementError("INVALID_POINT", "Expected a coordinate triple") from exc
        if len(xyz) != 3:
            raise MeasurementError("INVALID_POINT", "Expected a coordinate triple")
        xyz = [_number(x) for x in xyz]
        world = [_number(sum(row[i] * xyz[i] for i in range(3)) + row[3])
                 for row in matrix[:3]]
        for i in range(3):
            local_low[i] = min(local_low[i], xyz[i])
            local_high[i] = max(local_high[i], xyz[i])
            world_low[i] = min(world_low[i], world[i])
            world_high[i] = max(world_high[i], world[i])
        count += 1
    if not count:
        raise MeasurementError("EMPTY_GEOMETRY", "The evaluated mesh has no vertices")
    return {
        "vertex_count": count,
        "local_aabb_bu": _bounds(local_low, local_high),
        "world_aabb_bu": _bounds(world_low, world_high),
        "world_aabb_m": None if factor is None else _bounds(world_low, world_high, factor),
    }


def _error(exc):
    return {"code": getattr(exc, "code", "READ_FAILED"), "message": str(exc)}


def _same_path(left, right):
    return bool(left and right) and os.path.normcase(os.path.realpath(left)) == os.path.normcase(os.path.realpath(right))


def _identity(bpy):
    scene = bpy.context.scene
    build_hash = bpy.app.build_hash
    if isinstance(build_hash, (bytes, bytearray)):
        build_hash = build_hash.decode("ascii", errors="replace")
    return {
        "pid": os.getpid(),
        "blender_version": bpy.app.version_string,
        "blender_build_hash": str(build_hash),
        "blend_filepath": bpy.data.filepath,
        "is_saved": bpy.data.is_saved,
        "is_dirty": bpy.data.is_dirty,
        "scene_name": scene.name,
        "view_layer": bpy.context.view_layer.name,
        "frame": scene.frame_current,
        "subframe": scene.frame_subframe,
        "transport": "local_blender_python",
    }


def build_report(bpy_module, names, meters_per_unit=None, expected_file=None, expected_scene=None):
    """Collect a current scene receipt; no mutation or persistent mesh allocation."""
    bpy = bpy_module
    scene = bpy.context.scene
    units = scene.unit_settings
    report = {
        "schema_version": 1,
        "ok": False,
        "request_id": str(uuid.uuid4()),
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "identity": _identity(bpy),
        "expected": {"blend_filepath": expected_file, "scene_name": expected_scene},
        "units": None,
        "objects": [],
        "errors": [],
        "limitations": [
            "Evaluated mesh vertex stream at the recorded frame/view layer; instances are not independently enumerated.",
            "Bounds are not true mesh volume, collision clearance or walkability.",
            "Meter values use the declared conversion only; Unity import and VRChat client behavior are not tested.",
            "Current in-memory scene identity is not a writer lock or a saved-file content revision.",
        ],
    }
    try:
        if expected_file is not None and not _same_path(bpy.data.filepath, expected_file):
            raise MeasurementError("FILE_MISMATCH", "Current Blender file differs from expected file")
        if expected_scene is not None and scene.name != expected_scene:
            raise MeasurementError("SCENE_MISMATCH", "Current scene differs from expected scene")
        if meters_per_unit is not None:
            factor, source = _scale(meters_per_unit), "explicit_override"
        elif units.system in {"METRIC", "IMPERIAL"}:
            factor, source = _scale(units.scale_length), "scene_unit_scale"
        else:
            factor, source = None, "unknown"
        report["units"] = {
            "system": units.system,
            "length_unit": units.length_unit,
            "scene_scale_length": _number(units.scale_length),
            "meters_per_unit": factor,
            "source": source,
        }
        if isinstance(names, str):
            raise MeasurementError("INVALID_OBJECT_NAMES", "Pass a list of exact object names")
        names = list(names)
        if not names or any(not isinstance(name, str) or not name for name in names):
            raise MeasurementError("NO_OBJECTS", "Name at least one mesh object")
        depsgraph = bpy.context.evaluated_depsgraph_get()
    except Exception as exc:
        report["errors"].append(_error(exc))
        return report

    for name in names:
        row = {"ok": False, "object": name}
        evaluated = None
        mesh = None
        try:
            obj = scene.objects.get(name)
            if obj is None:
                raise MeasurementError("OBJECT_NOT_FOUND", "No such object in the current scene")
            if bpy.context.view_layer.objects.get(name) is None:
                raise MeasurementError("OBJECT_NOT_IN_VIEW_LAYER", "Object is outside the current view layer")
            if obj.type != "MESH":
                raise MeasurementError("UNSUPPORTED_OBJECT_TYPE", "This tool measures mesh vertices")
            if obj.mode != "OBJECT":
                raise MeasurementError("UNSUPPORTED_OBJECT_MODE", "Object-mode mesh required; edit-mode data may be stale")
            evaluated = obj.evaluated_get(depsgraph)
            if not evaluated.is_evaluated:
                raise MeasurementError("NOT_EVALUATED", "Object is unavailable in the evaluated dependency graph")
            mesh = evaluated.to_mesh()
            if mesh is None:
                raise MeasurementError("EMPTY_GEOMETRY", "No evaluated mesh")
            row["geometry"] = measure_points((v.co for v in mesh.vertices), evaluated.matrix_world, factor)
            row["geometry_scope"] = "evaluated_mesh_vertex_stream"
            row["instance_enumeration"] = "not_checked"
            row["matrix_world"] = [[float(x) for x in axis] for axis in evaluated.matrix_world]
            row["evaluation_mode"] = depsgraph.mode
            row["visible_in_view_layer"] = obj.visible_get(view_layer=bpy.context.view_layer)
            row["source_library"] = obj.library.filepath if obj.library else None
            row["ok"] = True
        except Exception as exc:
            row["error"] = _error(exc)
        finally:
            if evaluated is not None and mesh is not None:
                try:
                    evaluated.to_mesh_clear()
                except Exception as exc:
                    row["ok"] = False
                    row["error"] = {"code": "MESH_CLEANUP_FAILED", "message": str(exc)}
        report["objects"].append(row)
    report["identity_after"] = _identity(bpy)
    if report["identity_after"] != report["identity"]:
        report["errors"].append({"code": "CONTEXT_CHANGED", "message": "Scene identity changed during evaluation; inspect and retry"})
    report["ok"] = not report["errors"] and all(row["ok"] for row in report["objects"])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--object", action="append", required=True, dest="objects")
    parser.add_argument("--output", required=True, type=Path, help="New JSON receipt path; existing files are preserved")
    parser.add_argument("--meters-per-unit", type=float)
    parser.add_argument("--expect-file")
    parser.add_argument("--expect-scene")
    if argv is None:
        argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    args = parser.parse_args(argv)
    try:
        import bpy
    except ImportError:
        print("Run this script inside Blender; use --help for arguments.", file=sys.stderr)
        return 2
    report = build_report(bpy, args.objects, args.meters_per_unit, args.expect_file, args.expect_scene)
    try:
        payload = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    except (OSError, ValueError) as exc:
        print(f"Could not write new receipt: {exc}", file=sys.stderr)
        return 2
    print(f"Measurement receipt: {args.output} (ok={report['ok']})")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

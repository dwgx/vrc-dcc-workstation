"""Blender regression fixture for the read-only mesh measurement helper.

Run this file from Blender, for example::

    blender --background --factory-startup --python tests/blender_measurement_fixture.py -- \
        --output-root D:/tmp/vrc-measurement

The fixture deliberately owns every object it creates.  It writes a new run
directory below ``--output-root`` and never removes an existing artifact.  The
test is kept in one file so it can be copied into a clean station checkout and
run without pytest, an add-on, a live MCP server, or a project file.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import sys
import time
import traceback
from pathlib import Path

try:  # Keep the file syntax-checkable outside Blender.
    import bpy  # type: ignore
    from mathutils import Matrix, Vector  # type: ignore
except ImportError:  # pragma: no cover - exercised only by py_compile
    bpy = None  # type: ignore
    Matrix = None  # type: ignore
    Vector = None  # type: ignore


CURRENT_SCENE_NAME = 'Measurement Fixture "CM"'
QUOTED_OBJECT_NAME = 'Fixture "Quoted Cube"'
ARRAY_OBJECT_NAME = 'Fixture Array Cube'
EMPTY_OBJECT_NAME = 'Fixture Empty (not mesh)'
HIDDEN_OBJECT_NAME = 'Fixture Hidden View Layer'
FOREIGN_OBJECT_NAME = 'Fixture Other Scene'
MISSING_OBJECT_NAME = 'Fixture Missing "Object"'

BASE_BOX_MIN = (-1.0, -1.0, -1.0)
BASE_BOX_MAX = (1.0, 1.0, 1.0)
QUOTED_BOX_MIN = (-1.0, -0.5, -0.75)
QUOTED_BOX_MAX = (1.0, 1.25, 1.5)


class FixtureFailure(RuntimeError):
    """A fixture setup failure that should be reported in fixture-result.json."""


def _require_blender() -> None:
    if bpy is None or Matrix is None or Vector is None:
        raise FixtureFailure("This fixture must run inside Blender's Python environment")
    if not bpy.app.background or bpy.data.is_saved:
        raise FixtureFailure("Use a separate background factory-startup process without a loaded file")


def _parse_output_root(argv: list[str]) -> Path:
    """Parse only arguments after Blender's ``--`` separator."""

    try:
        separator = argv.index("--")
    except ValueError as exc:
        raise FixtureFailure("missing Blender argument separator '--'") from exc

    args = argv[separator + 1 :]
    output_root: str | None = None
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--output-root":
            if index + 1 >= len(args) or not args[index + 1].strip():
                raise FixtureFailure("--output-root requires a non-empty path")
            output_root = args[index + 1]
            index += 2
            continue
        raise FixtureFailure(f"unknown fixture argument: {arg}")

    if output_root is None:
        raise FixtureFailure("usage: --output-root <directory>")
    return Path(output_root).expanduser().resolve()


def _new_run_directory(output_root: Path) -> Path:
    """Create a unique artifact directory without touching prior runs."""

    output_root.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    for suffix in range(1000):
        suffix_text = f"-{suffix:02d}" if suffix else ""
        candidate = output_root / f"blender-measurement-fixture-{stamp}-{os.getpid()}{suffix_text}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        return candidate
    raise FixtureFailure(f"could not allocate a new run directory below {output_root}")


def _load_measurement_module() -> object:
    """Load the station helper from this checkout without installing anything."""

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "measure_blender_mesh.py"
    if not script_path.is_file():
        raise FixtureFailure(f"measurement helper is missing: {script_path}")
    module_name = "vrc_dcc_measure_blender_mesh_fixture_target"
    spec = importlib.util.spec_from_file_location(module_name, str(script_path))
    if spec is None or spec.loader is None:
        raise FixtureFailure(f"could not load measurement helper: {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    if not hasattr(module, "build_report"):
        raise FixtureFailure(f"measurement helper has no build_report(): {script_path}")
    return module


def _box_vertices(minimum: tuple[float, float, float], maximum: tuple[float, float, float]):
    xmin, ymin, zmin = minimum
    xmax, ymax, zmax = maximum
    return [
        (xmin, ymin, zmin),
        (xmax, ymin, zmin),
        (xmax, ymax, zmin),
        (xmin, ymax, zmin),
        (xmin, ymin, zmax),
        (xmax, ymin, zmax),
        (xmax, ymax, zmax),
        (xmin, ymax, zmax),
    ]


BOX_FACES = [
    (0, 1, 2, 3),
    (4, 7, 6, 5),
    (0, 4, 5, 1),
    (1, 5, 6, 2),
    (2, 6, 7, 3),
    (4, 0, 3, 7),
]


def _add_mesh_object(scene_collection, name: str, vertices, faces):
    mesh = bpy.data.meshes.new(f"{name} Data")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    scene_collection.objects.link(obj)
    return obj


def _add_empty(scene_collection, name: str):
    obj = bpy.data.objects.new(name, None)
    scene_collection.objects.link(obj)
    return obj


def _set_transform(obj, location, rotation, scale):
    obj.location = location
    obj.rotation_mode = "XYZ"
    obj.rotation_euler = rotation
    obj.scale = scale


def _set_parent(child, parent) -> None:
    child.parent = parent
    # Make the parent transform intentionally observable.  The child keeps its
    # local transform, so matrix_world is analytically parent_world @ local.
    child.matrix_parent_inverse = Matrix.Identity(4)


def _create_fixture_scene() -> dict[str, object]:
    """Build all owned scenes, collections, objects, and known transforms."""

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    if scene is None:
        scene = bpy.data.scenes.new(CURRENT_SCENE_NAME)
        bpy.context.window.scene = scene
    scene.name = CURRENT_SCENE_NAME
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.01
    scene.unit_settings.length_unit = "CENTIMETERS"

    fixture_collection = bpy.data.collections.new('Fixture Collection "Owned"')
    scene.collection.children.link(fixture_collection)

    parent = _add_empty(fixture_collection, 'Fixture Parent "Transform"')
    _set_transform(
        parent,
        (1.25, -2.0, 0.75),
        (0.25, -0.15, 0.4),
        (1.3, 0.8, -0.7),
    )

    quoted = _add_mesh_object(
        fixture_collection,
        QUOTED_OBJECT_NAME,
        _box_vertices(QUOTED_BOX_MIN, QUOTED_BOX_MAX),
        BOX_FACES,
    )
    _set_transform(
        quoted,
        (2.0, -1.0, 0.5),
        (0.1, -0.2, 0.35),
        (-1.25, 0.5, 2.0),
    )
    _set_parent(quoted, parent)

    array_object = _add_mesh_object(
        fixture_collection,
        ARRAY_OBJECT_NAME,
        _box_vertices(BASE_BOX_MIN, BASE_BOX_MAX),
        BOX_FACES,
    )
    _set_transform(
        array_object,
        (-3.0, 2.0, 0.25),
        (0.0, 0.0, math.pi / 8.0),
        (1.0, 0.5, 2.0),
    )
    array_modifier = array_object.modifiers.new("Fixture Array", "ARRAY")
    array_modifier.count = 2
    array_modifier.use_relative_offset = True
    array_modifier.relative_offset_displace = (1.0, 0.0, 0.0)
    array_modifier.use_constant_offset = False

    empty = _add_empty(fixture_collection, EMPTY_OBJECT_NAME)
    _set_transform(empty, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))

    hidden_collection = bpy.data.collections.new('Fixture Hidden Collection "Excluded"')
    scene.collection.children.link(hidden_collection)
    hidden = _add_mesh_object(
        hidden_collection,
        HIDDEN_OBJECT_NAME,
        _box_vertices(BASE_BOX_MIN, BASE_BOX_MAX),
        BOX_FACES,
    )
    _set_transform(hidden, (10.0, 10.0, 10.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))
    hidden_layer_collection = next(
        child
        for child in bpy.context.view_layer.layer_collection.children
        if child.collection == hidden_collection
    )
    hidden_layer_collection.exclude = True

    # An object with the same ownership prefix in a different scene catches
    # accidental bpy.data.objects lookup instead of current-scene traversal.
    foreign_scene = bpy.data.scenes.new('Fixture Other Scene')
    foreign_collection = bpy.data.collections.new('Fixture Other Scene Collection')
    foreign_scene.collection.children.link(foreign_collection)
    foreign = _add_mesh_object(
        foreign_collection,
        FOREIGN_OBJECT_NAME,
        _box_vertices(BASE_BOX_MIN, BASE_BOX_MAX),
        BOX_FACES,
    )
    _set_transform(foreign, (20.0, 20.0, 20.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))

    # Ensure the active target is in Object mode and is selected deterministically.
    for candidate in bpy.context.view_layer.objects:
        candidate.select_set(False)
    quoted.select_set(True)
    bpy.context.view_layer.objects.active = quoted
    bpy.context.view_layer.update()

    return {
        "scene": scene,
        "foreign_scene": foreign_scene,
        "parent": parent,
        "quoted": quoted,
        "array": array_object,
        "empty": empty,
        "hidden": hidden,
        "foreign": foreign,
    }


def _matrix_tuple(matrix):
    return tuple(tuple(float(value) for value in row) for row in matrix)


def _object_snapshot(obj):
    data_vertices = ()
    if getattr(obj, "type", None) == "MESH" and obj.data is not None:
        data_vertices = tuple(
            tuple(float(value) for value in vertex.co[:3]) for vertex in obj.data.vertices
        )
    modifiers = tuple(
        (
            modifier.name,
            modifier.type,
            bool(getattr(modifier, "show_viewport", True)),
            bool(getattr(modifier, "show_render", True)),
        )
        for modifier in obj.modifiers
    )
    return {
        "name": obj.name,
        "type": obj.type,
        "matrix_world": _matrix_tuple(obj.matrix_world),
        "location": tuple(float(value) for value in obj.location),
        "rotation_euler": tuple(float(value) for value in obj.rotation_euler),
        "scale": tuple(float(value) for value in obj.scale),
        "parent": obj.parent.name if obj.parent else None,
        "selected": bool(obj.select_get()),
        "hide_viewport": bool(obj.hide_viewport),
        "hide_render": bool(obj.hide_render),
        "data_vertices": data_vertices,
        "modifiers": modifiers,
    }


def _state_snapshot():
    scene = bpy.context.scene
    unit_settings = scene.unit_settings
    return {
        "filepath": str(getattr(bpy.data, "filepath", "")),
        "is_dirty": getattr(bpy.data, "is_dirty", None),
        "scene": scene.name if scene else None,
        "frame_current": int(scene.frame_current) if scene else None,
        "frame_subframe": float(scene.frame_subframe) if scene else None,
        "mode": bpy.context.mode,
        "active": (
            bpy.context.view_layer.objects.active.name
            if bpy.context.view_layer.objects.active
            else None
        ),
        "selected": tuple(sorted(obj.name for obj in bpy.context.selected_objects)),
        "view_layer": bpy.context.view_layer.name,
        "scene_units": {
            "system": unit_settings.system,
            "scale_length": float(unit_settings.scale_length),
            "length_unit": unit_settings.length_unit,
        },
        "scene_objects": tuple(
            _object_snapshot(obj) for obj in sorted(scene.objects, key=lambda item: item.name)
        ),
        "view_layer_objects": tuple(sorted(obj.name for obj in bpy.context.view_layer.objects)),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _transform_points(obj, points):
    return [obj.matrix_world @ Vector(point) for point in points]


def _bounds(points):
    if not points:
        raise FixtureFailure("cannot compute bounds for an empty point set")
    minimum = tuple(min(float(point[index]) for point in points) for index in range(3))
    maximum = tuple(max(float(point[index]) for point in points) for index in range(3))
    dimensions = tuple(maximum[index] - minimum[index] for index in range(3))
    return {"min": minimum, "max": maximum, "dimensions": dimensions}


def _expected_geometry(objects: dict[str, object], meters_per_unit: float | None):
    quoted = objects["quoted"]
    array_object = objects["array"]
    quoted_local = _bounds([Vector(vertex) for vertex in _box_vertices(QUOTED_BOX_MIN, QUOTED_BOX_MAX)])
    array_local_points = [
        Vector(vertex) for vertex in _box_vertices(BASE_BOX_MIN, BASE_BOX_MAX)
    ] + [
        Vector((vertex[0] + 2.0, vertex[1], vertex[2]))
        for vertex in _box_vertices(BASE_BOX_MIN, BASE_BOX_MAX)
    ]
    expected = {
        QUOTED_OBJECT_NAME: {
            "local": quoted_local,
            "world": _bounds(_transform_points(quoted, _box_vertices(QUOTED_BOX_MIN, QUOTED_BOX_MAX))),
        },
        ARRAY_OBJECT_NAME: {
            "local": _bounds(array_local_points),
            "world": _bounds(_transform_points(array_object, array_local_points)),
        },
    }
    for values in expected.values():
        world = values["world"]
        values["world_m"] = (
            None
            if meters_per_unit is None
            else {
                key: tuple(float(value) * meters_per_unit for value in vector)
                for key, vector in world.items()
            }
        )
    return expected


def _as_vec3(value):
    if isinstance(value, dict):
        if all(key in value for key in ("x", "y", "z")):
            return (float(value["x"]), float(value["y"]), float(value["z"]))
        if all(key in value for key in (0, 1, 2)):
            return (float(value[0]), float(value[1]), float(value[2]))
    return tuple(float(component) for component in value[:3])


def _assert_vec3(actual, expected, label: str, errors: list[str], tolerance=1e-5):
    try:
        actual_vec = _as_vec3(actual)
        expected_vec = _as_vec3(expected)
    except Exception as exc:  # pragma: no cover - defensive schema diagnostic
        errors.append(f"{label}: not a 3-vector ({exc})")
        return
    if len(actual_vec) != 3 or any(
        not math.isclose(actual_vec[index], expected_vec[index], rel_tol=1e-6, abs_tol=tolerance)
        for index in range(3)
    ):
        errors.append(f"{label}: expected {expected_vec}, got {actual_vec}")


def _assert_geometry(
    report,
    expected,
    label: str,
    errors: list[str],
    meters_per_unit: float | None,
):
    rows = report.get("objects") if isinstance(report, dict) else None
    if not isinstance(rows, list):
        errors.append(f"{label}: report.objects is not a list")
        return
    by_name = {
        row.get("object"): row for row in rows if isinstance(row, dict) and row.get("object")
    }
    for object_name, values in expected.items():
        row = by_name.get(object_name)
        if row is None:
            errors.append(f"{label}: missing object row {object_name!r}")
            continue
        if row.get("ok") is not True:
            errors.append(f"{label}: object row {object_name!r} is not ok: {row}")
            continue
        geometry = row.get("geometry")
        if not isinstance(geometry, dict):
            errors.append(f"{label}: object {object_name!r} has no geometry")
            continue
        for report_key, expected_key in (
            ("local_aabb_bu", "local"),
            ("world_aabb_bu", "world"),
            ("world_aabb_m", "world_m"),
        ):
            actual_box = geometry.get(report_key)
            expected_box = values[expected_key]
            if expected_box is None:
                if actual_box is not None:
                    errors.append(
                        f"{label}: {object_name!r} geometry.{report_key} expected null, got {actual_box}"
                    )
                continue
            if not isinstance(actual_box, dict):
                errors.append(f"{label}: {object_name!r} geometry.{report_key} is missing")
                continue
            for bound_key in ("min", "max", "dimensions"):
                if bound_key not in actual_box:
                    errors.append(f"{label}: {object_name!r} geometry.{report_key}.{bound_key} is missing")
                else:
                    _assert_vec3(
                        actual_box[bound_key],
                        expected_box[bound_key],
                        f"{label}:{object_name}:{report_key}:{bound_key}",
                        errors,
                    )

    units = report.get("units") if isinstance(report, dict) else None
    if not isinstance(units, dict):
        errors.append(f"{label}: report.units is not an object")
    else:
        actual_meters = units.get("meters_per_unit")
        if meters_per_unit is None:
            if actual_meters is not None:
                errors.append(
                    f"{label}: expected units.meters_per_unit=null, got {actual_meters!r}"
                )
        elif not isinstance(actual_meters, (int, float)) or not math.isclose(
            float(actual_meters), meters_per_unit, rel_tol=1e-6, abs_tol=1e-8
        ):
            errors.append(
                f"{label}: expected units.meters_per_unit={meters_per_unit}, got {actual_meters!r}"
            )


def _jsonable(value):
    """Convert Blender/mathutils values defensively for receipt writing."""

    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, Path):
        return str(value)
    return str(value)


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(_jsonable(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _report_call(measurement_module, names, meters_per_unit=None, expected_file=None, expected_scene=None):
    """Call the explicit helper contract and keep failures in the receipt."""

    return measurement_module.build_report(
        bpy,
        list(names),
        meters_per_unit=meters_per_unit,
        expected_file=expected_file,
        expected_scene=expected_scene,
    )


def _run(output_root: Path) -> tuple[int, Path]:
    _require_blender()
    run_directory = _new_run_directory(output_root)
    receipts_directory = run_directory / "receipts"
    receipts_directory.mkdir()
    result: dict[str, object] = {
        "ok": False,
        "fixture": {"run_directory": str(run_directory)},
        "reports": {},
        "checks": {},
        "errors": [],
    }
    errors: list[str] = result["errors"]  # type: ignore[assignment]

    try:
        measurement_module = _load_measurement_module()
        objects = _create_fixture_scene()
        scene = objects["scene"]
        quoted = objects["quoted"]
        array_object = objects["array"]

        bpy.context.view_layer.update()
        expected_metric = _expected_geometry(objects, 0.01)
        expected_none = _expected_geometry(objects, None)
        expected_override = _expected_geometry(objects, 0.25)
        valid_names = [QUOTED_OBJECT_NAME, ARRAY_OBJECT_NAME]
        mixed_names = [
            QUOTED_OBJECT_NAME,
            ARRAY_OBJECT_NAME,
            EMPTY_OBJECT_NAME,
            HIDDEN_OBJECT_NAME,
            FOREIGN_OBJECT_NAME,
            MISSING_OBJECT_NAME,
        ]

        def call(label, names, meters_per_unit=None, expected_file=None, expected_scene=None):
            before = _state_snapshot()
            try:
                report = _report_call(
                    measurement_module,
                    names,
                    meters_per_unit=meters_per_unit,
                    expected_file=expected_file,
                    expected_scene=expected_scene,
                )
            except Exception as exc:  # Keep all other checks and write a useful receipt.
                report = {
                    "ok": False,
                    "objects": [],
                    "errors": [{"code": "fixture_call_exception", "message": str(exc)}],
                }
                errors.append(f"{label}: build_report raised {type(exc).__name__}: {exc}")
            after = _state_snapshot()
            if before != after:
                errors.append(f"{label}: build_report changed the in-memory scene/context state")
            result["reports"][label] = _jsonable(report)  # type: ignore[index]
            _write_json(receipts_directory / f"{label}.json", report)
            return report

        # The factory-startup file has no path.  This checks the unsaved identity
        # independently from the later saved-file/hash checks.
        unsaved_report = call("unsaved-metric-cm", valid_names)
        identity = unsaved_report.get("identity", {}) if isinstance(unsaved_report, dict) else {}
        if identity.get("is_saved") is not False:
            errors.append(f"unsaved-metric-cm: expected identity.is_saved=false, got {identity}")
        if identity.get("blend_filepath") not in ("", None):
            errors.append(f"unsaved-metric-cm: expected empty blend_filepath, got {identity}")
        if unsaved_report.get("ok") is not True:
            errors.append(f"unsaved-metric-cm: report is not ok: {unsaved_report}")
        _assert_geometry(unsaved_report, expected_metric, "unsaved-metric-cm", errors, 0.01)

        fixture_path = run_directory / "measurement_fixture.blend"
        save_result = bpy.ops.wm.save_as_mainfile(filepath=str(fixture_path))
        if "FINISHED" not in save_result or not fixture_path.is_file():
            raise FixtureFailure(f"Blender did not save fixture: {fixture_path} ({save_result})")
        hash_before_reports = _sha256(fixture_path)
        result["fixture"].update(  # type: ignore[union-attr]
            {
                "blend_path": str(fixture_path),
                "blend_sha256_before_reports": hash_before_reports,
                "scene_name": scene.name,
                "quoted_object": quoted.name,
                "array_object": array_object.name,
            }
        )

        saved_report = call(
            "saved-metric-cm",
            valid_names,
            expected_file=str(fixture_path),
            expected_scene=scene.name,
        )
        saved_identity = saved_report.get("identity", {}) if isinstance(saved_report, dict) else {}
        if saved_identity.get("is_saved") is not True:
            errors.append(f"saved-metric-cm: expected identity.is_saved=true, got {saved_identity}")
        if saved_report.get("ok") is not True:
            errors.append(f"saved-metric-cm: report is not ok: {saved_report}")
        _assert_geometry(saved_report, expected_metric, "saved-metric-cm", errors, 0.01)
        hash_after_saved_report = _sha256(fixture_path)
        if hash_before_reports != hash_after_saved_report:
            errors.append("saved-metric-cm: fixture hash changed during read-only report")

        # Unit NONE does not declare a meter conversion.  Keep raw BU bounds,
        # and require the helper to leave meter bounds unknown until an
        # explicit override is supplied.
        scene.unit_settings.system = "NONE"
        scene.unit_settings.scale_length = 1.0
        scene.unit_settings.length_unit = "ADAPTIVE"
        none_report = call(
            "unsaved-unit-none",
            valid_names,
            expected_file=str(fixture_path),
            expected_scene=scene.name,
        )
        if none_report.get("ok") is not True:
            errors.append(f"unsaved-unit-none: report is not ok: {none_report}")
        _assert_geometry(none_report, expected_none, "unsaved-unit-none", errors, None)

        override_report = call(
            "explicit-override-025",
            valid_names,
            meters_per_unit=0.25,
            expected_file=str(fixture_path),
            expected_scene=scene.name,
        )
        if override_report.get("ok") is not True:
            errors.append(f"explicit-override-025: report is not ok: {override_report}")
        _assert_geometry(override_report, expected_override, "explicit-override-025", errors, 0.25)

        mixed_report = call(
            "mixed-invalid-names",
            mixed_names,
            meters_per_unit=0.25,
            expected_file=str(fixture_path),
            expected_scene=scene.name,
        )
        if mixed_report.get("ok") is not False:
            errors.append(f"mixed-invalid-names: expected ok=false, got {mixed_report}")
        mixed_rows = mixed_report.get("objects", []) if isinstance(mixed_report, dict) else []
        mixed_by_name = {
            row.get("object"): row
            for row in mixed_rows
            if isinstance(row, dict) and row.get("object")
        }
        for invalid_name in (
            EMPTY_OBJECT_NAME,
            HIDDEN_OBJECT_NAME,
            FOREIGN_OBJECT_NAME,
            MISSING_OBJECT_NAME,
        ):
            row = mixed_by_name.get(invalid_name)
            if not isinstance(row, dict) or row.get("ok") is not False or not isinstance(
                row.get("error"), dict
            ):
                errors.append(f"mixed-invalid-names: expected structured error for {invalid_name!r}, got {row}")

        wrong_file_report = call(
            "mismatch-file",
            valid_names,
            expected_file=str(run_directory / "different-file.blend"),
            expected_scene=scene.name,
        )
        if wrong_file_report.get("ok") is not False or wrong_file_report.get("objects") != []:
            errors.append(
                f"mismatch-file: expected ok=false and objects=[], got {wrong_file_report}"
            )

        wrong_scene_report = call(
            "mismatch-scene",
            valid_names,
            expected_file=str(fixture_path),
            expected_scene="Fixture Scene That Does Not Exist",
        )
        if wrong_scene_report.get("ok") is not False or wrong_scene_report.get("objects") != []:
            errors.append(
                f"mismatch-scene: expected ok=false and objects=[], got {wrong_scene_report}"
            )

        # The helper must refuse to interpret edit-mode data as an object-mode
        # measurement.  Restore Object mode even when the check fails.
        for candidate in bpy.context.view_layer.objects:
            candidate.select_set(False)
        quoted.select_set(True)
        bpy.context.view_layer.objects.active = quoted
        bpy.ops.object.mode_set(mode="EDIT")
        try:
            edit_mode_report = call(
                "edit-mode-rejected",
                valid_names,
                meters_per_unit=0.25,
                expected_file=str(fixture_path),
                expected_scene=scene.name,
            )
        finally:
            bpy.ops.object.mode_set(mode="OBJECT")
        if edit_mode_report.get("ok") is not False:
            errors.append(f"edit-mode-rejected: expected ok=false, got {edit_mode_report}")
        edit_rows = edit_mode_report.get("objects", []) if isinstance(edit_mode_report, dict) else []
        edit_by_name = {
            row.get("object"): row
            for row in edit_rows
            if isinstance(row, dict) and row.get("object")
        }
        edit_quoted = edit_by_name.get(QUOTED_OBJECT_NAME)
        if not isinstance(edit_quoted, dict) or edit_quoted.get("ok") is not False:
            errors.append(
                f"edit-mode-rejected: expected quoted object structured error, got {edit_quoted}"
            )

        final_hash = _sha256(fixture_path)
        if final_hash != hash_before_reports:
            errors.append("final: fixture hash changed after all read-only reports")
        result["fixture"]["blend_sha256_after_reports"] = final_hash  # type: ignore[index]
        result["checks"].update(  # type: ignore[union-attr]
            {
                "read_only_reports": not any("changed the in-memory scene/context state" in error for error in errors),
                "saved_file_hash_unchanged": final_hash == hash_before_reports,
                "analytic_bounds_checked": True,
                "unit_modes_checked": ["METRIC_CENTIMETERS", "NONE", "EXPLICIT_0.25"],
                "invalid_name_scope_checked": True,
                "mode_and_identity_checked": True,
            }
        )
    except Exception as exc:
        errors.append(f"fixture setup/runtime failure: {type(exc).__name__}: {exc}")
        errors.append(traceback.format_exc())

    result["ok"] = not errors
    result_path = run_directory / "fixture-result.json"
    _write_json(result_path, result)
    print(f"BLENDER_MEASUREMENT_FIXTURE_RESULT={result_path}")
    print(f"BLENDER_MEASUREMENT_FIXTURE_BLEND={result.get('fixture', {}).get('blend_path', '')}")
    if errors:
        print(f"BLENDER_MEASUREMENT_FIXTURE_OK=false errors={len(errors)}")
        return 1, result_path
    print("BLENDER_MEASUREMENT_FIXTURE_OK=true")
    return 0, result_path


def main() -> int:
    try:
        output_root = _parse_output_root(sys.argv)
        exit_code, _ = _run(output_root)
        return exit_code
    except Exception as exc:
        # Argument/setup failures happen before a run directory exists.  Keep
        # the stderr/stdout diagnostic concise; normal run failures have a full
        # fixture-result.json from _run().
        print(f"BLENDER_MEASUREMENT_FIXTURE_OK=false error={type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

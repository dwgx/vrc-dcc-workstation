# Read a mesh measurement receipt

Use for an authorized World/avatar dimension check. The optional
[measure_blender_mesh.py](../../../scripts/measure_blender_mesh.py) reads explicitly
named mesh objects in the current Blender scene/view layer. It uses evaluated
mesh vertices and their world transform, including parents. It does not save
the scene, change modes/selections or connect to MCP.

## Run against the intended document

Use the current project's authorized Blender route. For an independent file
check, follow [DCC instance routing](dcc-instance-routing.md): select the installed
executable, use task-owned child settings/output paths and preserve other writers.

```text
blender --background --factory-startup --disable-autoexec /absolute/fixture.blend --python-exit-code 1 --python /absolute/station/scripts/measure_blender_mesh.py -- --object "Door A" --expect-file /absolute/fixture.blend --expect-scene Scene --output /absolute/new-receipt.json
```

Resolve example paths to actual authorized files. Load the file before the script.
Set BLENDER_USER_RESOURCES, BLENDER_USER_CONFIG, BLENDER_USER_SCRIPTS,
BLENDER_USER_EXTENSIONS and BLENDER_USER_DATAFILES to task-owned directories only
in that child when isolating settings. Disable automatic file scripts for a
file-only read unless the task explicitly requires and authorizes them; record
evaluation differences for assets dependent on scripts/drivers.

Repeat `--object` for another mesh. The output parent must exist; existing output
files are preserved, so choose a new path for another observation. Optional
expected-file/scene checks reject a mismatch before measuring. Unspecified
expectations are not verified. Unsaved scenes remain unsaved. Names are dictionary
lookups, never interpolated Python code.

The callable `build_report(bpy, names, ...)` also works through an already
authorized local Blender execution route. It does not establish a particular
MCP addon's background or multiple-instance support.

## Interpret the receipt

- Identity: PID, Blender version, current file, saved/dirty flags, scene, view
  layer and frame. This is in-memory identity, not a writer lock or content hash;
  a saved file can differ from unsaved changes.
- Geometry: vertex count, object-local AABB and world-axis-aligned AABB in Blender
  units. World extents use transformed evaluated vertices, rather than rotating
  only the corners of an already enlarged box.
- Units: `METRIC`/`IMPERIAL` use the declared scene scale as meters per Blender
  unit. `NONE` leaves meter results null. `--meters-per-unit` explicitly overrides
  and records the conversion. Neither setting proves scale after engine import.
- Scope: evaluated mesh vertex stream at the recorded frame/view layer; instances
  are not independently enumerated. Non-mesh, absent, out-of-layer, edit-mode and empty objects return
  errors. No mode changes are made to obtain a result.
- Outcome: `ok` means all requested reads succeeded. Failed objects retain an
  error alongside successful rows. CLI status is 0 for successful reads, 1 for
  measurement/identity failure, 2 for output/runtime setup failure. Keep the log.

For a World door or prop, record the desired clearance separately. Compare local
and world extents, then read back dimensions in the authorized Unity project
after import. Usable clearance requires the intended colliders, player/avatar
and interaction test. AABB extents do not measure an empty opening, true mesh
volume, navigation or a VRChat performance rank. Follow
[World production](../../../docs/WORLD_PRODUCTION.md) for client/multiplayer
checks. Avatar tasks can share this geometry method with their own SDK context.

## Validation and sources

`python tests/test_blender_measurement.py` checks coordinates, units and invalid
inputs without Blender. The optional
[Blender fixture](../../../tests/blender_measurement_fixture.py) creates its own
objects and saved file in a supplied directory. Run it only in an isolated
factory-startup process, never in an existing production session:

```text
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python /absolute/station/tests/blender_measurement_fixture.py -- --output-root /absolute/fixture-output
```

Use the installed version's help/API:
[Object](https://docs.blender.org/api/current/bpy.types.Object.html),
[dependency graph](https://docs.blender.org/api/current/bpy.types.Depsgraph.html),
[unit settings](https://docs.blender.org/api/current/bpy.types.UnitSettings.html).
Comparing [Copilot's measurement tool](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/measurement_tools.py)
motivated explicit file/unit/space evidence. This standalone reader does not
replace that repository, repair its connection cache or install another bridge.

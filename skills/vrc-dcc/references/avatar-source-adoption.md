# Reuse Blender Copilot's Avatar work

Use when turning existing Avatar tools and research into a concrete improvement.
These are implementation candidates, not shipped adapters or Unity validation.
Keep working Blender Copilot and project-owned tool routes available while
testing an extension.

Observations below refer to
[Blender Copilot revision d3b71e9](https://github.com/dwgx/blender-copilot/tree/d3b71e9e4d09b70f58f0d17a104932c63970cf79).
Recheck changed source paths with [upstream-updates.md](upstream-updates.md)
when adopting a newer version. Its Avatar modules are implementation material,
beyond a catalog of Blender commands.

## Connect expression blueprints to actual consumers

`vrc_generate_expression_menu` in
[vrc_tools.py](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/vrc_tools.py#L1532)
produces `items`, a parameter dictionary and a memory summary. The
[Unity consumers](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/unity_tools.py#L395)
expect `controls` and a parameter array with `name`, `valueType`, `defaultValue`,
`saved` and `synced`. Axis controls and nested `sub_items` also need explicit
consumer support; renaming `items` to `controls` alone loses semantics.

A useful first slice is an offline adapter that keeps the original blueprint,
emits the consumer's parameter JSON and reports unresolved menu dependencies.
Record Saved/Synced choices as policy/input and detect conflicting parameter
definitions before a dictionary silently replaces one. Distinguish converted
JSON from generated Unity assets. Preserve axis controls and submenu semantics
in the intermediate result when the current consumer cannot yet generate them.

Validate type/default conversion, conflicting names, axis parameters and nested
menus with small fixtures. Then have the authorized Unity writer create/read
back a disposable asset and compare actual fields. Check current
[parameter rules](https://creators.vrchat.com/avatars/animator-parameters/) and
[menu/control rules](https://creators.vrchat.com/avatars/expression-menu-and-controls/)
when implementing budget/control validation. Authoring estimates do not replace
the final generated avatar's parameters.

## Check viseme deformation and the selected face mesh

The source offers template creation, MMD mapping and base-shape generation.
Compare its
[viseme operations](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/vrc_tools.py#L497),
[constants](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/vrc_constants.py#L263)
and [pipeline](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/pipeline_tools.py#L118):
some generated names use different case, and templates can create names without
vertex deformation. Name presence alone does not demonstrate usable lip sync.

Add a read-only receipt for the explicitly selected mesh: original names,
proposed alias mapping, missing/ambiguous entries and vertex deltas from Basis.
Distinguish a neutral/silence shape from an unexpectedly empty speaking shape.
Preserve the project's actual descriptor mapping; do not automatically rename
an existing avatar to match one tool's naming convention.

An isolated Blender fixture should contain empty/nonempty shapes and ambiguous
aliases. Unity readback should name the intended face renderer and descriptor
mapping. Visual/Play lip-sync acceptance follows the data checks separately.

## Carry export evidence across the Blender/Unity boundary

Existing [FBX export](https://github.com/dwgx/blender-copilot/blob/d3b71e9e4d09b70f58f0d17a104932c63970cf79/src/blender_copilot/vrc_tools.py#L996)
already provides settings and pipeline support. Extend it with source object/
armature identity, selected settings, output path, size and hash. Use structured
path arguments when constructing scripts so quotes and non-ASCII paths survive.
Preserve selection/context when no permanent change is required.

Test a disposable skinned mesh, armature and shape keys. Reimport into a clean
Blender scene to check exported contents; separately read Unity's ModelImporter,
Humanoid result, bones and blend-shape names. File creation or Blender reimport
does not prove Unity/SDK or VRChat client acceptance.

## Let the resource library serve these slices

[vrc-mod-guide](https://dwgx.github.io/vrc-mod-guide/) can route an actual task by
Avatar/World domain, operation, toolchain, platform and content type. Embedded
guides contain readable articles; video metadata and archived-post pointers
identify candidate sources. Historical quality labels are catalog metadata,
not current technical validation.

For a selected method, record the content actually read, source revision/date,
tool versions, inputs/outputs, working example and failure conditions. Return a
small reusable lesson and reproduction with the project result. Keep the broad
catalog for discovery; promote a method into a skill/tool when it changes useful
behavior and has appropriate evidence. See [source-learning.md](source-learning.md).

Shared World/Avatar work can reuse the existing
[mesh measurement reader](mesh-measurement.md) and
[material workflow](material-production.md). Geometry measurements, UV/material
quality and final engine behavior remain separate acceptance questions.

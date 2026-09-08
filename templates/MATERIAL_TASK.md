# Material task (copy into the project's private task pack)

Use with [material-production.md](../skills/vrc-dcc/references/material-production.md).
Keep an existing project brief if it already captures these decisions. Fill
relevant fields; leave genuinely unknown values explicit instead of guessing.

```yaml
task_id: EXAMPLE-MATERIAL-001
domain: world | avatar
outcome: concrete surface and intended improvement
role: repeating_surface | uv_atlas | unique_surface | decal
deliverable: design_reference | base_color_candidate | material_set
target:
  mesh_and_uv_revision: project asset IDs / hashes / current revision
  material_slots: intended assignments
  unity_and_pipeline: installed version and render pipeline
  shader_and_version: exact shader / package / variant
  platform: intended client platform
references:
  geometry_and_camera_views: paths, measurements, units
  fixed_constraints: geometry / openings / fit that must be preserved
  permitted_changes: explicit design freedom
surface:
  coverage_per_repeat: physical units, or not_applicable for an atlas
  uv_direction_and_padding: island orientation / bleed / mirroring
  viewing_distances_and_poses: relevant close, distant or deformed views
outputs:
  native_dimensions: desired pixels; record actual delivered pixels separately
  channels: slot -> source file/channel/encoding/default/derivation
  normal_convention: producer convention and verification method
  alpha_purpose: transparency | smoothness | mask | unused
  original_and_derived_paths: preserve source bytes; name intentional revisions
import_plan:
  color_and_data: sRGB / linear / normal-map type by file and slot
  sampler_and_platform: wrap / mip / filtering / compression / size overrides
scope:
  producer_and_owned_paths: who writes which outputs
  engine_writer: current project writer, or engine work not in this assignment
```

Define the checks before sending:

When geometry measurements are needed, the optional
[mesh measurement reader](../skills/vrc-dcc/references/mesh-measurement.md) can
record named Blender mesh bounds, current file/scene and units. Link the receipt
under geometry references; keep desired clearance and engine scale checks separate.

| Criterion | Method/reference | Result and evidence |
|---|---|---|
| File format and native size | Decode originals; optional image inspector | observed / deviation / unknown |
| Surface role | Repeated swatch, actual UV mesh, or target decal placement | observed / deviation / unknown |
| Fixed geometry / camera constraints | Named views and measured references | observed / deviation / unknown |
| Channels and import | Actual shader options, imported asset readback | observed / deviation / unknown |
| Appearance and use | Relevant lighting, distance, poses, target client | observed / deviation / unknown |

Keep production status, these observations, design acceptance and engine test
status distinct. A non-applicable check should state why. For browser work,
add this brief to [WEB_TASK.md](WEB_TASK.md); preserve the actual prompt and
conversation/send state using its existing receipt format.

`deliverable` describes this material task's outcome; it does not add an
`artifact_class` to WEB_RESULT. A browser color request uses
`base_color_candidate`; keep channel authoring and engine integration in the
project's material receipt, with their own evidence.

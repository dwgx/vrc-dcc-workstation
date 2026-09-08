# Material production for Worlds and avatars

Use for a material brief, candidate review, or shader import task in either
domain. Fill only relevant fields in [MATERIAL_TASK.md](../../../templates/MATERIAL_TASK.md).
Keep the project's geometry, UVs, art direction and installed shader authoritative.

## Choose the surface before the image

| Intended use | Supply to the producer | Check on the result |
|---|---|---|
| Repeating wall, floor or fabric swatch | Physical coverage per repeat, direction, scale reference, intended viewing distances | Neighboring repeats, opposite edges, directional continuity and repetition at the intended scale; later check mips and oblique views in-engine |
| Furniture or avatar UV atlas | Mesh/UV revision, island layout, assigned material slots, orientation and padding needs | Actual mesh with that UV revision, island seams/bleed and direction; poses for deforming surfaces |
| Unique surface or decal | Target surface/UVs, placement, bounds and transparency purpose | Placement, borders and blending on that surface |

A failed 2-by-2 repeat does not disqualify an atlas. A seamless swatch does not
establish that it fits an avatar UV layout. Do not infer intended use from a
filename or from successful decoding.

For image-led modeling, attach measured geometry and camera references. Mark
fixed openings, silhouette and dimensions separately from permitted design
changes. Compare each required view; apparent agreement in one perspective is
not a scale or clearance measurement. Keep room circulation and avatar fit
checks specific to their respective domain.

## Describe channels for the actual shader

Record Unity version, render pipeline, shader name/package version, slots,
keywords and relevant material options before packing channels. For **Unity
2022.3 Built-in Standard, Metallic workflow**, metallic uses R; smoothness can
use Metallic Alpha or Albedo Alpha according to the selected source. The
separate Occlusion slot expects G. An unused G in a metallic texture is not
automatically AO: assigning a zero-filled G there can darken indirect lighting.
See the [Metallic manual](https://docs.unity3d.com/2022.3/Documentation/Manual/StandardShaderMaterialParameterMetallic.html),
[Smoothness source](https://docs.unity3d.com/2022.3/Documentation/Manual/StandardShaderMaterialParameterSmoothness.html)
and [official 2022.3 Inspector declarations](https://github.com/Unity-Technologies/UnityCsReference/blob/2022.3/Editor/Mono/Inspector/StandardShaderGUI.cs).

Do not carry this packing into lilToon, a custom shader or another render
pipeline by name alone. Check the installed shader and its
[author's documentation](https://lilxyzw.github.io/lilToon/). Record what each
slot actually samples and what a missing texture/default channel means.

For example, lilToon **2.3.4**'s reflection path samples the R channels of
`_SmoothnessTex` and `_MetallicGlossMap` separately when their features are
enabled; supplying Standard's smoothness-in-A texture does not reproduce that
mapping. See the [tagged shader source](https://raw.githubusercontent.com/lilxyzw/lilToon/2.3.4/Assets/lilToon/Shader/Includes/lil_common_frag.hlsl).
The author's [shadow settings](https://lilxyzw.github.io/lilToon/ja_JP/color/shadow.html)
describe AO channels for toon shadow layers. Check those controls on the actual
installed variant instead of equating them with Standard's Occlusion slot.

Color and numerical data need different import treatment. Preserve the source
encoding; record sRGB for color textures and linear sampling for numerical masks
where applicable. Use the normal-map importer for normal data and verify its
Y convention against the producer and a known relief/lighting test; do not flip
green from a filename guess. Unity documents
[linear data sampling](https://docs.unity3d.com/2022.3/Documentation/Manual/LinearRendering-LinearTextures.html)
and [normal-map import options](https://docs.unity3d.com/2022.3/Documentation/Manual/texture-type-normal-map.html).

Label channels as authored, measured, baked, generated or derived, with the
derivation parameters. A designed height field can produce internally related
normal/height maps without establishing measured material properties. Color
brightness alone does not establish height or roughness. Use `1 - roughness`
only when the source encoding and destination convention justify that conversion.

## Inspect the original, then its use

Optional image inspection uses Pillow in a task environment:

```text
python -m pip install -r scripts/requirements-images.txt
python scripts/inspect_image_assets.py path/to/base-color.png path/to/normal.png --expect-size 1024x1024 --expect-format PNG
```

The example dimensions are a requested check, not a station texture budget.
Omit expectations when inventorying existing files. The tool reads only named
files, emits JSON and changes no inputs. It hashes the same byte snapshot it
verifies and decodes. Exit 0 means the requested file/frame checks passed;
`--frames all` extends decoding beyond the default first frame. This cannot
certify material role, seamlessness, visual quality or shader compatibility.
Pillow can tolerate some trailing damage, so this is not strict container
integrity validation. An alpha channel/metadata observation also does not
establish that any pixel is transparent.

Keep four measurements separate: original pixel dimensions, physical surface
coverage, actual platform-imported dimensions/format, and runtime memory cost.
An import Max Size is a ceiling, not native resolution or a VRAM measurement.
Check [Texture Importer settings](https://docs.unity3d.com/2022.3/Documentation/Manual/class-TextureImporter.html)
against the selected platform and inspect the imported result.

## Accept each claim separately

Preserve original outputs and revisions. Record production completion, file
checks, criterion-level review, Owner/design decisions and engine evidence
separately. Use observed/deviation/unknown with an evidence pointer for each
criterion; reserve acceptance for the actual reviewer. A color candidate is
not a complete material; a complete set of files is not an accepted engine result.

When an old verdict was too broad, supersede that verdict with its reason and
affected downstream uses. Keep the original files and earlier receipt. Reuse
unaffected work; do not resend a completed generation merely to repair its label.
Use [web-handoff.md](web-handoff.md) for browser send/recovery evidence and
[evidence-layers.md](evidence-layers.md) for subsequent engine checks.

Technical references checked 2026-09-08. Versioned online documentation does not
prove the installed patch version or this project's rendered result.

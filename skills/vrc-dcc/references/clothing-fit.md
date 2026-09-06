# Clothing fit (MA merge ≠ adapted outfit)

Load with [clothing-menu.md](clothing-menu.md) when the job is 加衣服 / 穿上胸不对 / 骨骼对不上 / 衣服穿模. **换素体 / 他体服 / fusion:** [clothing-convert.md](clothing-convert.md).

**Stop line:** Modular Avatar Merge Armature parents bones. It does **not** rebuild weights, does not create missing blendshapes, and does not map extra clothing breast bones onto marshmallow. An outfit not authored for **this** mesh is a Blender job. Do not “fix” that with a shop-chart scale or guessed body morphs.

## Two machines

| What you see | Where |
|---|---|
| Menu does not show/hide, wrong colors, sailor body caves in, nipples on the wrong outfit | Unity MA: ObjectToggle / MaterialSwap / ShapeChanger / `FS_GateSailorShrink`. Playbook: clothing-menu. Nipples **through** clothes while dressed: covering-mesh ShapeChanger + marshmallow LimitCollider, not outfit Int. |
| Covering SC already max-flatten on the body but the dressed mesh still shows nipples or a chest hole | **Not Unity morph.** Dump nipple-key max |delta|. If all < 0.01, stop — VertexFilterByShape on those keys will not hide basis nipples. Migrated cloth / cutout → clothing-convert + Blender. Do not another ShapeChanger. |
| Hips/Chest world delta ≈ 0 after merge, but chest still clips or ignores 棉花糖 | Extra clothing bones (`Breast_L.002`) and blendshape **name** mismatch. Unity can remap BSS + BoneProxy. Weights still Blender. Marshmallow/SPS/PCS: [marshmallow-erp.md](marshmallow-erp.md). |
| Mesh floats, elbow twist, crotch gap, fingers in cloth after merge | Bind pose / weights. **Blender + CATS 5.2**, then new FBX. Stop in Unity. |
| Nameplate / handheld / dropped panty at the feet after instance | `BoneProxy` KeepWorldPose at world origin, or constraint weights 0 | [clothing-convert.md](clothing-convert.md) stop 10–11. Pose in Edit. Do not hang generic SKUs |
| Vendor palette folder has 3 mats, menu has 6 radios | Incomplete pack. Do not invent swaps. Leave unmapped slots on the default palette or hide that radio. |
| Shop shoes clip when the shop outfit hides | Often a child of the shop-original root. Hiding that root hides the shoe. Do not add body morphs the vendor clip did not drive. |

## Edit dump (named `vrc_pose_bounds` / `vrc_audit`, no Play)

Resolve MA references with `AvatarObjectReference.Get(component)`, not `FindPropertyRelative("targetObject")` (false missOT=0).

1. **Wear:** outfit Int ObjectToggle paths actually `Get()` to live objects. Last ObjectToggle in the clothes menu wins. Whole-suit must hide shop original, other outfits, default underwear, and outfit-specific extras. Turning the other outfit **OFF** sets `Clothes=0` (VRC). Mesh restore is the shop-original OT; shop FX **Bools** need Idle ParameterDriver or they stay 0.
2. **Shrink:** covering outfits must zero shop shrink shapes on the body SMR. `Clothes>0` still needs a gate if shop FX keeps playing after the shop mesh hides.
3. **Breast shapes on the clothing SMR** vs **body rest**. Dump both. Remap names (example: clothing `Breast_big(limit)` vs body `Breast_Big_____胸_大(mizuki)`). Do not invent keys.
4. **Bone names:** dump this armature. Extra clothing-only bones after merge: names on the clothing armature that are not on the body. `Breast_L.002` vs body `Breast_L.end` is the usual chest-follow miss.
5. **Empty SMR** (`sharedMesh==null`, 0 tris): disable renderer. Do not leave a missing-mesh slot for SDK Review.
6. **Materials:** `NULL _MainTex` on `*metal*` / lilToon metal is often OK. `NULL` on cloth/bandage/sleeve-sub is a bug — copy albedo from the sibling piece in the same palette.

## Unity-side fixes (allowed)

- **BlendshapeSync remap:** `Blendshape` = body `Breast_Big_____胸_大(mizuki)`, `LocalBlendshape` = clothing `Breast_big(limit)`. Keep `Breast_small` 1:1. Do not bind two body shapes onto one local shape.
- **BoneProxy** `AsChildKeepWorldPose` on extra `Breast_L.002` / `Breast_R.002` → body `Breast_L.end` / `Breast_R.end` (or `.001` if `.end` is missing). Do not `AsChildAtRoot` (flattens the clothing chest).
- **ShapeChanger Delete** vendor 胸寄せ/脚趾/足背/脚踝/小腿 on the **outfit root** is correct. Do not copy those onto a MenuItem.
- **MeshCutter** only on the clothing mesh, never on a MenuItem, never on the body SMR for “make room”.

## Blender-side (stop and say so)

Humanoid names must match **this** armature before export. CATS 5.2 vendor zip only if the job needs it. Weight-transfer extra breast chains onto the live breast bone. Do not expect a second Merge Armature to fix a cage authored for a different chest.

## Typical CN shop folders

New packs often land in `Assets/衣服`. Menus: `菜单/衣服`. Next outfit Int is **whatever MAP says is free** — do not copy another body's numbering. Whole-suit first. USB: `python maps/query.py library --fusion` before Booth. One fusion example: [examples/composite-avatar.md](examples/composite-avatar.md).

Session: [dcc-session.md](dcc-session.md). Menus/bits: [clothing-menu.md](clothing-menu.md). Marshmallow/SPS/PCS: [marshmallow-erp.md](marshmallow-erp.md).

# Clothing menus (load on demand)

Full playbook: [`docs/CLOTHING_MENU.md`](../../../docs/CLOTHING_MENU.md) · 中文 [`docs/i18n/zh-CN/CLOTHING_MENU.md`](../../../docs/i18n/zh-CN/CLOTHING_MENU.md).

When the job is 穿脱 / 换色 / 轮盘 / 叠加件 / expression bit budget. **Wear / chest / bone fit first:** [clothing-fit.md](clothing-fit.md).

0. Live map: gitignored `maps/<avatar>/MAP.md` (**确定** wins). New body: [`maps/templates/AVATAR.md`](../../../maps/templates/AVATAR.md). USB shelf: [`maps/library/README.md`](../../../maps/library/README.md) then `python maps/query.py library` before Booth. Do not link clone-owner MAP files from the public skeleton.

1. Three layers: outfit Int, strip Bools, color Ints. SubMenus get **empty** parameter names.
2. 8 controls per VRC page → first page + `更多`.
3. Never reuse one Int for two radios (围裙 vs 蝴蝶结).
4. Sync strip Bools; `isSynced=false` accessory colors if 256 is tight.
5. Drive MA in the Editor (ObjectToggle / MaterialSwap / MaterialSetter). Do not YAML-edit the avatar prefab. If *this* avatar already uses lilycalInventory or DressingTools for clothes, dump that chain — do not migrate to MA MenuItem just to match this playbook. Station default for CN shop radios is still MA.
6. Nipples — two different bugs; do both on **every** 改模. Detail below.
7. Strip Bools: scene rest **OFF**, ObjectToggle `Inverted=false` + `Active=true` (same as 内衣). Do not inverted-hide rest-ON pieces — NDMF XOR-rewrites rest and 穿脱 becomes a no-op.
8. If clothes have **no** `Breast_small` and the body default is 100 **and marshmallow is not using the small rest**: ShapeChanger Set body `Breast_small=0` on the clothing meshes can fill baggy tops. **With marshmallow blend 0 / body `Breast_small=100`:** do **not** Set 0 — that enlarges the body past the small collider and pokes nipples/chest through cloth. Vendor: body chest key slightly **smaller** than clothes. Do not MeshCutter breasts on a MenuItem. Shop FX shrink clips often **keep running** after the shop mesh hides — zero those shapes on covering outfits **and** drive the shop Bools off while `Clothes>0`. **Idle (`Clothes==0`) must ParameterDriver those Bools back to the MA defaults** or the saved zeros stick after the other outfit is turned OFF (VRC Int Toggle OFF → `Clothes=0`; ObjectToggle restores the shop mesh, but FX still thinks shrink is on). Do not try to make Toggle OFF leave a removed Int value — VRC cannot do that.
9. Two ObjectToggles on `Bra`/`Pants`: last in hierarchy wins. Keep 默认内衣 above added outfits (白/黑 hide). Udon is worlds-only; avatar clothing is Expression Parameters + FX.
10. Do not add body blendshapes (`Foot_heel_OFF`, extra shrink) to clothing clips the vendor clip did not drive. Rest-OFF meshes are not missing pieces. Default-off gizmos need a MenuItem.
11. Token: [token-budget.md](token-budget.md). One Editor dump: [editor-reports.md](editor-reports.md). Bits: [params-256.md](params-256.md). MenuItem `isSynced=true` ORs away MA `localOnly`.

## Nipples through clothes (every 改模)

`Nipple_On=0` on the body SMR does **not** mean the rest mesh has no nipple geo. Some shop bodies keep protruding nipples on the basis. Marshmallow jiggle then pokes them through thin tops. Dump the live nipple key names and weights before guessing. A fusion example with four keys: [examples/composite-avatar.md](examples/composite-avatar.md).

| Lane | When | Wiring |
|---|---|---|
| Covering mesh (dressed) | Top / outer / bra / outfit root **active** | **Non-inverted** ShapeChanger on that **mesh** (not the outfit Int): flatten the live nipple keys on the body SMR. |
| Bra strip (undressed) | Bra / 内衣 MenuItem **off** | **Inverted** ShapeChanger on the **MenuItem**: Set `Nipple_On=100`, `Nipple_Up=100`, `Nipple_Small=0`. Default-ON keeps rest flattened. |
| Outfit Int | Never | Blocks 全脱 (nipples stay forced 0 when every piece is off). |
| Inverted SC on rest-OFF `FS_Bra` mesh | Never | Applies whenever that mesh is hidden → sailor + other outfits leak nipples. |
| **Stop Unity SC** | Edit rest already `Nipple_Small=100` on `Body_b` **and** covering SC targets `Body_b`, but world still shows nipples / chest hole | **Not a morph miss.** Triage: (1) neckline/cutout = cloth doesn’t cover → Blender weights / MA overall scale from **measured** Head/arm, not another SC. (2) poke only while walking = marshmallow LimitCollider. (3) ass+pussy+chest together = migrated outfit, `clothing-convert.md`. Do not raise Small past 100, do not second BSS. |

**Calibrate, don’t stamp 100.** Dump body nipple weights **and** `ChangedShape.Object` target **and** per-key max vertex delta (`GetBlendShapeFrameVertices`). If target is the clothing mesh, the SC is a no-op. If the flatten key is already maxed on the body, more ShapeChanger will not hide nipples in a gap. If **every** nipple key max |delta| is **< 0.01**, the morphs do not move the basis geo — **stop Unity**. Do not VertexFilterByShape those keys. Do not MeshCutter in the same turn as that dump. Tell the Owner: accept the neckline, or Blender (delete nipple tris / retopo cloth). Never MeshCutter on a MenuItem.

Also:

- Do **not** ShapeChanger body `Breast_small=0` on clothing meshes while marshmallow rest is small (blend 0). That **enlarges** the body under clothes (opposite of vendor: body chest key slightly **smaller** than clothes, e.g. 90 vs 100). Maid BSS already copies `Breast_small` 1:1.
- Marshmallow walk-clip: raise `_buffer_limit_colider_position` (LimitColliderPosition, vendor priority) before cutting MaxSquish. [marshmallow-erp.md](marshmallow-erp.md)
- Prove in **Edit**: `Body_b` `Nipple_On`/`Up`/`Small` after toggling 内衣/胸罩. Do not wait SPS Play.

Outfit-specific colors, removed SKUs, and “skip nipples” rulings live in `maps/<avatar>/` + CURRENT. Do not copy another body’s Clothes Int into this prefab.

## Shop original vs added outfits (every 改模)

One MAP node + one REVIEW row per outfit. Do not treat them as one ObjectToggle.

| Lane | Typical | Restore / hide | Fit leftover |
|---|---|---|---|
| **Shop original** | Body FX Bools. `Clothes=0` | Idle must ParameterDriver those Bools **back to defaults**. OT restores the mesh; FX does not. | Shoes often under this root; do not guess extra body morphs |
| **Added whole-suit** (black maid, gothic) | Outfit Int + OT, no strip bits | Int OFF → 0 (shop). Do not pay strip bits twice | Extra unmatched bones (`Breast_*.002`, `Butt_*_end`) → BoneProxy KeepWorldPose or Blender. Merge Armature ≠ fitted |
| **Added strip** (white maid) | Int + synced Bools, scene rest **OFF** | Same OT convention as 内衣. Last OT wins → default underwear **above** | Nipple covering SC on the **mesh**, not the Int |
| **Default underwear** | Rest-OFF `Bra`/`Pants` | Not missing pieces | Two bras if sailor Bool stuck 0 |

New outfit: instance, turn **on in Edit**, Owner looks, **then** bits. Coverage: `python maps/review.py coverage <avatar>`.

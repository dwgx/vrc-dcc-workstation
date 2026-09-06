# Marshmallow vs clothes vs SPS/PCS

Load with [clothing-fit.md](clothing-fit.md) when the job is 棉花糖 / 胸跟不住 / PCS胸孔 / SPS孔.

**Stop line:** Marshmallow is an **NDMF bake**. In Edit, stock `Breast_L`/`Breast_R` PhysBones are **off** and the jiggle lives under the marshmallow Dummy. That is not a broken install. Do not enter Play just to see jiggle if VRCFury haptic bake hangs (>60s → exit, do not save).

## What marshmallow does at bake

Preset paths are **per body**. Dump the live marshmallow Setup. Stock Rurune collider names may **not** exist on a fusion armature — then breasts clip arms until you slot body colliders. Do not borrow outfit Physics (they die when the outfit is off). One fusion fill-in: [examples/composite-avatar.md](examples/composite-avatar.md).

Do **not**:

- Parent SPS/PCS sockets to marshmallow Dummy, `Adjust_Breast_*`, or `PhysBone_L1`.
- Parent SPS/PCS Breast/Boobs to `Breast_L` (hole jumps with one breast).
- Raise `_breast_blendshape` while the body rest is already on the small chest key. Blend 0 = small collider. Blend 100 fights a small rest mesh.
- Turn `_marshmallowPBEnabled` on if a marshmallow menu target already exists (duplicate menu).
- Point marshmallow colliders at **clothes** Physics. Put colliders on the **body** armature.

## Collider paths

Preset collider names are **per body**. If `_PhysBone_collider[]` is all null, slot colliders on the **body** armature. Do not copy numbers from an outfit Physics object. Fusion example: [examples/composite-avatar.md](examples/composite-avatar.md).

## SPS / PCS — keep the holes on torso bones

| Socket | BoneProxy (KeepWorldPose) | Do not |
|---|---|---|
| SPS Mouth / PCS Mouth | `Head` | marshmallow Dummy |
| SPS Breast / PCS Boobs | `Chest` | `Breast_L` / `.end` |
| SPS Pussy Ass Dick / PCS Pussy Ass | `Hips` | Chest |
| ぱいたっち L/R | `Chest/Breast_L` and `Breast_R` | Dummy paths |
| Extra clothing breast bones | body `Breast_*.end` | `AsChildAtRoot` |

PCS configurator `Find`s `Penetration Contact System/Target Objects/<PCS Target> *` in **Edit**. BoneProxy must stay on those objects; do not move them in the Hierarchy. Bake reparents. Rest poses are **per body** — dump, do not copy another avatar. Dick size is a vendor Int; do not invent euler “fixes”. No DPS. Stack SPS → PCS.

PCS menu clicks still need **MA Parameters on `Penetration Contact System`** before NDMF.

## Clothes (Unity vs Blender)

Same as clothing-fit: BSS `Breast_Big_____胸_大(mizuki)` → clothing `Breast_big(limit)`, keep `Breast_small` 1:1. Extra `Breast_L.002` → `Breast_L.end` KeepWorldPose. Weights still Blender. Convert lanes: [clothing-convert.md](clothing-convert.md).

Vendor **貫通防止**: `_breastInterference_BreakPreventionCollider` enables bake `PhysBone_Limit_for_Clipping_*`. Reduces breast-through-mesh; **outfit cloth can still clip** on jiggle. Do not promise zero. Dump live values into `maps/<avatar>/`.

Official trouble (clothing clips through): https://wataame89.github.io/documents-wataameya/en/marshmallowPB/trouble/

| Lever (vendor order) | Field on `marshmallow_PB_MA` | Do |
|---|---|---|
| LimitColliderPosition (priority for squish-through) | `_buffer_limit_colider_position` 0→1 shallower | Raise toward 1 before cutting MaxSquish |
| MaxSquish (normal-pose squish) | `_PhysBone_Max_Squish` | Lower only after LimitCollider |
| Body chest key slightly **smaller** than clothes | do **not** Set body `Breast_small=0` on clothing meshes | dump rest |
| EX menu off squish / normal PB / MM off | player toggle | last resort |
| Migrated outfit (shoes/ass/chest/hair together) | [clothing-convert.md](clothing-convert.md) | not another BSS, not a chart scale |

Nipple geo still pokes thin cloth after flatten=0: covering-mesh ShapeChanger. [clothing-menu.md](clothing-menu.md).

VRC **AudioSource cap is 3 simultaneous**. Performance rank “8 sources” is not the runtime cap. Do **not** leave one-shot / nade `playOnAwake` occupying slots. PCS vendor `pcs/isEnable` default is often **0**. PCS SFX `AudioSource.clip` **null in Edit** is bake-time assign, not broken audio. Live defaults belong in MAP.

Motchiri / body shaders: bind to the **body** SMR, never the face/eye mesh.

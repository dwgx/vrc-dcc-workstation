# Clothing body-convert (MA merge ≠ adapted outfit)

Load with [clothing-fit.md](clothing-fit.md) when the job is 换素体 / 他体服 / clothes authored for a **different** base onto **this** live mesh. Menus stay [clothing-menu.md](clothing-menu.md). Chest physics: [marshmallow-erp.md](marshmallow-erp.md). Agent mistakes: [vrc-agent-pitfalls.md](vrc-agent-pitfalls.md).

Identify **source body** and **target body** before any scale. A fusion, a stock base, and a different Booth SKU with a similar display name are three jobs. `wear_fusion` in the USB catalog means a listed prefab heuristic, not that Edit already fit. Worked example: [examples/composite-avatar.md](examples/composite-avatar.md).

## Stop lines (cannot waive in chat)

1. **MA Merge Armature parents/retargets bones by name.** It does not rebuild weights, does not create missing blendshapes, and does not map extra clothing breast bones onto marshmallow. https://modular-avatar.nadena.dev/docs/reference/merge-armature
2. **Do not default Armature scale `0.95`.** That number is one cell on some shop conversion PNGs, labeled 指標 / 微调整. Prefer the official prefab for **this** target at **scale 1** unless measured.
3. **`neck 1.01` on the chart is a Neck *local scale*, not fusion Head world-Y ~1.01 m.** Do not conflate them.
4. **Read the chart labels.** A PNG named for bases A/B/C is not a third unnamed mesh. Do not Merge a pack for a different named base unless the Owner names that job.
5. **Do not guess `Foot_heel_OFF` (or any body morph) onto a vendor clip that did not drive it.**
6. **Bone Proxy is not the clothing merge.** Exception: leftover extra bones after merge (`Breast_L.002`) → `AsChildKeepWorldPose`. https://modular-avatar.nadena.dev/docs/reference/bone-proxy
7. **CATS 5.2 does not transfer clothing shapekeys onto a different mesh.** `ShapeKeyApplier` = apply selected key to Basis on **that** mesh. Weight transfer is Blender Data Transfer (or Robust Weight Transfer).
8. **Marshmallow vendor: some clothes will clip.** Official trouble is PB/squish tuning, not a weight fix. https://wataame89.github.io/documents-wataameya/en/marshmallowPB/trouble/
9. **Identify source body and target body before any scale.** Fusion ≠ stock base ≠ similarly named Booth SKU.
10. **Handheld / nameplate / dropped-panty props are not clothes merge.** Vendor `BoneProxy` `AsChildKeepWorldPose` keeps **current world pose**. Instantiating the prefab at `(0,0,0)` leaves the mesh at the feet. Pose the proxy to Head / `Right Hand` / `Hips` in **Edit** and dump BakeMesh vs that bone (`vrc_pose_bounds`) **before** the next item. `dRH≈0` means the **wrist**, not a grip — also dump wrist→`Index Distal` length and `handLocal`. Do not use `renderer.bounds` as fit. `AsChildAtRoot` zeros the palm offset. `VRCParentConstraint` `Sources.*.Weight` all `0` means it does not follow. Do not “fix later”.
11. **POLICY `body_token` / require_prefab_path:** no matching prefab → do not Instantiate. Generic world props for other bodies stay off this avatar. A listed prefab whose Hips Y ≠ body Hips is still **not fitted**. Stop, show the Owner, do not stack three SKUs.

## 0. Identity (before Unity or Blender)

| Question | How |
|---|---|
| What body authored this outfit? | Prefab name / `bodies[]` in the USB catalog. Prefer that SKU at **scale 1**. |
| What is the live target? | Measure **Head world Y** and **Hips/Chest**. Write them in `STATE.md`. |
| Same armature names? | Dump this armature vs the clothing armature. |
| Vendor pack for this body? | `python maps/query.py library` then Booth. |

**Stop.** If the pack ships a prefab named for **this** target, instance **that** prefab, scale 1, Setup Outfit.

## 1. Symptom triage (one Edit dump, then pick a lane)

| What you see after Setup Outfit / Merge Armature | Lane | Not |
|---|---|---|
| Menu hide/color/shrink/nipple wrong | Unity [clothing-menu.md](clothing-menu.md) | Fit |
| Hips/Chest world delta ≈ 0, chest ignores 棉花糖 or clothing breast shape names differ | Unity **BSS + BoneProxy** | Scale 0.95 |
| Extra bones `Breast_L.002` / `Breast_R.002` after merge | BoneProxy `AsChildKeepWorldPose` → body `Breast_*.end` | Merge Armature again |
| **Shoes in the ground AND clip at feet/ass/chest/hair** | **Migrated outfit.** Measure height. Then MA reset-position **or** Blender | Shoe Y alone; default 0.95 |
| Shoes **only** sink; rest of mesh follows body | Shoe local Y / Floor Adjuster if Owner owns one | Whole Armature scale |
| Hair clips while moving; rest pose OK | Hair **PhysBone colliders on the body** (chest/head capsules scaled to **this** body) | Clothes Physics (dies when outfit off) |
| Mesh floats, elbow twist, crotch gap, fingers in cloth | **Blender weight transfer**, new FBX | Second MA merge |
| Chest clips only when marshmallow squishes / jiggles | Marshmallow trouble (MaxSquish / LimitCollider / 貫通防止 collider). Clothes extra bones still need BoneProxy | Perfect zero-clip promise |
| Covering SC already `Nipple_Small=100` → `Body_b`, nipples still visible | Cloth doesn’t cover (cutout / fusion cage). **Stop Unity SC.** Measure Head/arm or Blender | Stamp Small again; second BSS |
| Vendor palette folder has 3 mats, menu has 6 radios | Incomplete pack | Invent swaps |

GothicLolium-rurune on this fusion (2026-09-02): BSS + BoneProxy + empty spine SMR off **already done**. Remaining multi-region clip is this table’s migrated-outfit lane, not another BSS pass.

## 2. When Unity BSS / BoneProxy is enough

Use when **bone names already match this armature**, Hips/Chest rest delta ≈ 0, and the miss is **names / extra breast bones / marshmallow reparent**.

- **Blendshape Sync:** body `Breast_Big_____胸_大(mizuki)` → clothing `Breast_big(limit)`; keep `Breast_small` 1:1. BSS copies values; **it does not create missing keys**.
- **BoneProxy extra breasts:** `AsChildKeepWorldPose` only. Not `AsChildAtRoot`.
- **ShapeChanger Delete** vendor 胸寄せ/脚趾/足背/脚踝/小腿 on the **outfit root**, not a MenuItem.
- **MeshCutter** on clothing mesh only, never `Body_b`, never a MenuItem.

**Stop and leave Unity** if BSS+proxy still leaves float / twist / multi-region clip.

## 3. When MA “reset position / overall scale” is allowed (still not 0.95)

For outfits **not authored for this avatar**, MA inspector (Setup Outfit) can:

- Reset outfit bone **positions** to the base.
- Optional rotation (can look wrong across DCC).
- Optional local scale (when the **base** bones were scaled).
- Optional **adjust overall scale by arm length** (`MergeArmatureInspectorTools.AdjustRootScale`: `targetWingspan / mergeWingspan`). Official: generally recommended for setting up outfits. https://modular-avatar.nadena.dev/docs/reference/merge-armature

**Stop.** Measure Head Y / arm length **on this pair** before clicking. Do not type `0.95`. If already BoneProxy/BSS’d, do not click overall scale as a second “fix” without measuring.

## 4. When shoe Y offset is enough

Only if **the rest of the outfit already follows the body**. Gothic-class (shoes in ground **plus** ass/chest/hair) is not a shoe-Y job. Shoes SMR parented to Hips with hundreds of bones will not move if you translate the `shoes` GameObject.

## 5. When hair PhysBone colliders are enough

Hair/skirt PB swinging into body: colliders on the **body** armature, scaled to this torso. Marshmallow: fusion stock paths `upperArm_L_collider` may be **missing** — put colliders on **body**, not maid `Upper_Arm_L`. Rest-pose hair stuck through the skull is weights, not a collider.

## 6. When marshmallow extra bones are the chest lane

See [marshmallow-erp.md](marshmallow-erp.md). Do not parent SPS/PCS sockets to Dummy / `Adjust_Breast_*` / `Breast_L`. Vendor 貫通防止 is `_breastInterference_BreakPreventionCollider` (enables bake `PhysBone_Limit_for_Clipping_*`). Some clip is expected; do not promise zero.

## 7. When Blender + CATS 5.2 is required

Trigger: bind pose / vertex groups from **another cage**, or MA reset still leaves float/twist/crotch/finger-in-cloth.

Station: Blender **5.2.1**, CATS zip only if this job needs it — `vendors/upstream/cats-blender-plugin-5.2`.

| Tool | Does | Does not |
|---|---|---|
| CATS **Merge Armatures** | Merge two **rigged** armatures; vertex groups by name | Spatial weight paint from body→clothes |
| CATS **Mesh Mode** | Parent an **unweighted** mesh to one bone (hat) | Deforming clothing |
| CATS **Apply Selected Shapekey to Basis** | Bake a key into Basis on **that** mesh | Copy keys onto a different topology |
| Blender **Data Transfer** `VGROUP_WEIGHTS` | Body → clothes weights | MA |
| Export FBX | Humanoid **names = this target armature** before MA | Unity rebuilding visemes |

## 8. Shop conversion charts (named bases only)

Some Booth shops ship a PNG of Armature scales between **named** bases (labels like 指標 / 微调整). Read **that** PNG if the Owner has it. Do not invent a machine path. Do not treat those three-base numbers as a fusion default.

**Stop.** Chart cells are guidelines for the bases printed on the PNG, not permission to skip weight transfer, not a third unlabeled mesh.

## 9. Clothes authored for base A worn on a different live mesh

1. Use the prefab named for **this** target when it exists, Armature **scale 1**.
2. Setup Outfit → Merge Armature. Dump extra bones vs body armature.
3. §1. If only breast names / `Breast_*.002` → BSS + BoneProxy.
4. If shoes-in-ground **and** feet/ass/chest/hair → **migrated**. Measure Head Y vs a same-base reference **this session**.
5. Marshmallow preset is **per body**. Dump Setup; do not copy another avatar.
6. Finger/toe accessories: MenuItem local + rest-OFF is wiring, not fit. `renderer.bounds` is bind AABB; **BakeMesh**.

**Stop.** Do not invent a new default from HeadY ratios.

## 11. Accessory 看齐 (nails / handheld)

Hands and toes are **two** fits. N anchors are **N** fits. Wiring pass is not this section.

| Step | Do | Fail if you |
|---|---|---|
| 1. List attach points | Every named anchor + nails hand **and** foot BakeMesh | Pose only the right hand / only fingers |
| 2. Pose the **source**, not the constrained child | Move BoneProxy anchors. `KeepWorldPose`. Dump VRC `Locked` + `PositionAtRest`. If the Owner already posed it: dump only. | Translate the inner mesh and leave anchors at the wrist |
| 3. Grip ≠ wrist | Each hand: `Lerp(Hand, Index Distal, 0.55)`, dump BakeMesh vs that point | Score `dRH≈0` as held |
| 4. Skinned mesh | `BakeMesh` vs the nail bed | Trust `renderer.bounds` |
| 5. Parent/child bones | Apply the delta **once** | Parent+child each `+= delta` |
| 6. Mesh GO translate | Moving the renderer transform does **not** move skinned verts | “I moved the renderer so the toes should follow” |
| 7. Stop | Owner looks in Edit | Hide the miss in notes |

A filled fusion pass: [examples/composite-avatar.md](examples/composite-avatar.md). Do not copy another body's world poses.

## 10. Worked example

Do not paste USB paths into the public playbook. Overlay `LIBRARY.md` / `query.py library` names the pack. Migrated-outfit symptoms → §1, then measure, then MA scale **or** Blender.

## Sources

| Claim | Source |
|---|---|
| MA merge ≠ weights | https://modular-avatar.nadena.dev/docs/reference/merge-armature |
| BoneProxy not for clothing; KeepWorldPose | https://modular-avatar.nadena.dev/docs/reference/bone-proxy |
| BSS name remap only | https://modular-avatar.nadena.dev/docs/reference/blendshape-sync |
| CATS 5.2 | blender.md ; `vendors/upstream/cats-blender-plugin-5.2` |
| Shop chart numbers | Owner’s Booth PNG if present; never a hardcoded disk path |
| Per-body Head Y / fusion | `maps/<avatar>/STATE.md` + OWNER.md |
| Marshmallow clip expected | https://wataame89.github.io/documents-wataameya/en/marshmallowPB/trouble/ |

# Clothing menus (Modular Avatar)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/CLOTHING_MENU.md)
<!-- I18N:END -->

Booth / CN avatar shops converge on the same three layers. Rebuild *this* avatar’s shop original to that layout; do not copy another clone’s Int values.

## Three layers

| Layer | VRChat control | Typical param | Network bits |
|---|---|---|---|
| **Outfit** (which costume) | Toggle radio, one Int | `Clothes` = 0 default, 1 white maid, 2 black maid | **8** |
| **Strip** (which pieces) | Toggle Bools, default ON | one Bool per group | **1 each** (sync so others see it) |
| **Color** (look) | Toggle radio, one Int per independent region | `FS_Clothes_Color`, `FS_Apron_Color`, … | **8** if synced; **0** if `isSynced=false` |

Do **not** put leftover parameter names on SubMenu items (`衣服`, `FS`). ParameterAssigner still emits them.

VRChat: **8 controls per menu page**. Split 穿脱 into a first page + `更多`.

## CN shop patterns (what “轮盘” means)

- **套装轮盘**: Int radio, not two Bools. Off-state `0` is the **shop original**, not “empty”.
- **穿脱**: Bools, `isDefault=true`. Use **one** rest convention (same as default underwear):
  - Mesh **OFF** in the scene, ObjectToggle `Inverted=false` + `Active=true` (ON shows it, OFF restores hidden rest).
  - Do **not** use inverted-hide on rest-ON outfit pieces. NDMF computes `InitiallyActive XOR Inverted` and **rewrites** GameObject rest, so OFF restores the new rest and strip does nothing (or starts hidden).
  - Outfit **root** can stay inactive (`Clothes` Int turns the root on). Pieces under it still need rest OFF so strip Bools have a hidden rest to restore.
- **Shop shrink vs added outfit**: body FX often keeps driving shrink Bools after the shop mesh hides. Covering outfits must zero those shapes **and** Parameter-Driver the shop Bools off while `Clothes>0`. **Idle (`Clothes==0`) must Set those Bools back to MA defaults.** VRC Int Toggle OFF sets `Clothes=0`; ObjectToggle restores the shop mesh, but saved zeros otherwise leave shrink on. Do not expect Toggle OFF to leave `Clothes` at a removed Int. Shop FX may also hide default `Bra` while the original outfit is on — two bras if that Bool is forced off. Last ObjectToggle in hierarchy wins; keep default underwear **above** added outfits.
- **Base 内衣 vs outfit 胸罩/内裤**: they are different meshes (`Bra`/`Pants` vs `FS_Bra`/`FS_Panty`). Added outfits often ObjectToggle `Bra`/`Pants` Active=false. Last ObjectToggle in hierarchy wins, so **default underwear must sit above added outfits**. Otherwise 内衣 (default ON) turns base underwear back on under the extra suit.
- **颜色轮盘**: Int + `automaticValue=true` on siblings that share one param. First `isDefault` gets 0, others 1,2,… Values `>1` force Int (8 bits). Two colors can stay Bool (1 bit) if you only need 白/黑.
- **叠加**: extra pieces (wings, tail, bunny ears, bows) are Bools **on top of** the outfit Int. They must ObjectToggle **named meshes**, not the outfit root (the root is already owned by `Clothes`).
- **黑白两套 mesh**: full strip/color on **one** mesh set (white). The other outfit is a whole-suit Int only, until someone pays the bit cost again.

## Bit-saving (do this before adding another Int)

1. **Int radio beats N Bools** for exclusive colors (8 colors = 8 bits either way; Int also exclusive). Two-state (白/黑) → one Bool.
2. **`isSynced=false` / MA Parameters `localOnly`** for colors others need not see (metal, stocking, bow). Strip Bools stay synced.
3. **One MaterialSwap per coordinated palette** (UV1–UV5 From→To on the outfit root) instead of one Int per UV.
4. **Merge metal slots** into one `FS_Metal` (gold / rose / silver) instead of 挂饰 + 腿环 two Ints.
5. **Do not** give SubMenus a parameter. **Do not** reuse one Int for two radios (围裙 vs 蝴蝶结 sharing `FS_Apron` becomes one 16-way radio).
6. Audit `VRCExpressionParameters` **before** bake. Duplicate names (same token as Float+Bool) waste bits and confuse MA.
7. Group strip Bools by what players actually take off (上衣+领+袖褶, not every ribbon bone). One synced Bool per accessory is how a 改模 session burns ~33 clothing bits.
8. **Do not invent body morphs** on clothing clips (`Foot_heel_OFF` on loafer ON/OFF looked like ruined white clothes; vendor clips only toggled the loafer renderer). Fit leftover is Blender / a dedicated shrink clip, not a guessed shape on the toggle.
9. **VRCFury FullController params** must exist as **MA Parameters** on that object **before** NDMF, or `FixupExpressionsMenuPass` clears the MenuItem parameter and PCS/SPS clicks do nothing. Dump leftover VF compressor params; delete names no MenuItem references.
10. One avatar cannot split 256 bits across two SDK uploads. Slim vs full = two published avatars. Size radios (`SPS_DickSize` Int) are 8 bits unless `localOnly`.

Typical budget: accessory colors local; clothes + apron colors synced; strip Bools synced. Stay under 256. Overflow → MAP / params-256 playbook, not a dated overlay note.

## MA wiring (Editor, not YAML)

- Outfit Int: `MenuItem` Toggle, `automaticValue=false`, explicit 0/1/2, `isDefault` on 0. `ObjectToggle` shows that outfit root and hides the others.
- Strip: `MenuItem` Toggle + `ObjectToggle` listing **white** meshes only. Default ON.
- Color: `MaterialSwap` (From/To, `m_root` = white outfit) for whole-suit palettes. `MaterialSetter` (object + material index) for one mesh / one slot.
- **Bows vs apron**: if both setters write `FS_Apron` index 1, they fight. Apron = that mesh’s slots. Bows = `FS_Ribbon*` meshes.
- Nipples (every 改模): **covering mesh** non-inverted flatten on the body SMR. **Bra MenuItem** inverted show. Not on the outfit Int. Not inverted on rest-OFF bra mesh. Flatten=0 is not “no nipple geo”. Do not Set body `Breast_small=0` on clothes while marshmallow rest is small.

Never `EditorUtility.DisplayDialog` from MCP. Human clicks SDK Publish.

## Shop original vs added outfits

Do not treat original shop clothes and Booth add-ons as one ObjectToggle. One MAP node + one REVIEW row per outfit.

| Lane | Typical | Restore | Fit leftover |
|---|---|---|---|
| **Shop original** | Body FX Bools. Outfit `0` | Idle ParameterDriver Bools **back to vendor default**. OT restores mesh; FX does not. | Do not guess extra body morphs on vendor clips |
| **Added whole-suit** | Outfit Int + OT, no strip bits | Int OFF → `0` (shop) | Extra unmatched bones → BoneProxy KeepWorldPose or Blender. Merge Armature ≠ fitted |
| **Added strip** | Int + synced Bools, scene rest **OFF** | Same OT as 内衣. Last OT wins → default underwear **above** | Nipple covering SC on the **mesh**, not the Int |
| **Default underwear** | Rest-OFF `Bra`/`Pants` | Not missing pieces | Two bras if shop Bool stuck 0 |

New outfit: instance, turn **on in Edit**, Owner looks, **then** bits. Board: `python maps/review.py coverage <avatar>`.

## Example menu tree

Do not copy another clone’s Int values. Record *this* avatar in `maps/<avatar>/`. A filled fusion tree: [skills/vrc-dcc/references/examples/composite-avatar.md](../skills/vrc-dcc/references/examples/composite-avatar.md).

Typical CN shop:

```
衣服
  店里原装     Clothes=0
  追加套装
    白         Clothes=1
    黑         Clothes=2   (whole suit only)
    穿脱       Bools on the strip meshes
    颜色       Int / Bool per independent region
```

# Review board (any avatar)

Load at slice end with `vrc-review`, and when the Owner asks what is left / what was already checked. No default character.

MAP (`graph.json` + `notes.json`) is **what exists**. The review board is **what was proven**. New work is unreviewed until a row says otherwise.

## Files

| File | Who writes |
|---|---|
| `maps/<avatar>/REVIEW.json` | Agents/humans. Source of truth. |
| `maps/<avatar>/REVIEW.md` | `python maps/review.py render <avatar>` only. |
| `maps/templates/REVIEW.json` | Copy when a new avatar map folder is born. |
| `maps/<avatar>/MAP.md` | Structure + locked remarks. Not a scoreboard. New avatar: `python maps/init_avatar.py <id>` · [maps/README.md](../../../maps/README.md). |

```
cd <station>/maps
python review.py lint <avatar>
python review.py render <avatar>
python review.py next <avatar>
python review.py next <avatar> --json
python review.py coverage <avatar>
```

`next` is the agent queue: `unreviewed` + `edit` + `blocked`, world-gate first. `--json` is for parsers. Humans Read `REVIEW.md`.

## Status (one per row)

| status | Meaning | Who may set it |
|---|---|---|
| `unreviewed` | New, or never proven. Default for new writes. | Agent after a Unity/Blender change |
| `edit` | Editor dump / ObjectToggle / blendshape / console 0 error | Agent with a path in `evidence` |
| `world` | Owner confirmed **after SDK upload** in VRChat | Agent only if `owner_ok: true` from that chat |
| `accepted` | Known cost. Do not “fix” | Owner lock or playbook |
| `blocked` | Cannot proceed (bits, missing pack, bake hang) | Agent |
| `wontfix` | Owner said skip | Owner |

`gate`: `edit` | `world` | `blender` | `none`. Loco, marshmallow jiggle, PCS sound, SDK bits are `world`. Clothes/nipple rest can be `edit`. Unadapted mesh is `blender`.

Do not write `world` because YAML looked good. Layer names: [evidence-layers.md](evidence-layers.md). `edit` ≈ `UNITY_RESOLVED`. Upload claims need `UPLOAD_CONFIRMED` + `owner_ok`.

## Rules

1. **Same slice as the Unity write.** Upsert the rows you touched. Do not wait for “收尾”.
2. **New gizmo/outfit/menu** → new row (`id` stable, optional `node` = MAP id). `review.py coverage` lists MAP nodes with no row.
3. **Never** `status: world` because YAML or a named dump succeeded. Descriptor still showing shop loco in Edit is not in-world loco.
4. **Failed approach** stays on the row (`notes`) and in the playbook. Example: disabled MA MergeAnimator still bakes.
5. **Do not grow a second constitution in chat.** Durable rules go in this file, `AGENTS.md`, or a skill. Scores still live in `vrc-review`.
6. Evidence may be a string or `{kind, ref, caption}`. Kinds: `dump` | `playbook` | `screenshot` | `note` | `unity` | `world`. Screenshots live under `maps/<avatar>/evidence/` (optional multimodal). Dumps are enough for agents.
7. `python review.py lint` fails `world` without `owner_ok`, and `edit` without `evidence`.
8. **Lessons** (`REVIEW.json` `lessons[]`): failed approaches. Rendered at the top of `REVIEW.md`. Copy a lesson into the playbook if it will hit the next avatar. Do not retry a listed `failed`.
9. Optional `nodes: []` besides `node` so one row covers several MAP ids (coverage uses both).

## Freeze vs queue

If `notes/CURRENT.md` names a freeze file, **do not** mutate Unity because `next` still lists `edit` / `unreviewed`. That queue is for after thaw. Overlay SDK cards stay in `maps/<avatar>/`.

## Clothes: shop original vs added (every 改模)

Put one row per outfit. Lanes (also [clothing-menu.md](clothing-menu.md)):

| Lane | What | Typical proof |
|---|---|---|
| Shop original | Bools on body FX, `Clothes=0` must restore | Idle ParameterDriver + ObjectToggle |
| Added whole-suit | Outfit Int + OT, no strip bits | Int ON mesh on, Int=0 mesh off |
| Added strip | Int + synced Bools, rest-OFF | Each Bool in Edit |
| Default underwear | Rest-OFF is not missing | Hierarchy above other outfits |
| Nipples | Covering non-inverted SC; bra strip inverted on **MenuItem** | Dump the live nipple keys |
| Shrink gates | Shop FX keeps running if only the mesh hides | Zero shrink shapes while Clothes>0; Bools restore on Idle |

Unadapted extra bones (`Butt_*_end`, `Breast_*.002`) are BoneProxy or Blender — say which on the row. Do not mark `edit` “fitted” after Merge Armature alone.

## Public peers (do not install)

Home research stays in gitignored dated notes. Closest open stack is [sentfromspacevr/vrchat-agentic-tools](https://github.com/sentfromspacevr/vrchat-agentic-tools) (toggle-diff + post-build path checker + GM verifier). **Do not** add that Unity package here — it starts a second MCP and writes `.mcp.json`. Steal the *loops* into this board + named dumps. [felixchaos/vrchat-avatar-modding-skill](https://github.com/felixchaos/vrchat-avatar-modding-skill): unadapted clothes → Blender; baked menu/params beat the descriptor. Never agent-upload (`upload_vrchat_avatar` in other MCPs).

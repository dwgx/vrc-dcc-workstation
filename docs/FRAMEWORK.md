# Domain framework (avatar + world)

This is the **underlying split**. It does not implement live `world_*` Editor dumps (that is S01-c). It does not make this GitHub repo a private world product.

A clone-owner **live-test avatar** (any body in `local.json`) is overlay. It is not the public skeleton’s counterpart and not a default character.

## Three layers

| Layer | Responsibility | Now |
|---|---|---|
| **Core** (proposed C#) | Identity refuse tokens, POLICY load, lease-aware stamps, evidence fingerprints | Python: `maps/lease.py`, `maps/evidence.py`, `maps/allowlist.py`, `maps/policy.py` / `world_policy.py` |
| **Avatar adapter** | Named `vrc_*` on `VRCSDK3A` + Modular Avatar | `unity/vrc-dcc-tools` (`VrcDcc.Tools.Editor`) |
| **World adapter** | Named `world_*` on Worlds SDK / UdonSharp | **Not compiled.** Names are proposed. Station CLI: `init_world.py` / `world_handshake.py` / `world_gate.py` |

Do **not** add Avatar SDK or MA to a Worlds project so the avatar adapter compiles. Do **not** add Worlds SDK to an avatar project because a playbook mentioned Udon.

## Station CLI

| Domain | Seed | Handshake | Lease |
|---|---|---|---|
| Avatar | `python maps/init_avatar.py <id>` | `python maps/handshake.py <id>` | `python maps/gate.py <id> begin <review-id>` + `VRC_DCC_JOB_HOLDER` |
| World | `python maps/init_world.py <id>` | `python maps/world_handshake.py <id>` | `python maps/world_gate.py <id> begin <review-id>` + same env |

World maps live at gitignored `maps/worlds/<id>/`. Handshake prints `implemented_world_tools: false`. Allowlist: avatar jobs refuse `world_*`; world jobs refuse `vrc_*`. Both refuse `execute_code` / upload / publish **before HTTP**.

## Proposed `world_*` (not callable)

`world_probe` · `world_scene_dump` · `world_udon_inventory`

S01-c may implement read-only dumps after the owner names an authorized Worlds Unity path. Until then: disk intake (`skills/vrc-world/references/intake.md`) only.

## Evidence (S01-d schema)

`maps/evidence.py`: fingerprint (layer + sha256 + holder + lease id), `STALE_MUTATED` / `STALE_LEASE`, owned `PLAN.json` (`apply_allowed`). Layers include avatar NDMF/SDK plus `UDON_COMPILED` / `CLIENTSIM` / `MULTIPLAYER`. A Python `PASS` is not ClientSim and not in-world.

## Chat / web research

High-ambiguity decisions (assembly split, Udon evidence, STALE semantics vs other harnesses) go to a **web-research model**. Pack shape: [`templates/CHAT_RESEARCH.md`](../templates/CHAT_RESEARCH.md). Do not commit a filled pack; copy it to gitignored `notes/packs/`.

Human still clicks SDK **Build & Publish** on both domains.

# Domains (avatar vs world vs this station)

This repository stays **`vrc-dcc-workstation`**. Do not rename the public git remote or this folder to a private world product.

| Layer | What it is | Lives where |
|---|---|---|
| **Station** | Reusable agent contract, skills, named Editor tools, maps CLI | This clone (public skeleton + gitignored overlay) |
| **Avatar product** | One Unity 2022.3 avatar tree | `local.json` `unity_project`. Live `maps/<avatar>/` is gitignored |
| **World product** | One Unity Worlds / Udon tree | Owner overlay. Live `maps/worlds/<id>/` is gitignored. Not shipped here |

A private Worlds Unity tree is **a product that uses the station**. It is not this GitHub repo. Do not commit world IDs, textures, or live overlay maps.

A clone-owner **live-test avatar** (whatever sits in `local.json` `unity_project`) is overlay only. It is **not** the public skeleton’s counterpart, not a default character, and not required for foreign clones.

Per-avatar facts (meshes, Int values, freeze) live in gitignored `maps/<avatar>/`. Public playbooks are generic. [AVATAR_PROFILE.md](AVATAR_PROFILE.md).

## Route by intent

| Intent | Skill / door |
|---|---|
| Install / bootstrap **this clone** | `AGENTS.md` section 2 |
| Avatar / clothes / MA / PhysBones | `templates/JOB.md` + `skills/vrc-dcc` |
| Worlds / Udon / scene / multiplayer state | `skills/vrc-world` + [WORLD.md](WORLD.md) |
| Patch pins / skills / docs | `docs/MAINTAIN.md` then [CONTRIBUTING.md](../CONTRIBUTING.md) |

Do not send a world job down the avatar `handshake.py <avatar>` path. Do not install Avatar SDK / Modular Avatar into a Worlds project to satisfy `com.vrc-dcc.tools`. Do not install Worlds SDK into an avatar project because a playbook mentioned Udon.

## Core vs adapters (not landed as C# yet)

Proposed split: SDK-independent Core (identity, policy, lease, evidence) + Avatar adapter + World adapter. Python Core pieces are in this tree ([FRAMEWORK.md](FRAMEWORK.md)). Until C# splits, avatar named `vrc_*` stay on `VRCSDK3A` + MA. World named tools are **proposed**, not callable. Station world CLI does not POST `8080`.

See [PR_SLICES.md](PR_SLICES.md). Human still clicks SDK **Build & Publish** on both domains.

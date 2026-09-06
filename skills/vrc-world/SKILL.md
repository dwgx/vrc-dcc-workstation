---
name: vrc-world
description: >-
  VRChat Worlds / Udon / scene / multiplayer state (世界, UdonSharp,
  SceneDescriptor, ClientSim). Auto-apply only when the owner named a VRChat
  Worlds job or this clone is vrc-dcc-workstation with a Worlds ask. Do not use
  for generic Unity/game scenes, avatar clothes, or Modular Avatar. Do not
  auto-apply a user-global copy onto another repo. Named world dumps are
  proposed, not invented execute_code. Never click SDK Build & Publish.
---

# vrc-world

Draft reusable Worlds workflow. Not a live Editor package and not a rename of this repository. A private world product (if the clone owner has one) stays in gitignored overlay — see [docs/DOMAINS.md](../../docs/DOMAINS.md).

## Route

- **Inspect / intake:** read-only. Do not open an Editor, import, refresh, Play, bake, build, save, or publish merely to inspect.
- **Station maintenance:** edit this clone only (`docs/MAINTAIN.md`).
- **World changes:** exact approved Worlds Unity project + operation plan. Never install Avatar SDK / MA to satisfy avatar `vrc_*` assemblies.
- **Avatar changes:** `skills/vrc-dcc`, not this file.
- **Unknown target:** report ambiguity. Do not select the first `VRCSceneDescriptor`.

## Intake

1. Quote `session-probe` if it exists. World intent ≠ avatar `handshake.py`.
2. Confirm Unity version, `Packages/manifest.json` / VPM lock, git/backup, requested evidence layer. Record only tools this host actually exposes.
3. Identity = project path + Editor instance/epoch + loaded scene GUIDs + prefab stage + descriptor. A port is not identity.
4. Pipeline stub: [docs/WORLD.md](../../docs/WORLD.md).

If the owner named **ENV-001** / read-only takeover for a specific world folder: follow [references/intake.md](references/intake.md) and stop after the return record. A missing Editor is not a reason to start one.

## After an explicit write grant

1. Inventory source and shared consumers. Smallest write set + expected pre-state.
2. Discover the live tool schema. Names in [docs/PR_SLICES.md](../../docs/PR_SLICES.md) are proposed until `GetDynamicTools` lists them.
3. One writer lease. Preserve unrelated dirty scenes.
4. Keep UdonSharp proxy / backing / compiled program distinct from runtime. [udon-builder.md](references/udon-builder.md).
5. Shared state: ownership, caller checks, late join, owner leave, persistence, local opt-out. [network-evidence.md](references/network-evidence.md).
6. Apply, read back, record operation id. Timeout → inspect; do not assume it did not run.
7. Mark affected evidence STALE. ClientSim ≠ Desktop ≠ PCVR ≠ real multiplayer.
8. Human clicks SDK Publish.

## Progressive disclosure

[content.md](references/content.md) for textures / VRCUrl. Do not load a 200-row research catalog into every slice.

Do not invent `execute_code`. Do not POST `8080` when another product owns the Editor.

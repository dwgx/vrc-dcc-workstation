---
name: vrc-world
description: >-
  VRChat Worlds / Udon / scene / multiplayer state (世界, UdonSharp,
  SceneDescriptor, ClientSim). Use for a named VRChat Worlds job, or a
  vrc-dcc-workstation clone with a Worlds ask. Do not use for generic
  Unity/game scenes, avatar clothes, or Modular Avatar. Do not auto-apply a
  user-global copy onto another repo. Production uses discovered installed
  tools; proposed station world_* tools are optional future adapters.
---

# vrc-world

Build and verify the requested World with the project's existing toolchain.
Start with [WORLD_PRODUCTION.md](../../docs/WORLD_PRODUCTION.md), or its
[Chinese entry](../../docs/i18n/zh-CN/WORLD_PRODUCTION.md). Keep private project
facts in the project handoff or ignored overlay ([DOMAINS.md](../../docs/DOMAINS.md)).

## Route by the owner's intent

- **Production:** recover the current project, writer and accepted state; reuse
  existing authorization and continue the requested implementation and checks.
- **Inspect / intake:** honor the read-only scope. Opening Unity, importing,
  refreshing, playing or saving is not necessary just to inspect disk records.
- **Station maintenance:** improve this clone under `docs/MAINTAIN.md`.
  For project templates and local agent improvements, use
  [upstream updates](../vrc-dcc/references/upstream-updates.md) on demand.
- **Research / method improvement:** use the shared
  [research maintenance loop](../vrc-dcc/references/research-maintenance.md).
  Recover source revisions and active web requests before starting more research.
- **Avatar changes:** use `skills/vrc-dcc`. Avatar handshake and SKU/session
  limits do not apply to World production.

If the owner named **ENV-001** / read-only takeover for a specific world folder,
use [references/intake.md](references/intake.md) for that bounded return record.
For production, use native MCP or an installed provider CLI/SDK against the
project's bridge. Discover actual tools, select the observed instance and read
back its project and scenes. Support project-owned Editor C# / Blender builders
where useful. Do not guess nonexistent tool names or the target from port 8080.

## Production loop

1. Recover the requested outcome, owned write set, current state and backup.
   Read only the references needed for this slice.
2. Use one writer for a shared Editor or overlapping assets. Independent
   delegated research/model preparation can progress alongside it.
3. Produce a complete useful slice. Inspect models, materials and colliders;
   compile scripts as needed, save and reopen for readback. After a timeout,
   inspect effects before retrying. Continue across slices in the same task.
4. Keep UdonSharp proxy / backing / compiled program distinct from runtime:
   [udon-builder.md](references/udon-builder.md).
5. For shared state, check ownership, late join, owner leave, persistence and
   local opt-out: [network-evidence.md](references/network-evidence.md).
6. Record relevant results and remaining checks. ClientSim, Desktop, PCVR and
   real multiplayer prove different things. Authorized Build & Test can be
   agent-driven; the owner performs SDK Build & Publish.
7. Save a concise handoff and continue the next authorized action. Recover
   completed outputs after compaction instead of redoing them.

## Optional station records

Existing project records are sufficient. When useful, initialize
`python maps/init_world.py <id>` and read `python maps/world_handshake.py <id>`.
`world_gate.py <id> begin <review-id>` uses `VRC_DCC_JOB_HOLDER` for a writer lease,
allows successive slices and preserves mutation history. This is bookkeeping.

`implemented_world_tools: false` describes the unshipped station adapter only.
It does not block installed production tools or require waiting for S01-b/c.
See [WORLD.md](../../docs/WORLD.md) and [FRAMEWORK.md](../../docs/FRAMEWORK.md).

[web-handoff.md](../vrc-dcc/references/web-handoff.md) supports delegated research,
design references and candidate materials; reuse existing project receipt formats
when they already work. [content.md](references/content.md) covers textures and
VRCUrl. Keep project dimensions, downloaded assets and private chat IDs in overlay.

Use [material production](../vrc-dcc/references/material-production.md) for
surface/UV briefs, shader-specific channels and criterion-level review.
[DCC instance routing](../vrc-dcc/references/dcc-instance-routing.md) distinguishes
offline work, Blender background Python and the installed MCP client's capabilities.

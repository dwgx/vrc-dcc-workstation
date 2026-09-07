# Index library

Architecture (layers, new avatar, iterate loop): [README.md](README.md). Three graphs: [GRAPHS.md](GRAPHS.md). Do not mix them.

| Need | Open |
|---|---|
| What this is / how agents work | [AGENT.md](AGENT.md) |
| **New avatar map** | `python maps/init_avatar.py <id>` · [templates/AVATAR.md](templates/AVATAR.md) |
| **New world map** | `python maps/init_world.py <id>` · [templates/WORLD.md](templates/WORLD.md) · [docs/FRAMEWORK.md](../docs/FRAMEWORK.md) |
| World handshake / lease | `python maps/world_handshake.py <id>` · `python maps/world_gate.py <id> begin <review-id>` |
| Product handshake (POLICY + JOB + REVIEW next) | `python maps/handshake.py <avatar>` · `python maps/handshake.py <avatar> --json` |
| Which graph (clothes vs USB vs C#) | [GRAPHS.md](GRAPHS.md) |
| Find on a **live avatar** | `python maps/query.py <avatar> <words>` or Read `maps/<avatar>/MAP.md` |
| Find on the **USB shelf** (owned packs) | `python maps/query.py library <words>` or Read generated `library/LIBRARY.md` (gitignored) |
| C# / station Python | MCP `codegraph_explore` + `projectPath` — [GRAPHS.md](GRAPHS.md) · `powershell ./scripts/graphs-ready.ps1` |
| Refresh USB catalog | `python maps/library/scan.py` (keeps gitignored `notes.json`) |
| New zip on disk | [library/INGEST.md](library/INGEST.md) · `python maps/library/ingest.py` |
| Refresh avatar after Unity edits | `python maps/refresh.py <avatar> --from-dump dump.txt` |
| Regen MAP.md | `python maps/render_map.py <avatar>` |
| Slice gate (lint + JOB sku quota + lease) | `python maps/gate.py <avatar>` · `python maps/gate.py <avatar> begin <id>` · env `VRC_DCC_JOB_HOLDER` |
| One Editor audit | named `vrc_audit` (not `python maps/audit.py`) |
| MergeAnimator / OT / dangling / missing FX paths | `vrc_ma_wiring` / `vrc_ot_inventory` / `vrc_dangling_params` / `vrc_clip_missing_paths` |
| Prefab / pose / leftover menu | `vrc_prefab_identity` · `vrc_pose_bounds` · `vrc_leftover_menu` |
| Review board (proven vs new) | `python maps/review.py next <avatar>` · `python maps/review.py render <avatar>` |
| Plugin overlap | `maps/<avatar>/conflicts.json` · [plugin-conflicts.md](../skills/vrc-dcc/references/plugin-conflicts.md) |
| Frozen? | gitignored `notes/CURRENT.md` (clone-owner door) |
| Booth / web | `python maps/booth.py --search <name>` · AGENT.md § Booth |
| Subagents | AGENT.md § Dispatch |

Codegraph indexes **source** (C#, Python, …). It does **not** replace MAP or LIBRARY. Do **not** `codegraph init` on a Unity scene expecting clothes menus.

Live `maps/<avatar>/` folders and the USB catalog are clone-owner overlay (gitignored). This clone stores reusable memory in `skills/` plus whatever dated `notes/` the owner keeps locally.

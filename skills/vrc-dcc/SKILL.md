---
name: vrc-dcc
description: >-
  VRChat avatar DCC (改模, clothes, visemes, PhysBones, Modular Avatar,
  NDMF, FaceEmo, lilToon, FBX, VRM, CATS, Blender, Unity). Auto-apply
  when the user wants to edit a VRChat avatar or the task is clearly
  Blender/Unity for an avatar — do not wait to be named. Worlds / Udon:
  skills/vrc-world, not this file. Load slice-loop.md:
  python maps/handshake.py <avatar> then python maps/gate.py begin, then
  named vrc_audit / vrc_pose_bounds (not invented execute_code). Read
  AGENTS.md in this clone. Attach Blender/Unity MCP only for this job, never
  user-global MCP. Never click SDK Build & Publish.
---

# vrc-dcc

Canonical after clone: this repository root. Machine paths belong in gitignored `local.json` (see `local.json.example`).

## 1. Init (every VRC job)

If the window cwd is the **avatar Unity project**, or the ask is clearly a VRChat / avatar / DCC job, load [references/dcc-session.md](references/dcc-session.md), [references/slice-loop.md](references/slice-loop.md), and [references/token-budget.md](references/token-budget.md) first. Classify by intent (see `templates/JOB.md`); do not require a passphrase. Do not treat four-runtime `CONTINUE.md` as this job after `kind: dcc` or after that intent. Home/station cwd: do not write the avatar Unity project; paste for a Unity window. Door: `notes/CURRENT.md` Products table names `<avatar>`. Run `python maps/handshake.py <avatar>`. If `vrc_audit` is missing from `unityMCP` after reopen, Unity window: `scripts/install-vrc-dcc-tools.ps1` then Reload.

1. Read `AGENTS.md`, gitignored `OWNER.md` if present, and `local.json`. Empty `local.json` during **install** is the questionnaire. A DCC job with `notes/` already there: skip `INIT_QUESTIONNAIRE`.
2. Read `notes/CURRENT.md` (door). `INDEX.md` is the archive. Then `python maps/handshake.py <avatar>`. Do **not** dump MAP + LIBRARY on init. Clothes/plugins / USB packs: `query.py` on demand (`maps/AGENT.md` when the slice is find/Booth). C#: `maps/GRAPHS.md` on demand. Snapshot only if CURRENT names it.
3. Pins: `manifests/tools.json`. Stale? `scripts/refresh-pins.ps1` (prefers `gh api`). GitHub releases beat third-party VPM catalogs.
4. Pipeline: `docs/WORKFLOW.md`. Unity package URLs: `docs/UNITY.md`.
5. Attach MCP only for a live DCC job. See [lazy-mcp.md](lazy-mcp.md). Mutation needs `unityMCP` in **this** chat’s tool list.
6. End with `vrc-review`. Durable facts: `notes/` + `maps/<avatar>/STATE.md` + **`maps/<avatar>/REVIEW.json`** the same slice. Queue: `python maps/review.py next <avatar>`. “修好了” without Edit blendshape dump or Play stays observed. New work is **unreviewed** until a board row says otherwise.
7. After ~100 silent MCP turns: stop and tell the owner to **new chat**. Do not re-init that window.

## 2. Pipeline

Mesh / weights / visemes / CATS → Blender. MA / menus / PhysBone / FaceEmo / lilToon → Unity. Unadapted clothes: stop. Human clicks SDK Publish.

## 3. On-demand

- [references/slice-loop.md](references/slice-loop.md) — one slice: `handshake.py` + `gate.py` + named `vrc_*` (not invented `execute_code`)
- [../../docs/ITERATION.md](../../docs/ITERATION.md) — station base loop (fail-closed identity). Not a Unity mutate.
- [references/self-review.md](references/self-review.md) — after a station/layer slice: dispatch independent auditors; generator ≠ evaluator
- [references/dcc-session.md](references/dcc-session.md) — avatar-cwd session (no estate init, no guessed morphs)
- [references/avatar-intake.md](references/avatar-intake.md) — 改模开局：先命名 `<avatar>`，再 dump；无默认角色
- [references/token-budget.md](references/token-budget.md) — stop silent MCP loops
- [references/editor-reports.md](references/editor-reports.md) — named `vrc_*` dumps (not `execute_code`)
- [references/params-256.md](references/params-256.md) — edit vs bake bits, WantSynced OR
- [unity-ma.md](unity-ma.md)
- [references/clothing-menu.md](references/clothing-menu.md) — 穿脱 / 换色 / 轮盘 / bit budget
- [references/clothing-fit.md](references/clothing-fit.md) — 衣服骨骼/胸/BSS；MA merge ≠ 改权重
- [references/clothing-convert.md](references/clothing-convert.md) — 换素体 / 他体服 / fusion 他体服
- [references/vrc-agent-pitfalls.md](references/vrc-agent-pitfalls.md) — Unity-MCP / MA / GoGo 常见错
- [references/marshmallow-erp.md](references/marshmallow-erp.md) — 棉花糖 bake、衣服跟胸、SPS/PCS 孔不要绑 Breast_L
- [references/gogoloco.md](references/gogoloco.md) — 默认走路 paryi；Base **Append** + `vrc-dcc.loco-switch`；Action Replace；不要 disabled-Replace
- [references/plugin-conflicts.md](references/plugin-conflicts.md) — two gizmos, one lane; `maps/<avatar>/conflicts.json`; Owner names the AFK/loco winner
- [references/review-board.md](references/review-board.md) — reviewed vs new; `REVIEW.json` / `review.py`
- [references/evidence-layers.md](references/evidence-layers.md) — STATIC_SOURCE … UPLOAD_CONFIRMED; inspect ≠ publish
- [../../docs/SOURCES.md](../../docs/SOURCES.md) — no mesh dumps in git; how public research is absorbed
- [references/upload-test.md](references/upload-test.md) — 人上传后测；Editor Play 证不了 loco/棉花糖/孔
- [references/perf-vram.md](references/perf-vram.md) — SDK 显存 vs Profiler；卸无用包，不压 2K
- [references/index-library.md](references/index-library.md) — find / Booth / dispatch
- [maps/README.md](../../maps/README.md) — per-avatar memory; `init_avatar.py` for a new body
- [maps/GRAPHS.md](../../maps/GRAPHS.md) — clothes vs USB vs C# (on demand)
- [vrc-world/SKILL.md](../vrc-world/SKILL.md) — Worlds / Udon (not MA clothes)
- [udon.md](udon.md)
- [blender.md](blender.md)
- [references/physbones.md](references/physbones.md)

Prefer live Editor APIs over YAML prefab edits. Never `EditorUtility.DisplayDialog` from MCP.

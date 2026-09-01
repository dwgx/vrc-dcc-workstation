---
name: vrc-dcc
description: >-
  VRChat avatar/world DCC (改模, clothes, visemes, PhysBones, Modular Avatar,
  NDMF, FaceEmo, lilToon, Udon, FBX, VRM, CATS, Blender, Unity). Auto-apply
  when the user wants to edit a VRChat avatar, 改模, 加衣服, 表情菜单, or the task
  is clearly Blender/Unity for VRC — do not wait to be named. Read AGENTS.md
  in this clone. Attach Blender/Unity MCP only for this job, never user-global
  MCP. Never click SDK Build & Publish.
---

# vrc-dcc

Canonical after clone: this repository root. Machine paths belong in gitignored `local.json` (see `local.json.example`).

## 1. Init (every VRC job)

1. Read `AGENTS.md`, gitignored `OWNER.md` if present, and `local.json` (handshake if `local.json` is empty).
2. Read `notes/INDEX.md`.
3. Pins: `manifests/tools.json`. Stale? `scripts/refresh-pins.ps1` (prefers `gh api`). GitHub releases beat third-party VPM catalogs.
4. Pipeline: `docs/WORKFLOW.md`. Unity package URLs: `docs/UNITY.md`.
5. Attach MCP only for a live DCC job. See [lazy-mcp.md](lazy-mcp.md).
6. End with `vrc-review`. Durable facts: `notes/` / `templates/AFTER_ACTION.md`.

## 2. Pipeline

Mesh / weights / visemes / CATS → Blender. MA / menus / PhysBone / FaceEmo / lilToon → Unity. Unadapted clothes: stop. Human clicks SDK Publish.

## 3. On-demand

- [unity-ma.md](unity-ma.md)
- [udon.md](udon.md)
- [blender.md](blender.md)
- [references/physbones.md](references/physbones.md)

Prefer live Editor APIs over YAML prefab edits. Never `EditorUtility.DisplayDialog` from MCP.

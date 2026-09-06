---
name: vrc-review
description: >-
  Dual-axis review and after-action notes for VRChat DCC work. Auto-apply only
  when finishing 改模/avatar/export/MCP/pin work in a vrc-dcc-workstation
  clone (or a named VRChat job), or when the user asks for a VRC score /
  评分 / 收尾. Do not use on generic app/web PRs. Do not auto-apply a
  user-global copy onto another repo. Writes notes/ and the REVIEW board.
  Never SDK upload from the agent.
---

# vrc-review

Read `AGENTS.md` then `docs/AGENT_EVOLUTION.md`. If `OWNER.md` exists, read it (clone-owner overlay). Scores: spec + standard. Critical if SDK Publish, official Unity 6 MCP in the 2022.3 avatar project, secrets in notes, or a control-plane window wrote the avatar project tree.

Board (reviewed vs new): `skills/vrc-dcc/references/review-board.md` · `maps/<avatar>/REVIEW.json` · `python maps/review.py next <avatar>` · `python maps/review.py render <avatar>`.

A dual-axis score **without** Gesture Manager / Play (or `read_console` after NDMF) stays **observed**. Do not tell the owner the avatar is fixed on Editor writes alone. Also critical: MeshCutter on a MenuItem, inverted rest-ON strip, unmatched generic body prefab, guessed body morphs on clothing clips.

Do not set REVIEW `world` without `owner_ok`. New Unity work lands `unreviewed` (or `edit` with a dump). Failed approaches go in `lessons[]`.

Chat in the resolved locale. Durable facts: `notes/` + `templates/AFTER_ACTION.md`. Session rules: `skills/vrc-dcc/references/dcc-session.md`.

## Loop

1. Mission in one sentence.
2. Evidence (paths, MCP attached or not, Blender addon state).
3. Scores 0–10. Overall = min if critical, else 0.55 spec + 0.45 standard.
4. Findings first.
5. Durable fact → `agent-notes` (`-Station vrc-dcc`).
6. Upsert **REVIEW.json** for every row this slice touched. `python maps/review.py lint <avatar> && python maps/review.py render <avatar>`.
7. Mesh/weight still wrong → say Blender/CATS; do not pretend MA Merge Armature fixes it.

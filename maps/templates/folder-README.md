# AVATAR_ID living map

Codegraph indexes **C# / scripts**. It does not see Modular Avatar, 轮盘, or Hierarchy.

| File | Who writes it |
|---|---|
| `JOB.json` | One-chat sku quota and lease. `python maps/gate.py AVATAR_ID begin <id>`. |
| `POLICY.json` | Per-body overlay. Copied to Unity `Assets/VrcDcc/POLICY.json`. |
| `STATE.md` | Humans/agents. Snapshot. |
| `graph.json` | Regenerated. No remarks. |
| `notes.json` | Humans/agents. Key = node `id`. **Never wipe.** |
| `MAP.md` | `python ../render_map.py AVATAR_ID`. Do not hand-edit. |
| `REVIEW.json` | Proven vs new. Never `world` without Owner. |
| `REVIEW.md` | `python ../review.py render AVATAR_ID` only. |

Architecture: [`../README.md`](../README.md). Find: `python ../query.py AVATAR_ID <words>`.

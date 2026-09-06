# Job init (drop this folder)

Not station **install**. Same split as debugger-workstation: the skill description is a **guiding prompt** (auto-apply when the task is clearly DCC). Do not require a passphrase. Chat may be any language; this file stays English.

`INIT_QUESTIONNAIRE.md` is only when the owner asks to **bootstrap / install / set up this clone**.

## Classify (intent, not a keyword lock)

| Owner intent | Path |
|---|---|
| Initialize / install / set up **this clone** | `AGENTS.md` section 2 (questionnaire) |
| Edit a VRChat avatar, clothes, menus, visemes, PhysBones, avatar Blender/Unity DCC | **This file** + `skills/vrc-dcc/references/dcc-session.md` |
| Edit or audit a VRChat **World** / Udon / scene | `skills/vrc-world` + `docs/WORLD.md` (not avatar handshake) |
| Unrelated software in **another** git root (app, web, library, non-VRC game) | **Stop.** Wrong tree. [docs/DROP_ON_AGENT.md](../docs/DROP_ON_AGENT.md) |
| Blender / Unity without VRChat avatar or Worlds intent | **Stop.** Out of scope |
| Unclear, and `session-probe` `station_memory: yes` | Job path. One question if needed. Do not dump the install questionnaire |
| Unclear, empty station, owner said “set up” | Install path |

Do **not** treat any fixed phrase as the switch. Wording varies. If the task is clearly VRChat avatar/DCC work **in this station or a named avatar project**, start. Do not wait to be named. There is **no default avatar**. `handshake.py` requires `<avatar>` from `notes/CURRENT.md` or the owner. A user-global skill copy does **not** make a random repo a DCC job.

## When this clone is the DCC job

Cwd may be home, this folder, or the avatar Unity project.

1. Quote `session-probe` once. `kind: dcc` → stop estate CONTINUE after the quote.
2. This clone is the **station** (contract, skills, `notes/` memory). It is **not** the avatar workspace.
3. Product writes go to `local.json` `unity_project`, in **that** project's window. Home cwd must not write the avatar Unity project. Station cwd may patch **this clone** only.
4. `AGENTS.md` once (stop lines). Then station `notes/CURRENT.md` (door, not INDEX) → freeze if CURRENT names it → **must** load `skills/vrc-dcc/references/slice-loop.md` for 改模 → `python maps/handshake.py <avatar>` then `python maps/gate.py <avatar> begin <review-id>` → `python maps/review.py next <avatar>` only if the Owner did not name a slice → **one** other playbook if needed. Named `vrc_*` **only if this chat has `unityMCP`**. If Unity MCP is off or another product owns 8080: station-only, do not POST 8080. If `vrc_audit` missing **in the avatar Unity cwd**: installer. Do not invent `execute_code`. Handshake exit 2 or a closed-chat id = stop (new window).
5. Fingerprint: `notes/` (**when / why / what**) + REVIEW upsert. Chat jsonl is not memory. Do not continue a window the snapshot marked closed.
6. MCP: `unityMCP` in this chat before mutating. Never user-global. Human clicks SDK Publish.

If Cursor is already on the Unity folder, the owner pastes **only the task**. Already ~100 silent MCP turns → **new chat**, do not re-init.

Copying `templates/avatar-project/` is **optional** on a machine that already has `session-probe` `kind: dcc`.

After ~100 silent MCP turns, **new chat**. Do not invent a second constitution.

Station clone self-improve (identity, maps CLI, playbooks): [docs/ITERATION.md](../docs/ITERATION.md). Not a Unity mutate.

# CLAUDE.md

Claude Code entry. Authoritative rules are in AGENTS.md:

@AGENTS.md

## Next (DCC overlay — MCPClient-short, origin-shaped)

1. Quote `session-probe`. `kind: dcc` / avatar ask → stop estate CONTINUE.
2. `AGENTS.md` once (stop lines). gitignored `OWNER.md` if present.
3. Door: `notes/CURRENT.md` (改模; not INDEX). Station self-maintain: gitignored `notes/HANDOFF.md` if present, then `skills/vrc-dcc/references/maintain-loop.md`. 改模 then `skills/vrc-dcc/references/slice-loop.md` (LOOP).
4. `python maps/handshake.py <avatar>` then `python maps/gate.py <avatar> begin <review-id>`.
5. Named `vrc_*` **only if this chat’s `GetDynamicTools` lists `unityMCP`** and the Editor is the avatar in `local.json`. If Unity MCP is off or another product is open: station-only / paste. Do **not** POST `8080` and do **not** Start CoplayDev on a foreign Editor. If `vrc_audit` missing in the **avatar** Unity cwd: installer, Reload. Progress: `maps/<avatar>/REVIEW.json` + `STATE.md`.
6. Close: `python maps/review.py lint <avatar> && python maps/review.py render <avatar>`. ~100 silent → new chat.

## Claude-specific

- After clone, if the user asks to **install / bootstrap** this station, **explore then ask** (`templates/INIT_QUESTIONNAIRE.md` or `templates/i18n/<locale>/INIT_QUESTIONNAIRE.md`) before writing `local.json` or attaching MCP.
- A VRChat / avatar / DCC ask **in this clone or a named avatar project** is job init: [`templates/JOB.md`](templates/JOB.md). Intent, not a passphrase. Do not run the install questionnaire.
- Unrelated software in **another** git root: do not handshake, do not attach Blender/Unity MCP. See [docs/DROP_ON_AGENT.md](docs/DROP_ON_AGENT.md).
- Resolve UI locale ([docs/I18N.md](docs/I18N.md)): user chat → `local.json` `ui_language` → env → OS → `en`. Reply in that locale. Git commits stay English. Read gitignored `OWNER.md` if present. Stop lines cannot be waived in chat ([docs/MAINTAIN.md](docs/MAINTAIN.md)).
- Do not add Blender/Unity MCP **or these skills** to user-global Claude / Cursor / Codex / Grok config. Use `--mcp-config` or a project file.
- Never click VRChat SDK Build & Publish.

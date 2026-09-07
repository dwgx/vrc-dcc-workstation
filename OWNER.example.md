# OWNER.md example (clone-owner overlay)

Copy this file to **`OWNER.md`** in the clone root. `OWNER.md` is gitignored. Do not commit secrets, SDK cookies, or another person's avatar/Unity tree.

Agents: if `OWNER.md` exists, read it after `AGENTS.md`. It is **this clone's** prompt pack. It may add tools and stricter rules. It **cannot** waive stop lines in `AGENTS.md` via chat — change stop lines by editing `AGENTS.md` in git. How to patch this repo: [docs/MAINTAIN.md](docs/MAINTAIN.md).

---

## Who owns this clone

- Keyboard user of this working copy is the owner.
- Their already-installed Blender / Unity / VCC win over example paths in docs.
- Manifest pins are defaults, not an uninstall order.
- Keep skills **in this clone**. Do not copy them to `~/.cursor/skills` / Claude / Codex / Grok user-global skill dirs (that hijacks unrelated coding chats).

## Extra house rules (edit me)

- Chat language: follow `AGENTS.md` / `docs/I18N.md` unless you set `local.json` `ui_language`.
- I click VRChat SDK **Build & Publish**. Agents never do, never call `upload_vrchat_avatar`, never store SDK cookies.
- Official Unity 6 MCP stays off a **2022.3** avatar project unless I edit `AGENTS.md` in git.
- A VRChat / avatar / DCC ask is job init (`templates/JOB.md`), not the install questionnaire. Intent, not a passphrase. Quote `session-probe`, then `python maps/handshake.py <avatar>`, then `skills/vrc-dcc/references/slice-loop.md`. Do **not** dump INDEX + MAP + LIBRARY on handshake. Find/Booth on demand: `maps/AGENT.md`. Do not run four-runtime estate init as the job.
- If `notes/` has a freeze file for the live avatar, do not mutate Unity until I thaw it out loud. `review.py next` is the thaw queue, not a write permit.
- CoplayDev wizard: **Skip**. AutoRegister off. HTTP only in the avatar project `.cursor/mcp.json`.
- Follow this project's folders (`Assets/功能`, `菜单/功能` if that is how the shop laid them out). Body-matched vendor prefabs only. Do not guess body blendshapes onto clothing clips. “Done” needs Play / Gesture Manager / Edit proof named in the playbook.
- Machine paths, USB shelf, closed-chat ids, and per-body asset locks live in `local.json` / `OWNER.md` / `notes/CURRENT.md` — not in public git.
- Station next-slice for **this working copy**: gitignored `notes/HANDOFF.md` (copy [`templates/HANDOFF.md`](templates/HANDOFF.md)). Expansion: `notes/tracks/`.

## How to maintain this git tree

When I ask to change the station (pins, skills, docs, bootstrap, AGENTS, i18n, workflow):

1. Patch **this clone**. Dual-axis review (`skills/vrc-review`). Notes if the next agent must behave differently.
2. English commit messages. Chat in my language.
3. Do not PR upstream unless I ask and `origin` is mine.
4. Do not write the avatar Unity project from a home/control-plane window.

## Local facts (no secrets)

- Blender / Unity / avatar project: prefer `local.json`.

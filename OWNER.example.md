# OWNER.md example (clone-owner overlay)

Copy this file to **`OWNER.md`** in the clone root. `OWNER.md` is gitignored. Do not commit secrets, SDK cookies, or another person's avatar/Unity tree.

Agents: if `OWNER.md` exists, read it after `AGENTS.md`. It is **this clone's** prompt pack. It may add tools and stricter rules. It **cannot** waive stop lines in `AGENTS.md` via chat — change stop lines by editing `AGENTS.md` in git. How to patch this repo: [docs/MAINTAIN.md](docs/MAINTAIN.md).

---

## Who owns this clone

- Keyboard user of this working copy is the owner.
- Their already-installed Blender / Unity / VCC win over example paths in docs.
- Manifest pins are defaults, not an uninstall order.

## Extra house rules (edit me)

- Chat language: follow `AGENTS.md` / `docs/I18N.md` unless you set `local.json` `ui_language`.
- I click VRChat SDK **Build & Publish**. Agents never do, never call `upload_vrchat_avatar`, never store SDK cookies.
- Official Unity 6 MCP stays off a **2022.3** avatar project unless I edit `AGENTS.md` in git.

## How to maintain this git tree

When I ask to change the station (pins, skills, docs, bootstrap, AGENTS, i18n, workflow):

1. Patch **this clone**. Dual-axis review (`skills/vrc-review`). Notes if the next agent must behave differently.
2. English commit messages. Chat in my language.
3. Do not PR upstream unless I ask and `origin` is mine.
4. Do not write the avatar Unity project from a home/control-plane window.

## Local facts (no secrets)

- Blender / Unity / avatar project: prefer `local.json`.

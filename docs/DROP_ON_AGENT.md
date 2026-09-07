# Drop this repository on an agent

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/DROP_ON_AGENT.md) · [日本語](i18n/ja/DROP_ON_AGENT.md) · [한국어](i18n/ko/DROP_ON_AGENT.md)
<!-- I18N:END -->

Anyone can clone [dwgx/vrc-dcc-workstation](https://github.com/dwgx/vrc-dcc-workstation) and paste the block below. Agent contracts stay **English**. The agent **replies in the owner’s language** ([I18N.md](I18N.md)). Do not copy this author’s `C:\Users\…` paths.

This station already has a stronger 改模 loop than a generic inspect skill (handshake, `gate.py`, named `vrc_*`, fail-closed identity). Third-party skills are **cited and folded in**, not vendored ([SOURCES.md](SOURCES.md)).

## Paste this (English)

```text
Use https://github.com/dwgx/vrc-dcc-workstation (or this clone).

1. Read AGENTS.md first. Chat in my language. Git commits stay English.
2. Confirm locales.json kind is vrc-dcc-workstation. If this folder is not that clone
   and I am not doing a VRChat avatar/world job: do not run handshake.py, do not
   attach Blender/Unity MCP, do not apply vrc-dcc playbooks. Answer my actual ask.
3. If I asked to install / bootstrap / set up THIS clone: explore, then ask every
   question in templates/INIT_QUESTIONNAIRE.md. Wait for answers. Then a short plan,
   then bootstrap.ps1 dry-run, then -Apply only after I confirm. Skip missing
   Blender/Unity; docs-only is OK. Never write user-global MCP or user-global skills.
4. If I asked to edit a VRChat avatar: templates/JOB.md. No default character.
   python maps/handshake.py <avatar> after I name the id. Then
   python maps/gate.py <avatar> begin <review-id> with VRC_DCC_JOB_HOLDER.
   Named vrc_* only if unityMCP is in THIS chat. Never SDK Build & Publish.
5. If I asked about a VRChat World / Udon: skills/vrc-world, not avatar handshake.
6. Adapt to MY machine (OS, existing Blender/Unity versions). Do not uninstall my
   stack to match example paths.
```

## After clone (owner)

1. Open **this** folder in the AI client (project MCP / project skills). Do **not** copy `skills/` into `~/.cursor/skills` unless you only do VRChat — a user-global copy will hijack unrelated coding chats.
2. Say “set up this clone” for the questionnaire, or name an avatar id for 改模.
3. Human clicks VRChat SDK **Build & Publish**.

## Agent routing (do not skip)

| Situation | Do |
|---|---|
| Git root has `locales.json` kind `vrc-dcc-workstation` + install ask | Questionnaire, then bootstrap |
| Same root + avatar/clothes/menus ask | `JOB.md` → `vrc-dcc` |
| Same root + Worlds/Udon ask | `vrc-world` |
| Same root + “fix this Python/docs” (station self-maintain) | Patch **this clone** only (`MAINTAIN.md`) |
| Different git root, generic app/web/game code | **Stop DCC.** This skill does not apply |
| Avatar MCP after `gate.py begin` | Named `vrc_*` only. Set `VRC_DCC_JOB_HOLDER`. No `execute_code` / upload / `world_*` |
| Blender/Unity without VRChat avatar intent | **Stop DCC.** Film, other engines, non-VRC Unity are out of scope |
| No Blender or no Unity on disk | Continue docs/skills; leave MCP off; do not invent paths |

Inspect / diagnose is read-only until the owner authorizes a change. Evidence layers: [evidence-layers.md](../skills/vrc-dcc/references/evidence-layers.md).

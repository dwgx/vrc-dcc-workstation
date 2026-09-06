# vrc-dcc-workstation

<!-- I18N:START -->
**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)
<!-- I18N:END -->

A **skeleton repository** for a portable VRChat DCC workstation: **Blender 5.x LTS** (mesh / weights / visemes) plus **Unity 2022.3** (Modular Avatar / NDMF / PhysBones / menus), driven by AI agents over MCP. Worlds / Udon are a separate draft skill (`skills/vrc-world`); this repo is not a private world product.

Any agent (Claude Code / Codex / Cursor / Gemini / Copilot / Grok) or human can clone this repo and resolve the UI locale ([docs/I18N.md](docs/I18N.md)). **Install / bootstrap this clone:** handshake in [AGENTS.md](AGENTS.md) (or `AGENTS.zh-CN.md` / `AGENTS.ja.md` / `AGENTS.ko.md`). **Avatar / DCC job:** [`templates/JOB.md`](templates/JOB.md) — classify by intent, not a passphrase. This tree is a **reference skeleton**: keep your own Blender/Unity/prompts (`OWNER.example.md` → gitignored `OWNER.md`). Agents may **self-maintain this clone** when you ask; stop lines cannot be waived in chat ([docs/MAINTAIN.md](docs/MAINTAIN.md)). Chat in the user's language; git commits stay English.

After a job, agents score the slice (`skills/vrc-review`) and write `notes/` so the next session does not rediscover the same failure. See [docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md). Station self-improve (no default avatar, fail-closed identity): [docs/ITERATION.md](docs/ITERATION.md). What is **not** in git: [docs/SOURCES.md](docs/SOURCES.md).

**Give this URL to an agent:** [docs/DROP_ON_AGENT.md](docs/DROP_ON_AGENT.md) — English paste block; the agent reports in **your** language. Install is ask-then-act. Skills stay in **this clone** so they do not hijack unrelated coding chats.

> This repository ships **no** Blender/Unity/VRChat binaries and **no** avatar projects. See [DISCLAIMER.md](DISCLAIMER.md).

---

## What's in this repo

| Path | Contents |
| --- | --- |
| `AGENTS.md` | Authoritative agent entry — ask-then-act handshake, clone-owner overlay, MCP policy, stop lines |
| `OWNER.example.md` | Template for gitignored `OWNER.md` (this clone's prompts) |
| `docs/MAINTAIN.md` | How an agent patches **this** working copy |
| `docs/EVAL.md` | Static contract eval (`scripts/eval-agent-contract.py`) |
| `docs/BOOTSTRAP.md` | Project MCP paths + `local.json` |
| `docs/WORKFLOW.md` | Blender → Unity → human publish (2026-09 pipeline) |
| `docs/UNITY.md` | CoplayDev UPM + named `vrc_*` (`com.vrc-dcc.tools`) |
| `CLAUDE.md` / `GEMINI.md` / `.github/copilot-instructions.md` / `.cursor/rules/` | Per-client pointers to `AGENTS.md` |
| `templates/INIT_QUESTIONNAIRE.md` | Init questions (install / bootstrap only) |
| `templates/JOB.md` | Avatar / DCC job init (intent; not the install questionnaire) |
| `maps/` | Per-avatar memory CLI (`handshake.py`, `gate.py`) + templates. Live `maps/<id>/` is gitignored |
| `unity/vrc-dcc-tools` | Named `vrc_*` Editor package (`com.vrc-dcc.tools`) on CoplayDev 8080 |
| `skills/vrc-dcc/` / `skills/vrc-review/` / `skills/vrc-world/` | Avatar playbook, dual-axis review, Worlds/Udon (draft) |
| `docs/DOMAINS.md` / `docs/WORLD.md` / `docs/PR_SLICES.md` / `docs/AVATAR_PROFILE.md` / `docs/ITERATION.md` | Avatar vs world vs station; world stub; public PR slices; no default character; how the base iterates |
| `docs/SOURCES.md` | What stays out of git (meshes, vendor zips); steal vs refuse public stacks |
| `docs/DROP_ON_AGENT.md` | English paste block: clone URL → install questionnaire or 改模 job; do not hijack other repos |
| `manifests/` | Live pins (PyPI / GitHub / VPM). Re-check with `scripts/refresh-pins.ps1` |
| `mcp/*.template` | Opt-in MCP. Never user-global |
| `scripts/bootstrap.ps1` | Dry-run by default; `-Apply` writes gitignored `local.json`, `.mcp.json`, `.cursor/mcp.json` |

## Quick start

```powershell
git clone https://github.com/dwgx/vrc-dcc-workstation.git
cd vrc-dcc-workstation
# Open this folder in the AI client. Paste docs/DROP_ON_AGENT.md, or say "set up this clone".
# The agent must ask templates/INIT_QUESTIONNAIRE.md before bootstrap.ps1 -Apply.
powershell -File .\scripts\bootstrap.ps1
powershell -File .\scripts\bootstrap.ps1 -Apply
```

Then: human starts Blender **Start MCP Server** and/or Unity **MCP for Unity** inside the **avatar project** window. Agents attach those servers for that job only. Pipeline: [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Pins (2026-09-01)

| Role | Pin |
|---|---|
| Blender connect | PyPI `blender-mcp==1.9.0` (CPython **3.11** under uv if default is 3.14) |
| Unity editor bridge | CoplayDev `unity-mcp` **v10.1.2** / `mcpforunityserver==10.1.2` |
| Unity named tools | `com.vrc-dcc.tools` on CoplayDev 8080 (`vrc_audit`, …). Do not add lighfu UnityAgent |
| Fallback Blender 5.x | dcc-mcp-blender **v0.2.3** |

There is a live repo named TunaSync UnityMCP-VCC; **do not use it** (or swax/UnityMCP-VRC) as this station's default. Avatar MCP is CoplayDev + named `vrc_*`.

## Forbidden

- Agent-driven VRChat SDK **Build & Publish**
- Official Unity 6 MCP on a 2022.3 avatar project
- Blender + Unity MCP in four-runtime **user-global** config
- Copying `skills/` into user-global skill directories (unrelated repos start 改模)
- Two blender-mcp GUI clients at once

## License

MIT for the skeleton. Third-party tools keep their own licenses.

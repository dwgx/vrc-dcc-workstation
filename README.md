# vrc-dcc-workstation

<!-- I18N:START -->
**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)
<!-- I18N:END -->

A **skeleton repository** for a portable VRChat DCC workstation: **Blender 5.x LTS** (mesh / weights / visemes) plus **Unity 2022.3** (Modular Avatar / NDMF / PhysBones / menus), driven by AI agents over MCP.

Any agent (Claude Code / Codex / Cursor / Gemini / Copilot / Grok) or human can clone this repo, resolve the UI locale ([docs/I18N.md](docs/I18N.md)), run the handshake in [AGENTS.md](AGENTS.md) (or `AGENTS.zh-CN.md` / `AGENTS.ja.md` / `AGENTS.ko.md`), and reconstruct the station on their own machine. This tree is a **reference skeleton**: keep your own Blender/Unity/prompts (`OWNER.example.md` → gitignored `OWNER.md`). Agents may **self-maintain this clone** when you ask; stop lines cannot be waived in chat ([docs/MAINTAIN.md](docs/MAINTAIN.md)). Chat in the user's language; git commits stay English.

After a job, agents score the slice (`skills/vrc-review`) and write `notes/` so the next session does not rediscover the same failure. See [docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md).

> This repository ships **no** Blender/Unity/VRChat binaries and **no** avatar projects. See [DISCLAIMER.md](DISCLAIMER.md).

---

## What's in this repo

| Path | Contents |
| --- | --- |
| `AGENTS.md` | Authoritative agent entry — ask-then-act handshake, clone-owner overlay, MCP policy, stop lines |
| `OWNER.example.md` | Template for gitignored `OWNER.md` (this clone's prompts) |
| `docs/MAINTAIN.md` | How an agent patches **this** working copy |
| `docs/WORKFLOW.md` | Blender → Unity → human publish (2026-09 pipeline) |
| `docs/UNITY.md` | CoplayDev UPM + UnityAgent VPM pins |
| `CLAUDE.md` / `GEMINI.md` / `.github/copilot-instructions.md` / `.cursor/rules/` | Per-client pointers to `AGENTS.md` |
| `templates/INIT_QUESTIONNAIRE.md` | Init questions |
| `skills/vrc-dcc/` / `skills/vrc-review/` | Auto-discovered playbook + dual-axis review |
| `manifests/` | Live pins (PyPI / GitHub / VPM). Re-check with `scripts/refresh-pins.ps1` |
| `mcp/*.template` | Opt-in MCP. Never user-global |
| `scripts/bootstrap.ps1` | Dry-run by default; `-Apply` writes gitignored `local.json` / `mcp/local.mcp.json` |

## Quick start

```powershell
git clone https://github.com/dwgx/vrc-dcc-workstation.git
cd vrc-dcc-workstation
# handshake: read AGENTS.md, fill questionnaire
powershell -File .\scripts\bootstrap.ps1
powershell -File .\scripts\bootstrap.ps1 -Apply
```

Then: human starts Blender **Start MCP Server** and/or Unity **MCP for Unity** inside the **avatar project** window. Agents attach those servers for that job only. Pipeline: [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Pins (2026-09-01)

| Role | Pin |
|---|---|
| Blender connect | PyPI `blender-mcp==1.9.0` (CPython **3.11** under uv if default is 3.14) |
| Unity editor bridge | CoplayDev `unity-mcp` **v10.1.2** / `mcpforunityserver==10.1.2` |
| Unity MA/NDMF agent | lighfu UnityAgent **editor-v0.15.0** (VPM). GitHub releases beat stale VPM catalogs |
| Fallback Blender 5.x | dcc-mcp-blender **v0.2.3** |

There is **no** live repo named UnityMCP-VCC.

## Forbidden

- Agent-driven VRChat SDK **Build & Publish**
- Official Unity 6 MCP on a 2022.3 avatar project
- Blender + Unity MCP in four-runtime **user-global** config
- Two blender-mcp GUI clients at once

## License

MIT for the skeleton. Third-party tools keep their own licenses.

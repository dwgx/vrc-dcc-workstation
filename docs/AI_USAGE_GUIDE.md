# AI usage guide

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/AI_USAGE_GUIDE.md) · [日本語](i18n/ja/AI_USAGE_GUIDE.md) · [한국어](i18n/ko/AI_USAGE_GUIDE.md)
<!-- I18N:END -->

After clone:

- **Install / bootstrap this clone:** `AGENTS.md` section 2 (questionnaire), then `docs/WORKFLOW.md` / `docs/UNITY.md`, write `local.json`.
- **Avatar / DCC job:** [`templates/JOB.md`](../templates/JOB.md) — classify by intent, not a passphrase. Skip the questionnaire if `notes/` already exists.
- **Worlds / Udon job:** [`skills/vrc-world/SKILL.md`](../skills/vrc-world/SKILL.md) + [`docs/WORLD.md`](WORLD.md). Do not run avatar `handshake.py`.

Then:

1. Read `AGENTS.md` (MCP policy + stop lines).
2. Read `notes/CURRENT.md` (door) and gitignored `OWNER.md` if present. Not INDEX on handshake.
3. Attach MCP only for a live DCC job (`mcp/cursor.mcp.json.template` → gitignored `.cursor/mcp.json` / `.mcp.json` / `mcp/local.mcp.json`).
4. End with `skills/vrc-review`.

## Default pins (re-check with `scripts/refresh-pins.ps1`)

See `manifests/tools.json`. GitHub **releases** beat third-party VPM catalogs. Prefer `gh api` if unauthenticated GitHub REST is rate-limited.

## Unity packages (in the avatar project window, not a home/control-plane window)

- CoplayDev: `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>` plus named `vrc_*` (`com.vrc-dcc.tools`)
- Do not install lighfu UnityAgent / `execute_csharp` on this 2022.3 avatar pipeline

Do not use TunaSync UnityMCP-VCC or swax/UnityMCP-VRC as this station's default. Catalog pins are discovery, not install.

## Blender

Human: 3D View `N` → BlenderMCP → **Start MCP Server**. Client: `uvx --python 3.11 blender-mcp==<pin>` with `UV_PYTHON_PREFERENCE=only-managed` if the default Python is 3.14+.

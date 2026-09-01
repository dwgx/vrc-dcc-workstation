# AI usage guide

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/AI_USAGE_GUIDE.md) · [日本語](i18n/ja/AI_USAGE_GUIDE.md) · [한국어](i18n/ko/AI_USAGE_GUIDE.md)
<!-- I18N:END -->

After clone + bootstrap, agents should:

1. Read `AGENTS.md` (handshake + MCP policy).
2. Read `docs/WORKFLOW.md` and `docs/UNITY.md`.
3. Read `local.json` if it exists; otherwise ask and write it.
4. Read `notes/INDEX.md`.
5. Attach MCP only for a live DCC job (`mcp/cursor.mcp.json.template` → gitignored `.cursor/mcp.json` / `.mcp.json` / `mcp/local.mcp.json`).
6. End with `skills/vrc-review`.

## Default pins (re-check with `scripts/refresh-pins.ps1`)

See `manifests/tools.json`. GitHub **releases** beat third-party VPM catalogs. Prefer `gh api` if unauthenticated GitHub REST is rate-limited.

## Unity packages (in the avatar project window, not a home/control-plane window)

- CoplayDev: `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>`
- UnityAgent: VPM `https://lighfu.github.io/vpm/` tag `editor-v*` in the manifest

There is no live repo named UnityMCP-VCC.

## Blender

Human: 3D View `N` → BlenderMCP → **Start MCP Server**. Client: `uvx --python 3.11 blender-mcp==<pin>` with `UV_PYTHON_PREFERENCE=only-managed` if the default Python is 3.14+.

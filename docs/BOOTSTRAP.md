# Bootstrap layout

<!-- I18N:START -->
**English** · this file stays English (like `docs/EVAL.md`)
<!-- I18N:END -->

How `-Apply` turns this skeleton into a station. Dry-run is the default. Does not write user-global MCP. Does not write the avatar Unity tree.

## Project MCP (three copies, one payload)

`-Apply` renders `mcp/cursor.mcp.json.template` and writes:

| File | Why |
|---|---|
| `.cursor/mcp.json` | Cursor project MCP |
| `.mcp.json` | Claude Code project MCP |
| `mcp/local.mcp.json` | `claude --mcp-config` / docs |

Same JSON. Gitignored (paths / uvx). Attach still requires a live Blender MCP server / Unity MCP window.

## `local.json`

Always gitignored. `-Apply` writes `install_root` plus discovered Unity/Blender/uvx when the file is new. `ui_language` is written only with `-UiLanguage` or `WORKSTATION_UI_LANG` / `VRC_DCC_UI_LANG`, so an English Windows UI cannot lock out a Chinese chat.

## InstallRoot ≠ clone

If `-InstallRoot` is not this repo, bootstrap copies `manifests/`, `skills/`, `docs/`, `scripts/`, and root contract files into that root first.

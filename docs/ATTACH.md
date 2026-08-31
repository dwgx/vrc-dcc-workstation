# Attach MCP (human + agent)

Templates live in `mcp/*.template`. Generated `mcp/local.mcp.json` is gitignored (absolute paths). Full pipeline: [WORKFLOW.md](WORKFLOW.md). Unity URLs: [UNITY.md](UNITY.md).

## Blender

1. Fill `blender_exe` in `local.json`.
2. Enable the blender-mcp add-on; start **Start MCP Server** in the N-panel.
3. Client: `uvx --python 3.11 blender-mcp==<pin from manifests/tools.json>`.
4. Attach via project MCP or `claude --mcp-config mcp/local.mcp.json`.

One blender-mcp client at a time.

## Unity 2022.3

Open the **avatar Unity project** (not a home/control-plane window).

1. Package Manager → Git URL for CoplayDev (`manifests/tools.json` `upm` field).
2. Window → MCP for Unity → Start (HTTP `http://localhost:8080/mcp`).
3. Optional: VPM UnityAgent from `https://lighfu.github.io/vpm/`.
4. Copy servers into that project's `.cursor/mcp.json`.

Do not install official Unity MCP / Unity 6 AI Assistant into this 2022.3 project.

## This machine only

If `LOCAL-THIS-PC.md` exists, it has owner-specific paths. Do not commit it. Optional env for bootstrap probe: `VRC_DCC_UNITY_HUB`, `VRC_DCC_BLENDER`, `VRC_DCC_UVX`.

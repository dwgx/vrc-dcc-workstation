# Lazy MCP (VRC DCC)

**Skills stay loaded. MCP processes do not.**

Do not add Blender, Unity, or debugger backends to Claude / Codex / Cursor / Grok **user-global** MCP.

## When the job needs a live DCC

| Need | How to attach (this job only) |
|---|---|
| Blender scene | Human started Blender MCP. Client uses this clone's `mcp/local.mcp.json` (gitignored) as project/session config. |
| Unity Hierarchy | CoplayDev HTTP `http://localhost:8080/mcp` after UPM in the **open** avatar editor. |
| Unity MA/PhysBone agent | named `vrc_*` on CoplayDev 8080 after `com.vrc-dcc.tools`. Not lighfu. |

Claude Code one-shot (does not persist to user config):

```text
claude --mcp-config "/path/to/vrc-dcc-workstation/mcp/local.mcp.json"
```

Cursor: open this clone (or the avatar Unity project) as the workspace. Do not paste servers into the user-global MCP list.

If MCP is not attached: read files, write notes, tell the human which window to open. Do not silently `claude mcp add -s user`.

**Mutation gate:** do not edit Hierarchy / menus / parameters until `GetDynamicTools` shows `unityMCP` **in this chat**. Prefer named `vrc_audit` / `vrc_pose_bounds` / … over `execute_code`. If those names are missing: Unity window `scripts/install-vrc-dcc-tools.ps1`, compile, Reload. YAML grep is analysis. After CoplayDev Start, the human may still need Cursor Reload Window.

CoplayDev setup wizard step “Configure MCP Clients”: **Skip**. Never Configure Selected / Configure All. HTTP belongs in the **avatar project** `.cursor/mcp.json` only. A red missing-config dot against user-global Cursor config is expected.

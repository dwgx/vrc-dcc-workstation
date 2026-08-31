# Lazy MCP (VRC DCC)

**Skills stay loaded. MCP processes do not.**

Do not add Blender, Unity, or debugger backends to Claude / Codex / Cursor / Grok **user-global** MCP.

## When the job needs a live DCC

| Need | How to attach (this job only) |
|---|---|
| Blender scene | Human started Blender MCP. Client uses this clone's `mcp/local.mcp.json` (gitignored) as project/session config. |
| Unity Hierarchy | CoplayDev HTTP `http://localhost:8080/mcp` after UPM in the **open** avatar editor. |
| Unity MA/PhysBone agent | lighfu UnityAgent via VPM inside that project. Optional. |

Claude Code one-shot (does not persist to user config):

```text
claude --mcp-config "/path/to/vrc-dcc-workstation/mcp/local.mcp.json"
```

Cursor: open this clone (or the avatar Unity project) as the workspace. Do not paste servers into the user-global MCP list.

If MCP is not attached: read files, write notes, tell the human which window to open. Do not silently `claude mcp add -s user`.

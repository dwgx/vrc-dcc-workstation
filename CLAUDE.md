# CLAUDE.md

Claude Code entry. Authoritative rules are in AGENTS.md:

@AGENTS.md

## Claude-specific

- After clone, if the user asks to initialize this station, **explore then ask** (`templates/INIT_QUESTIONNAIRE.md`) before writing `local.json` or attaching MCP.
- Default chat language follows the user. Tracked files stay English.
- Do not add Blender/Unity MCP to user-global Claude MCP. Use `--mcp-config` or a project file.
- Never click VRChat SDK Build & Publish.

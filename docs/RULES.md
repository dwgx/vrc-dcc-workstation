# Rules

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/RULES.md) · [日本語](i18n/ja/RULES.md) · [한국어](i18n/ko/RULES.md)
<!-- I18N:END -->

- Human review: PhysBone limits, performance rank, SDK **Build & Publish**.
- Never let an agent click VRChat upload or call `upload_vrchat_avatar`.
- Official Unity MCP / Unity 6 AI Assistant stays off a 2022.3 avatar project.
- One blender-mcp instance: Cursor **or** Claude Desktop, not both.
- Do not wire these servers into user-global MCP.
- Package adds happen in the avatar Unity project window, not a home/control-plane window.
- `UnityMCP-VCC` is not a real repo. Use lighfu UnityAgent + CoplayDev unity-mcp pins in `manifests/tools.json`. Pin from GitHub releases, not from a third-party VPM catalog.

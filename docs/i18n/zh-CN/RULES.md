# 规则

<!-- I18N:START -->
[English](../../RULES.md) · **简体中文** · [日本語](../ja/RULES.md) · [한국어](../ko/RULES.md)
<!-- I18N:END -->

- 人审：PhysBone 上限、性能等级、SDK **Build & Publish**。
- 绝不让 agent 点 VRChat 上传或调用 `upload_vrchat_avatar`。
- 官方 Unity MCP / Unity 6 AI Assistant 不进 2022.3 角色工程。
- blender-mcp 实例只有一个：Cursor **或** Claude Desktop，不要两个。
- 不要把这些 server 写进用户全局 MCP。
- 加包在角色 Unity 工程窗口里做，不要在 home / 控制面窗口。
- 默认 Editor 桥：CoplayDev unity-mcp + 命名 `vrc_*`（`com.vrc-dcc.tools`）。这条 2022.3 改模管线不要加 lighfu UnityAgent、TunaSync UnityMCP-VCC 或 swax/UnityMCP-VRC 作为第二套活桥。钉 GitHub releases，不要钉滞后的第三方 VPM 目录。

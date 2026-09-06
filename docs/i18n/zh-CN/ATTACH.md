# 挂接 MCP（人 + agent）

<!-- I18N:START -->
[English](../../ATTACH.md) · **简体中文** · [日本語](../ja/ATTACH.md) · [한국어](../ko/ATTACH.md)
<!-- I18N:END -->

模板在 `mcp/*.template`。生成的 `mcp/local.mcp.json` 被 gitignore（含绝对路径）。完整管线：[WORKFLOW.md](WORKFLOW.md)。Unity URL：[UNITY.md](UNITY.md)。

## Blender

1. 在 `local.json` 填 `blender_exe`。
2. 启用 blender-mcp 插件；在 N 面板点 **Start MCP Server**。
3. 客户端：`uvx --python 3.11 blender-mcp==<pin from manifests/tools.json>`。
4. 用工程 MCP 或 `claude --mcp-config mcp/local.mcp.json` 挂接。

同一时间只有一个 blender-mcp 客户端。

## Unity 2022.3

打开**角色 Unity 工程**（不是 home / 控制面窗口）。

1. Package Manager → CoplayDev 的 Git URL（`manifests/tools.json` 的 `upm`）。
2. Window → MCP for Unity → Start（HTTP `http://localhost:8080/mcp`）。
3. 命名 `vrc_*`：在 Unity 工程 cwd 跑 `scripts/install-vrc-dcc-tools.ps1`。不要装 VPM UnityAgent。
4. 把 servers 写进该工程的 `.cursor/mcp.json`。

不要把官方 Unity MCP / Unity 6 AI Assistant 装进这个 2022.3 工程。

## 仅本机

若存在 `LOCAL-THIS-PC.md`，里面是主人专用路径。不要提交。bootstrap 探测可用环境变量：`VRC_DCC_UNITY_HUB`、`VRC_DCC_BLENDER`、`VRC_DCC_UVX`。

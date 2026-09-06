# Unity 包（角色工程窗口）

<!-- I18N:START -->
[English](../../UNITY.md) · **简体中文** · [日本語](../ja/UNITY.md) · [한국어](../ko/UNITY.md)
<!-- I18N:END -->

这些包加在**角色 Unity 工程里面**，不要从 home / 控制面窗口加。钉选：`manifests/tools.json`。

## CoplayDev — MCP for Unity（默认编辑器桥）

Package Manager 的 Git URL：

```
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.1.2
```

然后：Window → MCP for Unity → Start。Cursor HTTP：`http://localhost:8080/mcp`。向导 **Configure MCP Clients** 点 **Skip**（不要 Configure Selected / Configure All）。关掉 AutoRegister，免得下次开编辑器再写用户全局 MCP。HTTP 只放在角色工程 `.cursor/mcp.json`。用户全局缺配置的红点是预期现象。

PyPI 配套（stdio / 服务端）：`mcpforunityserver==10.1.2`。

可在 Unity 2021.3–6.x 上工作；本站角色仍钉 **2022.3 LTS**。

## lighfu UnityAgent（这条 2022.3 改模管线**不要装**）

改模路径是 CoplayDev HTTP + 命名 `vrc_*`（`com.vrc-dcc.tools`）。不要加 UnityAgent / `execute_csharp` / 第二套 MCP。`manifests/tools.json` 里的 VPM 钉只是目录事实。

## 这个 2022.3 角色工程禁止

- 官方 Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant`（Unity 6）
- TunaSync UnityMCP-VCC 或 swax/UnityMCP-VRC 作为**第二套活** Editor 桥
- Agent 去点 SDK Build & Publish

## Worlds / Udon（可选）

不是合衣服的首选。见 `skills/vrc-world`、[WORLD.md](../../WORLD.md)、`manifests/tools.json` 的 `swax-unitymcp-vrc`（仅目录）。不要再加第二套活 Unity MCP。

## 衣服菜单（MA）

套装 Int + 穿脱 Bool + 颜色轮盘。省 bit、国内店布局、MaterialSwap / Setter：[改模衣服菜单](CLOTHING_MENU.md) · [English](../../CLOTHING_MENU.md)。技能指针：`skills/vrc-dcc/references/clothing-menu.md`。

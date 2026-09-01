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

然后：Window → MCP for Unity → Start。Cursor HTTP：`http://localhost:8080/mcp`。

PyPI 配套（stdio / 服务端）：`mcpforunityserver==10.1.2`。

可在 Unity 2021.3–6.x 上工作；本站角色仍钉 **2022.3 LTS**。

## lighfu UnityAgent（MA / NDMF agent）

VPM 源：`https://lighfu.github.io/vpm/`

安装与 GitHub **release** 标签一致的 `editor-v*` 包（2026-09-01 核验例：`editor-v0.15.0`）。第三方 VPM 目录可能滞后。

## 这个 2022.3 角色工程禁止

- 官方 Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant`（Unity 6）
- 虚构的名字 “UnityMCP-VCC”
- Agent 去点 SDK Build & Publish

## Worlds / Udon（可选）

不是合衣服的首选。见 `skills/vrc-dcc/udon.md` 与 `manifests/tools.json` 的 `swax-unitymcp-vrc`。

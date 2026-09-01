# AI 使用指南

<!-- I18N:START -->
[English](../../AI_USAGE_GUIDE.md) · **简体中文** · [日本語](../ja/AI_USAGE_GUIDE.md) · [한국어](../ko/AI_USAGE_GUIDE.md)
<!-- I18N:END -->

clone + bootstrap 之后，agent 应当：

1. 读 [AGENTS.zh-CN.md](../../../AGENTS.zh-CN.md)（握手 + MCP 策略）。
2. 读 [WORKFLOW.md](WORKFLOW.md) 与 [UNITY.md](UNITY.md)。
3. 若有 `local.json` 则读；否则询问并写入。
4. 读 `notes/INDEX.md`。
5. 只为现场 DCC 任务挂 MCP（`mcp/cursor.mcp.json.template` → gitignore 的 `mcp/local.mcp.json`）。
6. 以 `skills/vrc-review` 收尾。

## 默认钉选（用 `scripts/refresh-pins.ps1` 复核）

见 `manifests/tools.json`。GitHub **releases** 优于第三方 VPM 目录。未登录 GitHub REST 被限速时优先 `gh api`。

## Unity 包（在角色工程窗口，不是 home / 控制面）

- CoplayDev：`https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>`
- UnityAgent：VPM `https://lighfu.github.io/vpm/`，清单里的 `editor-v*` 标签

没有名为 UnityMCP-VCC 的活仓库。

## Blender

人：3D 视图 `N` → BlenderMCP → **Start MCP Server**。客户端：`uvx --python 3.11 blender-mcp==<pin>`；默认 Python 是 3.14+ 时设 `UV_PYTHON_PREFERENCE=only-managed`。

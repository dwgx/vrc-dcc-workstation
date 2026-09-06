# AI 使用指南

<!-- I18N:START -->
[English](../../AI_USAGE_GUIDE.md) · **简体中文** · [日本語](../ja/AI_USAGE_GUIDE.md) · [한국어](../ko/AI_USAGE_GUIDE.md)
<!-- I18N:END -->

clone 之后：

- **装站 / 初始化本 clone：** [AGENTS.zh-CN.md](../../../AGENTS.zh-CN.md) 第 2 节问卷，再读 [WORKFLOW.md](WORKFLOW.md) / [UNITY.md](UNITY.md)，写 `local.json`。
- **改模 / DCC 干活：** [`templates/JOB.md`](../../../templates/JOB.md) — 按意图分类，不要口令。已有 `notes/` 就跳过问卷。
- **世界 / Udon：** [`skills/vrc-world/SKILL.md`](../../../skills/vrc-world/SKILL.md) + [`docs/WORLD.md`](../../WORLD.md)。不要跑角色 `handshake.py`。

然后：

1. 读 [AGENTS.zh-CN.md](../../../AGENTS.zh-CN.md)（MCP 策略 + 红线）。
2. 读 `notes/CURRENT.md`（门）。有 gitignore 的 `OWNER.md` 就读。handshake 不要堆 INDEX。
3. 只为现场 DCC 任务挂 MCP（`mcp/cursor.mcp.json.template` → gitignore 的 `.cursor/mcp.json` / `.mcp.json` / `mcp/local.mcp.json`）。
4. 以 `skills/vrc-review` 收尾。

## 默认钉选（用 `scripts/refresh-pins.ps1` 复核）

见 `manifests/tools.json`。GitHub **releases** 优于第三方 VPM 目录。未登录 GitHub REST 被限速时优先 `gh api`。

## Unity 包（在角色工程窗口，不是 home / 控制面）

- CoplayDev：`https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>`，加上命名 `vrc_*`（`com.vrc-dcc.tools`）
- 这条 2022.3 改模管线不要装 lighfu UnityAgent / `execute_csharp`

不要把 TunaSync UnityMCP-VCC 或 swax/UnityMCP-VRC 当成本站默认桥。清单 pin 是发现项，不是安装令。

## Blender

人：3D 视图 `N` → BlenderMCP → **Start MCP Server**。客户端：`uvx --python 3.11 blender-mcp==<pin>`；默认 Python 是 3.14+ 时设 `UV_PYTHON_PREFERENCE=only-managed`。

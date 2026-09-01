# vrc-dcc-workstation

<!-- I18N:START -->
[English](README.md) · **简体中文** · [日本語](README.ja.md) · [한국어](README.ko.md)
<!-- I18N:END -->

便携 **VRChat DCC** 工作站的**骨架仓库**：**Blender 5.x LTS**（网格 / 权重 / 口型）+ **Unity 2022.3**（Modular Avatar / NDMF / PhysBone / 菜单），由 AI agent 经 MCP 驱动。

任意 agent（Claude Code / Codex / Cursor / Gemini / Copilot / Grok）或人 clone 后，按 [docs/i18n/zh-CN/I18N.md](docs/i18n/zh-CN/I18N.md) 选定界面语言，走 [AGENTS.zh-CN.md](AGENTS.zh-CN.md) 握手，即可在自己的机器上还原工位。本树是**参考骨架**：保留自己的 Blender / Unity / 提示词（`OWNER.example.md` → gitignore 的 `OWNER.md`）。主人要求时 agent 可以**改这个 clone**；聊天不能取消红线（[docs/i18n/zh-CN/MAINTAIN.md](docs/i18n/zh-CN/MAINTAIN.md)）。**对话用中文**；git 提交说明保持英文。本仓库不含角色工程。

任务结束后用 `skills/vrc-review` 打分并写入 `notes/`。[docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md)。

> **不分发 Blender / Unity / VRChat 二进制，也不含角色工程。** 见 [DISCLAIMER.zh-CN.md](DISCLAIMER.zh-CN.md)。

---

## 这个仓库里有什么

| 路径 | 内容 |
| --- | --- |
| `AGENTS.zh-CN.md` | 中文 agent 合同：先问后做、克隆主人覆盖层、MCP、红线 |
| `OWNER.example.md` | gitignore 的 `OWNER.md` 模板（本 clone 提示词） |
| `docs/i18n/zh-CN/MAINTAIN.md` | 如何改**这个**工作副本 |
| `docs/i18n/zh-CN/WORKFLOW.md` | Blender → Unity → 人点 Publish（2026-09） |
| `docs/i18n/zh-CN/UNITY.md` | CoplayDev UPM + UnityAgent VPM |
| `docs/i18n/zh-CN/I18N.md` | 语言与初始化 |
| `CLAUDE.md` / `GEMINI.md` / `.cursor/rules/` | 各客户端入口，指向 `AGENTS.md` 并按语言读译文 |
| `templates/i18n/zh-CN/INIT_QUESTIONNAIRE.md` | 中文初始化问卷 |
| `skills/vrc-dcc/` / `skills/vrc-review/` | 改模手册 + 双轴审查（技能正文为英文，对话仍用中文） |
| `manifests/` | 钉选（PyPI / GitHub / VPM）。用 `scripts/refresh-pins.ps1` 复核 |
| `mcp/*.template` | 按需 MCP。绝不写进用户全局 |
| `scripts/bootstrap.ps1` | 默认 dry-run；`-Apply` 写入 gitignore 的 `local.json` / `mcp/local.mcp.json` |

英文对照表见 [README.md](README.md)。

## 快速开始

```powershell
git clone https://github.com/dwgx/vrc-dcc-workstation.git
cd vrc-dcc-workstation
powershell -File .\scripts\bootstrap.ps1
powershell -File .\scripts\bootstrap.ps1 -Apply
```

然后：人在 Blender 点 **Start MCP Server**，和/或在**角色 Unity 工程窗口**里启动 **MCP for Unity**。Agent 只为当前任务连接。流程：[docs/i18n/zh-CN/WORKFLOW.md](docs/i18n/zh-CN/WORKFLOW.md)。

## 钉选（2026-09-01）

| 角色 | 钉选 |
|---|---|
| Blender 连接 | PyPI `blender-mcp==1.9.0`（若默认是 3.14，用 uv 的 CPython **3.11**） |
| Unity 编辑器桥 | CoplayDev `unity-mcp` **v10.1.2** / `mcpforunityserver==10.1.2` |
| Unity MA/NDMF agent | lighfu UnityAgent **editor-v0.15.0**（VPM）。以 GitHub Release 为准，第三方目录可能滞后 |
| Blender 5.x 后备 | dcc-mcp-blender **v0.2.3** |

没有名为 UnityMCP-VCC 的活仓库。

## 禁止

- Agent 去点 VRChat SDK **Build & Publish**
- 往 2022.3 角色工程装官方 Unity 6 MCP
- 把 Blender + Unity MCP 写进四套运行时的**用户全局**配置
- 两个 blender-mcp GUI 客户端同时开

本机绝对路径只写在 gitignore 的 `LOCAL-THIS-PC.md` / `local.json`，不要推进 GitHub。

## 许可

骨架 MIT。第三方工具各跟各的许可。

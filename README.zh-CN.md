# vrc-dcc-workstation

<!-- I18N:START -->
[English](README.md) · **简体中文** · [日本語](README.ja.md) · [한국어](README.ko.md)
<!-- I18N:END -->

便携 **VRChat DCC** 工作站的**骨架仓库**：**Blender 5.x LTS**（网格 / 权重 / 口型）+ **Unity 2022.3**（Modular Avatar / NDMF / PhysBone / 菜单），由 AI agent 经 MCP 驱动。世界 / Udon 是另一条草案技能（`skills/vrc-world`）；本仓库不是某个私有世界产品。

任意 agent（Claude Code / Codex / Cursor / Gemini / Copilot / Grok）或人 clone 后，按 [docs/i18n/zh-CN/I18N.md](docs/i18n/zh-CN/I18N.md) 选定界面语言。**装站 / 初始化本 clone** 才走 [AGENTS.zh-CN.md](AGENTS.zh-CN.md) 问卷。改模干活走 `templates/JOB.md`（按意图分类，不要口令）。本树是**参考骨架**：保留自己的 Blender / Unity / 提示词（`OWNER.example.md` → gitignore 的 `OWNER.md`）。主人要求时 agent 可以**改这个 clone**；聊天不能取消红线（[docs/i18n/zh-CN/MAINTAIN.md](docs/i18n/zh-CN/MAINTAIN.md)）。**对话用中文**；git 提交说明保持英文。本仓库不含角色工程。

任务结束后用 `skills/vrc-review` 打分并写入 `notes/`。[docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md)。

> **不分发 Blender / Unity / VRChat 二进制，也不含角色工程。** 见 [DISCLAIMER.zh-CN.md](DISCLAIMER.zh-CN.md)。

---

## 这个仓库里有什么

| 路径 | 内容 |
| --- | --- |
| `AGENTS.zh-CN.md` | 中文 agent 合同：先问后做、克隆主人覆盖层、MCP、红线 |
| `OWNER.example.md` | gitignore 的 `OWNER.md` 模板（本 clone 提示词） |
| `docs/i18n/zh-CN/MAINTAIN.md` | 如何改**这个**工作副本 |
| `docs/EVAL.md` | 静态合同测评（英文） |
| `docs/i18n/zh-CN/WORKFLOW.md` | Blender → Unity → 人点 Publish（2026-09） |
| `docs/i18n/zh-CN/UNITY.md` | CoplayDev UPM + 命名 `vrc_*` |
| `docs/i18n/zh-CN/I18N.md` | 语言与初始化 |
| `CLAUDE.md` / `GEMINI.md` / `.cursor/rules/` | 各客户端入口，指向 `AGENTS.md` 并按语言读译文 |
| `templates/i18n/zh-CN/INIT_QUESTIONNAIRE.md` | 中文初始化问卷（装站） |
| `templates/i18n/zh-CN/JOB.md` | 干活初始化（按意图；不是装站问卷） |
| `maps/` | 每角色记忆 CLI（`handshake.py` / `gate.py`）+ 模板。活的 `maps/<id>/` 被 gitignore |
| `unity/vrc-dcc-tools` | 命名 `vrc_*`（`com.vrc-dcc.tools`） |
| `skills/vrc-dcc/` / `skills/vrc-review/` / `skills/vrc-world/` | 改模手册、双轴审查、世界/Udon（草案；技能正文英文） |
| `docs/DOMAINS.md` / `docs/WORLD.md` / `docs/PR_SLICES.md` | 角色 vs 世界 vs 工位；世界管线草稿；公开 PR 切片 |
| `docs/AVATAR_PROFILE.md` | 无默认角色；活体事实在 `maps/<avatar>/` |
| `manifests/` | 钉选（PyPI / GitHub / VPM）。用 `scripts/refresh-pins.ps1` 复核 |
| `mcp/*.template` | 按需 MCP。绝不写进用户全局 |
| `scripts/bootstrap.ps1` | 默认 dry-run；`-Apply` 写入 gitignore 的 `local.json`、`.mcp.json`、`.cursor/mcp.json` |

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
| Unity 命名工具 | CoplayDev 8080 上的 `com.vrc-dcc.tools`（`vrc_audit` 等）。不要加 lighfu UnityAgent |
| Blender 5.x 后备 | dcc-mcp-blender **v0.2.3** |

存在名为 TunaSync UnityMCP-VCC 的仓库；**不要拿它**（或 swax/UnityMCP-VRC）当本站默认桥。头像 MCP 用 CoplayDev + 命名 `vrc_*`。

## 禁止

- Agent 去点 VRChat SDK **Build & Publish**
- 往 2022.3 角色工程装官方 Unity 6 MCP
- 把 Blender + Unity MCP 写进四套运行时的**用户全局**配置
- 两个 blender-mcp GUI 客户端同时开

本机绝对路径只写在 gitignore 的 `LOCAL-THIS-PC.md` / `local.json`，不要推进 GitHub。

## 许可

骨架 MIT。第三方工具各跟各的许可。

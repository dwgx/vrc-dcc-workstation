# AGENTS.md — vrc-dcc-workstation

所有 AI agent（Claude Code、Codex、Cursor、Gemini CLI、Copilot、Grok）的权威入口。初始化或驱动本站前先读本文。

本仓库是**骨架**。不分发 Blender / Unity / VRChat 二进制，也不含角色工程。

<!-- I18N:START -->
[English](AGENTS.md) · **简体中文** · [日本語](AGENTS.ja.md) · [한국어](AGENTS.ko.md)
<!-- I18N:END -->

语言规则见 [docs/i18n/zh-CN/I18N.md](docs/i18n/zh-CN/I18N.md)。请用**用户正在使用的语言**对话；git 提交说明保持英文。

---

## 0. 这是什么

便携 **VRChat DCC** 工作站：Blender（网格 / 权重 / 口型）+ Unity 2022.3（Modular Avatar / NDMF / PhysBone / 菜单）。Agent **只为当前任务**挂 Blender MCP 和/或 Unity MCP。不要写进 Claude / Codex / Cursor / Grok **用户全局** MCP。

VRChat SDK **Build & Publish 必须由人点**。Agent 不得点。

---

## 1. 初始化握手（先问后做）

当用户要求初始化 / 安装 / 搭建本站时：

### 第 1 步 — 探索（只读）

读 `README.zh-CN.md`、本文、`docs/i18n/zh-CN/WORKFLOW.md`、`manifests/tools.json`、`manifests/mcp.json`、`docs/i18n/zh-CN/AI_USAGE_GUIDE.md`（若无则英文）。检测 OS、`git`、`python`/`uv`、Unity Editor、Blender、`uvx`。解析 UI 语言：对话 → `local.json` `ui_language` → 系统 UI → `en`。

### 第 2 步 — 提问（必须）

使用 `templates/i18n/zh-CN/INIT_QUESTIONNAIRE.md`。至少覆盖：

0. **界面语言**（en / zh-CN / ja / ko）；对话已是中文则可跳过，仍写入 `local.json` 的 `ui_language`。
1. **安装根**（默认：本 clone）。
2. **Blender** 路径与版本（目标 **5.2 LTS**）。
3. **Unity Editor**（角色管线 **2022.3 LTS**，不要用 Unity 6）。
4. **角色 Unity 工程**路径（没有改模任务可先空）。
5. **MCP**：只要文档 / 只要 Blender / 只要 Unity / 都要 / 都不要。
6. **AI 客户端**。
7. 是否 clone 可选 vendors（CATS 5.2、gummidot 文档、Codex VRC skill）。

不要猜测别人的 Unity 工程路径。

### 第 3 步 — 计划

将写入的文件（`local.json`、`mcp/local.mcp.json`）、将 clone 的 vendors、**不会**加入用户全局的 MCP。等确认。

### 第 4 步 — 执行（确认后）

1. `powershell -File scripts/bootstrap.ps1`（dry-run）。
2. `-Apply`（从模板写本机 MCP JSON；若无则填 `local.json`）。
3. 可选 `-CloneMcp`。
4. 钉选：`scripts/refresh-pins.ps1`（优先 `gh api`）。
5. 冒烟：Blender `--version`，若有 uv 则 `uvx --python 3.11 blender-mcp==<pin> --help`。
6. 以 `skills/vrc-review` 收尾。

### 第 5 步 — 报告

落地了什么、跳过了什么、剩余风险（上传仍须人点）。用中文写给中文用户。

---

## 2. MCP 策略

- 技能始终可读；MCP 进程只在本任务编辑活场景时启动。
- 同一时间只有一个 blender-mcp **客户端**（Cursor **或** Claude Desktop，不要两个一起）。
- Unity：在**已打开的工程**里装 CoplayDev unity-mcp（HTTP `http://localhost:8080/mcp`），和/或 VPM 上的 lighfu UnityAgent。官方 Unity 6 MCP / `com.unity.ai.assistant` 不要进 2022.3 角色工程。
- 没有名为 UnityMCP-VCC 的活仓库。不要发明它。

---

## 3. 管线

2026-09 步骤见 [docs/i18n/zh-CN/WORKFLOW.md](docs/i18n/zh-CN/WORKFLOW.md)。简图：

```
Blender  --blender-mcp-->  FBX / VRM
Unity 2022.3  --unity-mcp / UnityAgent-->  MA / 菜单 / 人审
人: SDK Build & Publish
```

网格 / 权重 / 口型 / CATS / 骨骼名 → Blender。
MA Merge Armature、菜单、参数、PhysBone、FaceEmo、lilToon → Unity。
衣服**没有适配这套身体**：停止。Unity 合并修不好权重。

---

## 4. 做 / 不做

**做**

- 等人在 N 面板点了 **Start MCP Server** 再驱动 Blender。
- 优先用编辑器实时 API，不要手改 `.prefab` / `.unity` YAML。
- PhysBone 上限「修复」、删除 MA 组件、任何上传：先停下来问。
- 可复用事实写入 `notes/`（`templates/AFTER_ACTION.md`）。对话不是记忆。

**不做**

- 点 VRChat Build & Publish、调用 `upload_vrchat_avatar`、保存 SDK cookie。
- 往 2022.3 角色工程装官方 Unity MCP。
- 两个 GUI 客户端同时挂 blender-mcp。
- 把 Blender/Unity 服务写进四套运行时的**用户全局** MCP。
- 把会话 jsonl 当成当前 Unity 场景。

---

## 5. 每次实质任务之后

读 `docs/AGENT_EVOLUTION.md` 与 `skills/vrc-review/SKILL.md`。双轴打分。笔记进 `notes/`。本机评分可进 `Reports/`（gitignore）。

---

## 6. 语言

- **对话**：与用户相同（本文为简体中文）。把 `ui_language` 写入 gitignore 的 `local.json`。
- **公开 git**：英文为正文。
- **路径**：绝对路径，或相对安装根。

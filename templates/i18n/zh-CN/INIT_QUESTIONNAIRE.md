# 初始化问卷（vrc-dcc-workstation）

AI：写 `local.json` 或挂 MCP 之前问完。结构化选项 + 推荐默认。英文正文：[templates/INIT_QUESTIONNAIRE.md](../../INIT_QUESTIONNAIRE.md)。语言规则：[docs/i18n/zh-CN/I18N.md](../../../docs/i18n/zh-CN/I18N.md)。

## Q0. 界面语言

Agent 对话用哪种语言？
- [ ] English（`en`）
- [ ] 简体中文（`zh-CN`）
- [ ] 日本語（`ja`）
- [ ] 한국어（`ko`）
- 推荐：与用户正在打的字一致。写入 gitignore 的 `local.json` 字段 `ui_language`。git 提交说明保持英文。

## Q1. 安装根目录

本 clone 在哪里？
- 推荐：就是这个 clone 目录。

## Q2. Blender

- [ ] `blender.exe` 路径（目标：**5.2 LTS**）
- [ ] 本会话是否安装/启用 blender-mcp 插件？
- 推荐：先填路径；需要现场景时由人点 **Start MCP Server**。

## Q3. Unity

- [ ] Unity **2022.3 LTS** 编辑器路径
- [ ] 角色工程 `.unity` / 工程文件夹（没有改模任务可先空）
- 推荐：本角色管线用 2022.3，不要用 Unity 6。

## Q4. 本任务的 MCP

- [ ] 无（只要文档 / 技能）
- [ ] Blender stdio（`manifests/tools.json` 里的 `blender-mcp` 钉选）
- [ ] Unity HTTP（在**已打开**的工程里 UPM 之后：`mcpforunityserver` / CoplayDev）
- [ ] 两者都要
- 推荐：没有改现场景前都不要。绝不写进用户全局 MCP。

## Q5. 可选 vendors

- [ ] CATS Blender Plugin 5.2 fork（Alrauna）
- [ ] gummidot vrchat-agentic-tools 文档
- [ ] felixchaos vrchat-avatar-modding-skill
- 推荐：任务需要时再 clone（`bootstrap.ps1 -Apply -CloneMcp`）。

## Q6. AI 客户端

Claude Code / Codex / Cursor / Gemini / Copilot / Grok — 只生成对应入口文件。

## Q7. 红线（确认已理解）

- [ ] Agent 不会点 VRChat Build & Publish
- [ ] Agent 不会把官方 Unity 6 MCP 装进这个 2022.3 工程
- [ ] Agent 不会保存 SDK cookie

答完后先写短计划，再执行。

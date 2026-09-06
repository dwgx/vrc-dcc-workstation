# 干活初始化（丢这个文件夹）

英文正文：[templates/JOB.md](../../JOB.md)。聊天可用中文；合同与模板保持英文。

这不是**装站**。和 debugger 工位同一分法：技能 `description` 是**引导提示词**（任务明显是改模/DCC 就自动套用），**不要**把某一句中文写成开关。

`INIT_QUESTIONNAIRE.md` 只在主人要求**搭建 / 安装 / 初始化本 clone** 时用。

## 按意图分类（不是口令表）

| 主人意图 | 路径 |
|---|---|
| 初始化 / 安装 / 搭建**本 clone** | `AGENTS.md` 第 2 节问卷 |
| 改 VRChat 角色、衣服、菜单、口型、PhysBone、Blender/Unity DCC | **本文件** + `dcc-session.md` |
| 改或审计 VRChat **世界** / Udon / 场景 | `skills/vrc-world` + `docs/WORLD.md`（不要走角色 handshake） |
| 说不清，且 probe `station_memory: yes` | 走干活。必要时问一句。不要甩装站问卷 |
| 说不清、工位是空的、主人说「先搭起来」 | 走装站 |

不要把任何固定短语当成开关。说法会变。任务明显是改模就开工，不必等被点名。**没有默认角色。** `handshake.py` 的 `<avatar>` 来自 `notes/CURRENT.md` 或主人点名。

## 本 clone 被拿来干活时

cwd 可以是 home、本文件夹、或角色 Unity 工程。

1. 先 quote `session-probe`。`kind: dcc` 就停四运行时 CONTINUE。
2. 本 clone 是**工位**（合同、技能、`notes/` 记忆）。**不是**角色工程工作区。
3. 改模型写到 `local.json` 的 `unity_project`，而且要在**那个工程的窗口**。home 不准写角色 Unity 工程。工位窗口只改本 clone。
4. 先读一次 `AGENTS.md`（停线）。再读工位 `notes/CURRENT.md`（门，不是 INDEX）→ 冻结 → **改模必读** `slice-loop.md` → `python maps/handshake.py <avatar>` → `python maps/gate.py <avatar> begin <review-id>`；没点名才 `python maps/review.py next <avatar>` → 至多再一本 playbook。没有 `vrc_audit`：在 Unity 窗口跑 `scripts/install-vrc-dcc-tools.ps1`。不要发明 `execute_code`。新素体：`python maps/init_avatar.py <id>`。handshake 退出码 2 或已关窗口 = 停（新开对话）。不要每回合重读。
5. 指纹：`notes/`（何时 / 为何 / 改了什么）+ REVIEW。jsonl 不是记忆。快照里已关掉的窗口不要续。
6. 本会话有 `unityMCP` 才能改 Hierarchy。禁止用户全局 MCP。SDK Publish 人点。

Cursor 已经开在角色 Unity 文件夹时，主人用**任意措辞**点名这一刀即可。已经约 100 轮哑巴 MCP → **新开对话**。

把 `templates/avatar-project/` 拷进 Unity 不是必须的。

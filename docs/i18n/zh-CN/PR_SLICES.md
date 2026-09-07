# 公开 PR 切片

英文规范：[PR_SLICES.md](../../PR_SLICES.md)。

提交说明保持英文。未获主人要求不要 push / 开 GitHub PR。

| 切片 | 状态 | 范围 | 本片不要混入 |
|---|---|---|---|
| **S00-a** | 已落地 `9ba91ca` | 链接、MCP 默认策略、公共入口不预选角色 | 活体 `maps/<id>/` |
| **S00-b** | 已落地 | 身份 / POLICY 失败即停 | 角色内容、USB 包、第一个 mesh 兜底 |
| **Drop-on-agent** | 本树 | 英文提示词、装站问卷 Q8/Q9、技能不劫持别的仓库 | 用户全局技能拷贝 |
| **S00-c** | 本树 | 工具白名单 / JOB lease / MCP `isError` | 上传 API、真机 Editor |
| **S01-a** | 本树框架 | 世界 maps CLI（无 live dump；`world_*` 前缀不可调用） | 装进真实 Worlds 工程；live `world_*` HTTP |
| **S01-b** | 提议（需编译证据） | 三包：Core / 保留 Avatar `com.vrc-dcc.tools` / Worlds | 为了编译往 Worlds 工程装 Avatar SDK |
| **S01-c** | 提议（S01-b + 授权 Worlds 路径之后） | 只读 `world_probe` | 通用 `execute_code`；顺手做 dump/inventory |
| **S01-d** | 本树 schema | 证据指纹 / STALE / `mutation_revision` / 有主 plan | 把 Python PASS 当成进世界 |
| **Chat 吸收 2026-09-07** | 本树 | 改写两套 Editor / 未实现 `world_*` / STALE 矩阵 | 把 zip 或 900KB JSON 提交进 git |

怎么跑循环：[ITERATION.md](../../ITERATION.md)。S01-b/c 是定制适配器路线，实际 World 制作通过[现有工具](WORLD_PRODUCTION.md)推进。World CLI 已取消 Avatar SKU / 单会话单片限制，保留租约互斥与变更版本；网页交接模板和检查器按需采用。

# 公开 PR 切片

英文规范：[PR_SLICES.md](../../PR_SLICES.md)。

提交说明保持英文。未获主人要求不要 push / 开 GitHub PR。

| 切片 | 状态 | 范围 | 本片不要混入 |
|---|---|---|---|
| **S00-a** | 已落地 `9ba91ca` | 链接、MCP 默认策略、公共入口不预选角色 | 活体 `maps/<id>/` |
| **S00-b** | 已落地 | 身份 / POLICY 失败即停 | 角色内容、USB 包、第一个 mesh 兜底 |
| **Drop-on-agent** | 本树 | 英文提示词、装站问卷 Q8/Q9、技能不劫持别的仓库 | 用户全局技能拷贝 |
| **S00-c** | 本树 | 工具白名单 / JOB lease / MCP `isError` | 上传 API、真机 Editor |
| **S01-a** | 本树框架 | 世界 maps CLI（无 live dump） | 装进真实 Worlds 工程；live `world_*` HTTP |
| **S01-b** | 之后（先 Chat 研究） | Core / Avatar / World 程序集 | 为了编译往 Worlds 工程装 Avatar SDK |
| **S01-c** | 之后 | 只读 `world_*` | 通用 `execute_code` |
| **S01-d** | 本树 schema | 证据指纹 / STALE / 有主 plan | 把 Python PASS 当成进世界 |

怎么跑循环：[ITERATION.md](../../ITERATION.md)。本页不要求已经存在可调用的 `world_*`。

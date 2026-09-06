# 公开 PR 切片

英文规范：[PR_SLICES.md](../../PR_SLICES.md)。

提交说明保持英文。未获主人要求不要 push / 开 GitHub PR。

| 切片 | 状态 | 范围 | 本片不要混入 |
|---|---|---|---|
| **S00-a** | 已落地 `9ba91ca` | 链接、MCP 默认策略、公共入口不预选角色 | 活体 `maps/<id>/` |
| **S00-b** | 本轮树内 | 身份 / POLICY 失败即停 | 角色内容、USB 包、第一个 mesh 兜底 |
| **S00-c** | 之后 | 工具白名单 / JOB lease | 上传 API |
| **S01-a** | 文档草稿 | 世界技能、世界模板、路由 | 装进真实 Worlds 工程 |

怎么跑循环：[ITERATION.md](../../ITERATION.md)。本页不要求已经存在可调用的 `world_*`。

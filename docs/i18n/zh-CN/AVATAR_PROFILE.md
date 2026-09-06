# 角色档案（任意素体）

英文规范：[AVATAR_PROFILE.md](../../AVATAR_PROFILE.md)。

本骨架**没有默认角色**。外来 clone / 公开 PR 不得把某一只商店角色（含作者活体）当成产品。

| 层 | 位置 | 是否进 git |
|---|---|---|
| 怎么改模 | `skills/vrc-dcc/references/` | 是 — 通用 |
| *这只*身体 | gitignore 的 `maps/<avatar>/` + `OWNER.md` | 否 |
| 合成结构示例 | `examples/composite-avatar.md` | 是 — 标明示例；没有对应工程 |

## 门

1. 主人点名 id，或 `notes/CURRENT.md` 的产品表点名。
2. **读取 / 审计 / 检查：** 若没有 `maps/<id>/`，报告缺失并停止。不要因为打开了 playbook 就跑 `init_avatar.py`。
3. **新建档案：** 只有主人要求播种时才 `python maps/init_avatar.py <id>`（目录已存在则拒绝）。
4. `python maps/handshake.py <id>` — **必填参数**。CLI 不默认角色名。
5. 活体事实：`STATE.md`、`MAP.md` **确定**、`POLICY.json`、`conflicts.json`、`REVIEW.json`。

工位 vs 产品 vs 后续世界域：[DOMAINS.md](../../DOMAINS.md)。公开骨架怎么迭代：[ITERATION.md](../../ITERATION.md)。

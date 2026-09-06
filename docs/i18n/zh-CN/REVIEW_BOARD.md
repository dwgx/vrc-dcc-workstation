# Review board（改模审查板）

英文：[`../../../skills/vrc-dcc/references/review-board.md`](../../../skills/vrc-dcc/references/review-board.md)。

MAP 记的是**头像上有什么**。审查板记的是**证过没有**。新写的东西默认 `unreviewed`。

- 源：`maps/<avatar>/REVIEW.json`
- 给人看：`python maps/review.py render <avatar>` → `REVIEW.md`
- 给 agent 的队列：`python maps/review.py next <avatar>`（可加 `--json`）
- 状态：`unreviewed` / `edit`（Editor 转储） / `world`（人在 VRChat 认了，`owner_ok`） / `accepted` / `blocked` / `wontfix`
- 走路、棉花糖晃、PCS 声音、SDK bit = `world`。衣服静息/乳首可以 `edit`。他体服权重 = `blender`
- 同一刀 Unity 改完就要 upsert 行。失败做法写进 `lessons[]`。不要因为 YAML 成功就标 `world`
- `python maps/review.py coverage <avatar>` 列出 MAP 里还没行的 plugin/outfit/menu
- 截图可选：`maps/<avatar>/evidence/`，evidence `kind: screenshot`
- 别人的开源 agent 包不要装进**这只**角色工程。不要开第二套 Unity MCP。

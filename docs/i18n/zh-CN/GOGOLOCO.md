# GoGoLoco（店里走路 vs 菜单切 GoGo）

英文：[`../../../skills/vrc-dcc/references/gogoloco.md`](../../../skills/vrc-dcc/references/gogoloco.md)。审查板：[`../../../skills/vrc-dcc/references/review-board.md`](../../../skills/vrc-dcc/references/review-board.md)。

- 默认走路/蹲/趴：**这只角色 MAP / OWNER / `conflicts.json` 写的**，不是某个写死的商店名。很多日系身是店里 Base（`paryi_Loco` 只是其中一种）。菜单 Bool 可切 GoGo。
- GoGo Base MergeAnimator 必须 **开着 + Append**，再靠 NDMF `vrc-dcc.loco-switch` 插 **WD-OFF 空状态**。
- **不要**「把 Base 组件勾掉」。MA 照样烘焙禁用的 MergeAnimator；**Disabled + Replace 仍会清掉店里走路**。
- **不要** Base **Replace**（`Go/Locomotion` 关掉也只是 GoGo 的 still/FBT）。**不要** Append 却不做 passthrough（双走路）。
- GoGo **动作/表情**：若店里 Action 已用 `VRCEmote`，Action = **Replace**。ABT / AFK 赢家见 [PLUGIN_CONFLICTS.md](PLUGIN_CONFLICTS.md)。
- Booth 同步大约 16 bit。走路只能世界上传证，Editor Play 不算。

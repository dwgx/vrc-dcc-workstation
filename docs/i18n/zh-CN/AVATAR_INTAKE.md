# 改模开局（任意角色）

英文：[`../../../skills/vrc-dcc/references/avatar-intake.md`](../../../skills/vrc-dcc/references/avatar-intake.md)。本骨架**没有默认角色**。[AVATAR_PROFILE.md](../../AVATAR_PROFILE.md)。

1. 主人点名 id，或 `notes/CURRENT.md` 产品表。
2. 没有 `maps/<id>/`：`python maps/init_avatar.py <id>`。
3. `python maps/handshake.py <id>`（必填；CLI **不会**默认某个商店名）。
4. 读 `STATE.md` + MAP **确定**，再 `vrc_audit`。不要猜 Booth 上另一只同名角色。

然后 dump：哪张 mesh 是脸/身体、骨架名、菜单从哪来、默认走路、插件在不在头像上。示例（不是默认产品）：[`examples/composite-avatar.md`](../../../skills/vrc-dcc/references/examples/composite-avatar.md)。

NDMF「部分纹理未启用 Mip Streaming」：agent 自己开 `streamingMipmaps`，不要让人点自动修复，也不要点「进行测试构建」。

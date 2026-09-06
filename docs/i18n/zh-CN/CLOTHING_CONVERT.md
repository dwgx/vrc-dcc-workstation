# 衣服换素体（MA 合并 ≠ 改好的衣服）

英文：[`../../../skills/vrc-dcc/references/clothing-convert.md`](../../../skills/vrc-dcc/references/clothing-convert.md)。贴合见 [CLOTHING_FIT.md](CLOTHING_FIT.md)。菜单见 [CLOTHING_MENU.md](CLOTHING_MENU.md)。

这是工位通用知识。先认**衣服为哪具素体做的**、**这只活体是谁**。融合身、原版素体、Booth 上另一个同名 SKU 是三份工作。不要把示例融合身当成默认角色。

## 停

- Merge Armature 只按名字挂骨骼，**不改权重**。
- **不要默认 0.95**。那是某些店里转换 PNG 上的一格指标，还写着微调整。优先用**这只目标**的官方预制、scale 1，除非量过。
- PNG 上的名字是**那几具素体**。不要把第三张没写的 mesh 套进去。`neck 1.01` 是脖子局部缩放，不是头高 1.01 m。
- 鞋陷地 **并且** 脚/屁股/胸/头发一起穿 = 迁移动作，不是再做一次 BSS，也不是只抬鞋 Y。
- CATS 5.2 的 ShapeKeyApplier **不会** 把 shapekey 拷到另一张拓扑上。权重用 Blender Data Transfer。
- 手持/名牌/掉地上的胖次：**不是** Merge 衣服。`BoneProxy` KeepWorldPose 会保住**当前世界坐标**。预制丢在 `功能/饰品` 原点 = 钉在脚边。先在 Edit 把物体放到 Head / 右手 / 髋，再 dump bounds。**贴着手腕骨头（dRH≈0）不是握在手里** — 还要量手腕到食指尖，中心大约在这条轴的 0.4–0.6。`AsChildAtRoot` 会丢掉掌心偏移。约束四个源 Weight 全 0 = 不跟。
- **主看齐：** 有几个挂点就量几处。香蕉要摆四个锚点（右掌/左掌/胸前/髋前），不要只挪被约束的子物体。VRC 约束看 `Locked` / `PositionAtRest`。Owner 自己摆过就不要再覆盖。卸掉饰品后还要扫菜单宿主上的 MA Parameters 残留名。美甲手和脚是两套 BakeMesh。骨头 d=0 但网格不在甲床 = 绑定位移；Toe 是 Foot 的子级，delta 只能加一次。网格物体平移带不动蒙皮。详细表：英文 playbook §11。
- 包里没有匹配 POLICY `body_token` 的预制（通用世界道具）**不要往这只身上挂**。髋高对不上也算没合上。一次只挂一件，Owner 看过再下一件。

## 怎么选路

1. 先认 **衣服是为哪具素体做的**、目标头高/胸高。
2. 胸形状名不对 / 多出来 `Breast_*.002` → Unity BSS + BoneProxy KeepWorldPose。
3. 只有鞋陷、其它都跟身 → 可以试鞋 Y。
4. 走动头发穿 → 身体上的 PhysBone 碰撞（不要挂会随衣服关掉的 Physics）。
5. 漂、肘拧、裆漏、多部位一起穿 → **Blender**，新 FBX。
6. 只有棉花糖挤的时候胸穿 → 厂商 貫通防止 / MaxSquish；不要保证完全不穿。

哥特格子（GothicLolium-rurune）BSS+BoneProxy 已经做过。还剩鞋陷地+多部位穿，按第 5 条，不要再猜缩放。

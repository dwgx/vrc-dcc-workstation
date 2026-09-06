# 衣服贴合（MA 合并 ≠ 改好权重）

完整英文 playbook：[`../../../skills/vrc-dcc/references/clothing-fit.md`](../../../skills/vrc-dcc/references/clothing-fit.md)。菜单层见 [CLOTHING_MENU.md](CLOTHING_MENU.md)。**换素体 / 他体服：** [CLOTHING_CONVERT.md](CLOTHING_CONVERT.md)。

Merge Armature **只把骨骼对上**，不重建权重、不补 blendshape、不把衣服多出来的 `Breast_L.002` 接到棉花糖。不是为**这张** mesh 做的衣服 → Blender。

- 开关/换色/shrink/乳首 → Unity MA（clothing-menu）。
- 胸跟不住、衣服有 `Breast_*.002`、形状名对不上 → Unity BSS remap + BoneProxy `AsChildKeepWorldPose`。棉花糖和 SPS/PCS 孔：[MARSHMALLOW_ERP.md](MARSHMALLOW_ERP.md)。
- 漂、肘拧、裆漏 → **停，Blender/CATS**。不要猜商店 PNG 上的缩放或乱加身体 morph。
- 名牌/手里道具/掉地上胖次钉在脚边 → KeepWorldPose 丢在原点，或约束 Weight 全 0。先放到对应骨头再 dump。POLICY 对不上预制 **不要 Instantiate**。见 [CLOTHING_CONVERT.md](CLOTHING_CONVERT.md)。
- 厂商某个配色文件夹只有 3 张 mat → 不要编 14 个 swap。
- 店里原装鞋常常挂在原装衣服根下，关原装套就关鞋。

Edit 里用 `AvatarObjectReference.Get`，不要只查 `targetObject`（会假报 missOT=0）。

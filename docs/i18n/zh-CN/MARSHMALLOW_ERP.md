# 棉花糖 / SPS / PCS

完整英文：[`../../../skills/vrc-dcc/references/marshmallow-erp.md`](../../../skills/vrc-dcc/references/marshmallow-erp.md)。衣服骨骼见 [CLOTHING_FIT.md](CLOTHING_FIT.md)。

- Edit 里 `Breast_L` PhysBone 关着、棉花糖在 Dummy 里，是 **NDMF 烘焙才挂上**，不是没装好。不要为了看晃专门进 Play（VRCFury 触觉 bake 会卡）。
- 孔跟 **Head / Chest / Hips**，不要跟 `Breast_L` 或棉花糖 Dummy。SPS 胸 / PCS Boobs → Chest。
- 融合身没有原版 `upperArm_*_collider`，要在身体大臂上自建碰撞再塞进 Setup 槽，不要借用女仆衣服 Physics。
- `Body_b` 静息是胸小=100，棉花糖 blend 保持 0。菜单已经在 `菜单/功能/胸`，不要再开 Setup 里的 `_marshmallowPBEnabled`。
- 貫通防止：`_breastInterference_BreakPreventionCollider`。走路/挤压穿布：先把 `_buffer_limit_colider_position` 往 1 调（官方优先），再降 MaxSquish。**活体数值写进 MAP**，不要抄另一只角色。布料仍可能穿，不要保证零。官方：https://wataame89.github.io/documents-wataameya/en/marshmallowPB/trouble/
- 不要在衣服上把身体 `Breast_small` 打成 0（身体变大，棉花糖碰撞还是小的，乳首和胸更容易穿出）。
- 音效：VRC 同时只播 **3** 个 AudioSource。`pcs/isEnable` 厂商默认关；ぱいたっち不要 `playOnAwake`。Edit 里 PCS `clip=null` 是烘焙才赋值。
- 屌默认 **中 0.88**（`SPS_DickSize=1`）。

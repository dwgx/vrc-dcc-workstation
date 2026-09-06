# 衣服菜单（Modular Avatar）

<!-- I18N:START -->
[English](../../CLOTHING_MENU.md) · **简体中文**
<!-- I18N:END -->

国内 Booth / 改模店衣服菜单基本是三层。**按这只角色自己的 MAP 填 Int**，不要抄另一只身的套装编号。**穿上胸不对 / 骨骼：** 先读 [CLOTHING_FIT.md](CLOTHING_FIT.md)。

## 三层，别混在一个子菜单里

| 层 | 玩家怎么点 | 参数 | 同步 bit |
|---|---|---|---|
| **套装** | 互斥开关（轮盘） | Int，`Clothes` 0=制服 1=女仆白 2=女仆黑 | **8** |
| **穿脱** | 每件开关，默认穿上 | Bool，一件（或一组 mesh）一个 | **各 1**（要给别人看就同步） |
| **颜色** | 互斥开关 | 每个**独立区域**一个 Int | 同步 **8**；`isSynced=false` 则 **0** |

子菜单（SubMenu）**不要填参数名**。填了 `衣服` / `FS` 这种，MA 仍会往表情参数表里塞。

VRC 一页最多 **8 个控件**。穿脱超过 8 件就「第一页 + 更多」。

## 国内常见做法（「轮盘」指什么）

- **套装轮盘**：一个 Int，不要两个 Bool 互打。`0` 是店里原装，不是真空。
- **穿脱**：Bool，`isDefault=true`。和默认内衣用**同一套**静息：
  - 场景里 mesh **关**，ObjectToggle `Inverted=false` + `Active=true`（开=穿上，关=恢复隐藏）。
  - **不要**在「场景里开着」的套装单件上用倒转隐藏。NDMF 会按 `InitiallyActive XOR Inverted` **改写**物体静息，关开关变成恢复新静息，穿脱等于没接线（或者一进套装就是脱光的）。
  - 套装**根**可以关着（`Clothes` Int 负责打开）。根下面的单件仍然要静息关，穿脱 Bool 才有隐藏可恢复。
- **店里 shrink vs 后加套装**：身体 FX 常常在原装 mesh 关掉之后还在播 shrink。后加套必须把那些形态打 0，并且把店里 Bool 写成 0。**Idle（`Clothes==0`）必须把 Bool 设回 MA 默认**。VRC 的 Int Toggle 关掉时参数变成 **0**。多个 ObjectToggle **层级里靠后的赢**，默认内衣排在后加套上面。
- **本体内衣 vs 套装胸罩/内裤**：不是同一块 mesh（`Bra`/`Pants` vs `FS_Bra`/`FS_Panty`）。后加套常常 ObjectToggle 关掉本体 `Bra`/`Pants`。多个 ObjectToggle 同时生效时**层级里靠后的赢**，所以 **默认内衣必须排在后加套上面**。否则内衣（默认开）会在后加套下面把本体内衣又打开。
- **颜色轮盘**：同一参数的兄弟项 `automaticValue=true`。默认项 `isDefault` 得到 0，其余 1、2… `value>1` 会变成 Int（8 bit）。只有白/黑时用 Bool 更省。
- **叠加**：翅膀、尾巴、兔耳、蝴蝶结是套装 Int **之上**的 Bool，Toggle 的是**单件 mesh**，不是整套根（根已经给 `Clothes` 管了）。
- **黑白两套网格**：精修只做一套（白）的穿脱和颜色；另一套先整套切换，别把 bit 付两遍。

## 省参数（加下一个 Int 之前先做）

1. **互斥颜色用 Int 轮盘**，不要 N 个 Bool。只有两色时用 1 bit Bool。
2. **别人看不见的颜色**（金属、丝袜、蝴蝶结）`isSynced=false` / MA Parameters `localOnly`。穿脱 Bool 保持同步。
3. **一套配色一个 MaterialSwap**（在套装根上 UV1–UV5 From→To），不要每个 UV 一个 Int。
4. **金属槽合并**成一个 `FS_Metal`（金/玫/银），不要「挂饰 + 腿环」两个 Int。
5. 两个轮盘**禁止共用一个参数**。围裙和蝴蝶结都写 `FS_Apron` 会变成 16 选 1，看起来像「蝴蝶结坏了」。
6. 烘焙前数 `VRCExpressionParameters`。重名（同一 token 既 Float 又 Bool）既费 bit 又让 MA 抽风。
7. 穿脱按玩家真会脱的组（上衣+领+袖褶），不要每个丝带骨骼一个 Bool。一件饰品一个同步 Bool，一轮就会吃掉大约 33 bit。
8. **不要在衣服开关动画上猜身体 morph**（皮鞋 ON/OFF 上加 `Foot_heel_OFF` 会把脚肉顶出鞋口，看起来像白衣服被改坏）。贴合剩余问题走 Blender 或单独的收脚 clip，不要改厂商原来只开关 Renderer 的动画。
9. **VRCFury 的 FullController 参数**必须先以 **MA Parameters** 挂在同一物体上，否则 NDMF `FixupExpressionsMenuPass` 会把菜单参数名清掉，PCS 点了没反应。烘焙残留的 VF 压缩器参数：没被菜单引用的删掉。
10. 同一只角色不能把 256 bit 拆成两次上传。精简版 = 另一只上传的模型。大小轮盘（`SPS_DickSize` Int）占 8 bit，别人不必看见就 `localOnly`。

颜色别人看不见就 local；穿脱同步。总预算压在 256 以下。活体数字写 MAP，不要抄 dated notes。

## MA 接线（用编辑器 API，不要手改 prefab YAML）

- 套装 Int：Toggle，`automaticValue=false`，写死 0/1/2，默认在 0。ObjectToggle 显示该套装根、关掉另外几套。
- 穿脱：Toggle + ObjectToggle，只指**白**套 mesh。默认开。
- 颜色：整套配色用 `MaterialSwap`（`m_root`=白套）。单件单槽用 `MaterialSetter`（物体 + material index）。
- **蝴蝶结 vs 围裙**：两边都写 `FS_Apron` 的 index 1 就会互打。围裙改围裙 mesh 的槽；蝴蝶结改 `FS_Ribbon*`。
- 乳首（每次改模都要查）：遮胸 mesh 上**不倒转** Set `Nipple_On=0` / `Up=0` / `Small=100`。胸罩/内衣 MenuItem **倒转** Set `On=100` / `Up=100` / `Small=0`。不要挂套装 Int，不要倒转挂静息关着的 `FS_Bra`。`Nipple_On=0` 不等于底模没有乳首。棉花糖静息胸小的时候，不要在衣服上把身体 `Breast_small` 打成 0（身体会变大，反而顶出衣服）。

MCP 里禁止 `EditorUtility.DisplayDialog`。SDK Publish 人点。

## 原版衣服 vs 后加的衣服

不要把店里原装和后来加的 Booth 服当成同一个 ObjectToggle。每套衣服一行 MAP + 一行 REVIEW。

| 车道 | 典型 | 还原 | 合身残留 |
|---|---|---|---|
| **店里原装** | 身体 FX Bool。套装 `0` | Idle 要把 Bool **写回厂商默认**。OT 只还原 mesh | 不要在厂商 clip 上猜身体 morph |
| **后加整套** | 套装 Int + OT，不付穿脱 bit | Int 关 → `0`（原装） | 对不上的多余骨骼 → BoneProxy KeepWorldPose 或 Blender。Merge Armature ≠ 改好了 |
| **后加穿脱** | Int + 同步 Bool，场景静息 **关** | 和内衣同一套 OT。后写的 OT 赢 → 默认内衣在上面 | 乳首遮盖 SC 挂 **mesh**，不要挂套装 Int |
| **默认内衣** | 静息关的 `Bra`/`Pants` | 不是缺件 | 店里 Bool 卡在 0 会出现两件胸罩 |

新衣服：先实例化、Edit 里打开给人看，**再**加 bit。审查：`python maps/review.py coverage <avatar>`。

## 示例菜单树

不要抄另一只角色的 Int。活体写 `maps/<avatar>/`。英文示例：[composite-avatar.md](../../../skills/vrc-dcc/references/examples/composite-avatar.md)。

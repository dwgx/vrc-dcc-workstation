# 分域（角色 vs 世界 vs 本工位）

英文规范：[DOMAINS.md](../../DOMAINS.md)。

公共仓库名保持 **`vrc-dcc-workstation`**。不要改成私有世界产品名。

英文是规范正文。下列中文入口与红线、意图路由保持一致。若某语言页不存在，用英文页；不声称译文对等。

| 层 | 是什么 | 在哪 |
|---|---|---|
| **工位** | 合同、技能、命名 Editor 工具、maps CLI | 本 clone |
| **角色产品** | 一棵 Unity 2022.3 角色树 | `local.json` `unity_project`。活体 `maps/<avatar>/` gitignore |
| **世界产品** | 一棵 Worlds / Udon 树 | 主人覆盖层。不是这个 GitHub 仓库。公开世界技能是后续 **S01-a** |

不要把世界 ID、贴图、活体 overlay map 提交进 git。角色档案：[AVATAR_PROFILE.md](AVATAR_PROFILE.md)。

## 按意图走

| 意图 | 技能 / 门 |
|---|---|
| 安装 / 搭建**本 clone** | `AGENTS.md` 第 2 节 |
| 角色 / 衣服 / MA / PhysBone | `templates/JOB.md` + `skills/vrc-dcc` |
| 世界 / Udon / 场景 | 后续公开切片 **S01-a**。不要自动加载尚不存在的世界技能。不要走角色 `handshake.py` |
| 改钉选 / 技能 / 文档 | `docs/MAINTAIN.md` |

切片计划：[PR_SLICES.md](../../PR_SLICES.md)。SDK **Build & Publish** 仍由人点。

# 基线怎么迭代

英文规范：[ITERATION.md](../../ITERATION.md)。

这是**工位**循环，不是改某一只角色，也不是 Worlds 真机编辑。公开 git 保持英文。Overlay 不进 git。

仓库名锁定：**`vrc-dcc-workstation`**。

## 「最好的 base」指什么

外来 clone / 公开 PR 能改**任意点名的角色**，不会继承作者那只店货。Agent：`templates/JOB.md` → `handshake.py <avatar>` → `gate.py` → 命名 `vrc_*`。人点 SDK **Build & Publish**。

没有 Play / Gesture Manager / PCVR 证据，不要说角色已经修好。离线测试是 `PASS`；没有 Editor 的编译是 `NOT_RUN`。

## 片顺序

S00-a 已在 `9ba91ca` 落地。S00-b（身份失败即停）在本树。丢给 agent 的英文提示词与「别劫持别的仓库」也在本树（[DROP_ON_AGENT.md](../../DROP_ON_AGENT.md)）。**S00-c**（工具白名单 / JOB lease）在本树。World **框架**（handshake/gate，无 live dump；`world_*` 前缀不可调用）与证据指纹 / `mutation_revision` schema 在本树。2026-09-07 Chat 结论已改写成 [FRAMEWORK.md](../../FRAMEWORK.md)（两套 Editor、三包名、S01-c 只做 `world_probe`）。本 clone 的活下一片在 gitignore 的 `notes/HANDOFF.md`。S01-b/c 只约束定制工位适配器的研发顺序；实际 World 制作使用[现有工具](WORLD_PRODUCTION.md)，无需等待这些切片。World maps 已支持同一操作者连续切片、不继承 Avatar SKU 配额，并在 reset 后保留变更版本。完整表见英文页与 [PR_SLICES.md](../../PR_SLICES.md)。架构：[FRAMEWORK.md](../../FRAMEWORK.md)。

网页 / Astra 可以继续搜。进 git 的是**规则**，不是 ZIP 也不是底模。见 [SOURCES.md](../../SOURCES.md)。

# 公开骨架存什么

英文规范：[SOURCES.md](../../SOURCES.md)。

**不要**把海量底模、Booth 包、USB 货架、世界 15 张贴图打进 git。那些在 overlay / Unity 工程 / 硬盘货架。公开仓库只存：任意点名角色的握手、身份失败即停、改模规则、命名 `vrc_*`、丢给 agent 的提示词、迭代循环。

ChatGPT / Codex web can keep searching. Promotion happens here after a slice, not by accumulating unread archives. 2026-09-07 S01 研究已吸收进 [FRAMEWORK.md](../../FRAMEWORK.md)；zip 与 JSON 留在 overlay。

lilycalInventory / FaceEmo 只在**这只角色已经装了**时当检查路径，不是本站默认衣服方案（默认仍是 Modular Avatar 的国风店菜单）。证据层级：[evidence-layers.md](../../../skills/vrc-dcc/references/evidence-layers.md)。

## 资料库与实现候选

按具体问题学习：[source-learning.md](../../../skills/vrc-dcc/references/source-learning.md)。
需要独立收集者时，使用可选的 [研究执行者模板](../../../templates/RESEARCH_EXECUTOR.md)，
由执行者返回来源与结果，主控决定如何吸收；已有工程格式可继续使用。

| 来源 | 可学习内容 | 吸收前核对 |
|---|---|---|
| [vrc-mod-guide](https://dwgx.github.io/vrc-mod-guide/) / [源仓库](https://github.com/dwgx/vrc-mod-guide) | World/Avatar 资源发现、原创教程正文、视频元数据与存档指针 | 实际读取相关正文；历史可信度标签或链接存活不等于技术结论仍然有效。链接资产的使用条件单独核对。 |
| [blender-copilot](https://github.com/dwgx/blender-copilot) | 尺寸测量、网格检查、UV/材质、导出及角色参数的实现方法 | 从工具注册追到处理函数和返回值；区分启发式、生成模板与实测功能。现场使用前核对目标实例和已装版本。 |
| [VRCD 文档入口](https://docs.vrcd.org.cn/books/vrc-YcF/page/vrc) | 中文社区文档及相关 World/Avatar 方法线索 | 记录具体读过哪些页面；重要 SDK/工具结论回到当前原始文档核对。 |

资料库用于发现和发展方法。研究完成、方法落地和工程验收分别记录；后续按用户方向继续，
无需因此创建定期自动维护。

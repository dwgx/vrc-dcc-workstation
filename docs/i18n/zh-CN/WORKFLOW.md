# 工作流（Blender → Unity → 人点 Publish）

<!-- I18N:START -->
[English](../../WORKFLOW.md) · **简体中文** · [日本語](../ja/WORKFLOW.md) · [한국어](../ko/WORKFLOW.md)
<!-- I18N:END -->

钉选：`manifests/tools.json`（用 `scripts/refresh-pins.ps1` 复核；GitHub **releases** 优于第三方 VPM 目录）。本页是 2026-09 公开管线。

```
Blender 5.2 LTS  --blender-mcp-->  FBX / VRM
Unity 2022.3 LTS --CoplayDev HTTP + named vrc_*-->  MA / NDMF / menus
Human: VRChat SDK Build & Publish
```

## 0. 握手

1. 读 [AGENTS.zh-CN.md](../../../AGENTS.zh-CN.md)。用 `scripts/bootstrap.ps1 -Apply` 从 `local.json.example` 填 `local.json`。
2. **不要**把 Blender / Unity MCP 写进 Claude / Codex / Cursor / Grok **用户全局**配置。
3. 加包或驱动编辑器时，在**角色 Unity 工程自己的窗口**里打开。

## 1. Blender（网格 / 权重 / 口型 viseme）

目标编辑器：**Blender 5.2 LTS**。用 `manifests/tools.json` 里钉选的 PyPI `blender-mcp` 连接（默认 Python 是 3.14+ 时，在 `uvx` 下用 CPython **3.11**）。

1. 人：启用 **Interface: Blender MCP**，N 面板 **Start MCP Server**（端口 9876）。
2. 客户端：`uvx --python 3.11 blender-mcp==<pin>`，需要时设 `UV_PYTHON_PREFERENCE=only-managed`。
3. 同一时间只有一个 blender-mcp **客户端**（Cursor **或** Claude Desktop，不要两个一起）。
4. 权重、口型、骨架名、CATS（可选 vendor `Alrauna/Cats-Blender-Plugin`）留在 Blender。
5. 导出给 Unity 的 FBX。Humanoid 骨骼名必须在 Modular Avatar 合并前与**目标**骨架一致。
6. 衣服**还没适配**这具身体：**停**。Unity 的 MA 修不好权重。

若 5.2 拒绝 ahujasid：用清单里的 `dcc-mcp-blender` 钉选。

细节：`skills/vrc-dcc/blender.md`（技能正文为英文）。

## 2. Unity 2022.3（MA / NDMF / 菜单）

目标编辑器：**Unity 2022.3 LTS**（本角色管线不要 Unity 6）。

在**已打开的角色工程**里（不是 home / 控制面窗口）：

1. 按 `manifests/tools.json` 的 `upm` 字段加入 CoplayDev MCP for Unity。
2. Window → **MCP for Unity** → Start（HTTP `http://localhost:8080/mcp`）。
3. 不要加 lighfu UnityAgent / EditorEye / 第二套 Unity MCP。
4. 用 **MA Merge Armature** / Menu Installer / Parameters 合衣服。未经要求不要 bake NDMF。衣服表情菜单：[CLOTHING_MENU.md](CLOTHING_MENU.md)。
5. 优先命名 `vrc_*`，不要手改 `.prefab` YAML。不要发明 `execute_code` / `execute_csharp`。
6. 永远不要从 MCP 调 `EditorUtility.DisplayDialog`（会卡住编辑器）。

官方 Unity 6 MCP / `com.unity.ai.assistant` 对本 2022.3 工程保持**关闭**。不要把 TunaSync UnityMCP-VCC 或 swax/UnityMCP-VRC 当默认 Editor 桥。

包 URL：[UNITY.md](UNITY.md)。PhysBone：`skills/vrc-dcc/references/physbones.md`。

## 3. 人点 Publish + 世界里测

人点 VRChat SDK **Build & Publish**。Agent 不得点、不得调 `upload_vrchat_avatar`、不得存 SDK cookie。

Editor Play 可能卡在 VRCFury 触觉 bake，那不是衣服坏了。Build 过了之后在 VRChat 里测：[UPLOAD_TEST.md](UPLOAD_TEST.md)。店里走路 vs GoGo：[GOGOLOCO.md](GOGOLOCO.md)（默认走路是 MAP/OWNER，不是写死的角色）。

## 4. 任务结束后

`skills/vrc-review` → `notes/`（`templates/AFTER_ACTION.md`）。聊天不是记忆。

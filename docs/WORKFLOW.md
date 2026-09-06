# Workflow (Blender → Unity → human publish)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/WORKFLOW.md) · [日本語](i18n/ja/WORKFLOW.md) · [한국어](i18n/ko/WORKFLOW.md)
<!-- I18N:END -->

Pins: `manifests/tools.json` (re-check with `scripts/refresh-pins.ps1`; GitHub **releases** beat third-party VPM catalogs). This page is the 2026-09 public pipeline.

```
Blender 5.2 LTS  --blender-mcp-->  FBX / VRM
Unity 2022.3 LTS --CoplayDev HTTP + named vrc_*-->  MA / NDMF / menus
Human: VRChat SDK Build & Publish
```

## 0. Handshake

1. Read `AGENTS.md`. Fill `local.json` from `local.json.example` (`scripts/bootstrap.ps1 -Apply`).
2. Do **not** attach Blender/Unity MCP to Claude / Codex / Cursor / Grok **user-global** config.
3. Open the **avatar Unity project** in its own window when you add packages or drive the Editor.

Named `vrc_*` need a filled `POLICY.json` (`unity_root_name`). They do not pick the first avatar in the scene. Station iteration: [ITERATION.md](ITERATION.md).

## 1. Blender (mesh / weights / visemes)

Target editor: **Blender 5.2 LTS**. Connect with PyPI `blender-mcp` at the pin in `manifests/tools.json` (CPython **3.11** under `uvx` if the default Python is 3.14+).

1. Human: enable **Interface: Blender MCP**, N-panel **Start MCP Server** (port 9876).
2. Client: `uvx --python 3.11 blender-mcp==<pin>` with `UV_PYTHON_PREFERENCE=only-managed` when needed.
3. One blender-mcp **client** at a time (Cursor **or** Claude Desktop, not both).
4. Weights, visemes, armature names, CATS (optional vendor `Alrauna/Cats-Blender-Plugin`) stay in Blender.
5. Export FBX for Unity. Humanoid bone names must match the **target** armature before Modular Avatar merge.
6. Outfit **not adapted** to this body: **stop**. Unity MA will not fix weights.

Fallback if 5.2 rejects ahujasid: `dcc-mcp-blender` pin in `manifests/tools.json`.

Details: `skills/vrc-dcc/blender.md`.

## 2. Unity 2022.3 (MA / NDMF / menus)

Target editor: **Unity 2022.3 LTS** (not Unity 6 for this avatar pipeline).

In the **open avatar project** (not a home/control-plane window):

1. Add CoplayDev MCP for Unity from the `upm` field in `manifests/tools.json`.
2. Window → **MCP for Unity** → Start (HTTP `http://localhost:8080/mcp`).
3. Do **not** add lighfu UnityAgent / EditorEye / a second Unity MCP.
4. Merge clothes with **MA Merge Armature** / Menu Installer / Parameters. Do not bake NDMF unless asked. Clothing expression menus: [CLOTHING_MENU.md](CLOTHING_MENU.md).
5. Prefer named `vrc_*` over hand-editing `.prefab` YAML. Do not invent `execute_code` / `execute_csharp`.
6. Never `EditorUtility.DisplayDialog` from MCP (hangs the Editor).

Official Unity 6 MCP / `com.unity.ai.assistant` stays **off** this 2022.3 project. Do not use TunaSync UnityMCP-VCC or swax/UnityMCP-VRC as the default Editor bridge.

Package URLs: `docs/UNITY.md`. PhysBones: `skills/vrc-dcc/references/physbones.md`.

## 3. Human publish + in-world test

The human clicks VRChat SDK **Build & Publish**. Agents must not click it, must not call `upload_vrchat_avatar`, and must not store SDK cookies.

Editor Play may hang on VRCFury haptic bake — that is not a clothes failure. After a successful Build, the owner tests in VRChat: [skills/vrc-dcc/references/upload-test.md](../skills/vrc-dcc/references/upload-test.md). Shop loco vs GoGo: [gogoloco.md](../skills/vrc-dcc/references/gogoloco.md) — default walk is MAP/OWNER, not a baked-in character.

## 4. After the job

`skills/vrc-review` → `notes/` (`templates/AFTER_ACTION.md`). Chat is not memory.

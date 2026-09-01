# Workflow (Blender → Unity → human publish)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/WORKFLOW.md) · [日本語](i18n/ja/WORKFLOW.md) · [한국어](i18n/ko/WORKFLOW.md)
<!-- I18N:END -->

Pins: `manifests/tools.json` (re-check with `scripts/refresh-pins.ps1`; GitHub **releases** beat third-party VPM catalogs). This page is the 2026-09 public pipeline.

```
Blender 5.2 LTS  --blender-mcp-->  FBX / VRM
Unity 2022.3 LTS --CoplayDev HTTP + optional UnityAgent-->  MA / NDMF / menus
Human: VRChat SDK Build & Publish
```

## 0. Handshake

1. Read `AGENTS.md`. Fill `local.json` from `local.json.example` (`scripts/bootstrap.ps1 -Apply`).
2. Do **not** attach Blender/Unity MCP to Claude / Codex / Cursor / Grok **user-global** config.
3. Open the **avatar Unity project** in its own window when you add packages or drive the Editor.

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
3. Optional: lighfu UnityAgent via VPM `https://lighfu.github.io/vpm/` (`editor-v*` tag from GitHub releases).
4. Merge clothes with **MA Merge Armature** / Menu Installer / Parameters. Do not bake NDMF unless asked.
5. Prefer live Editor APIs (`execute_csharp` / UnityAgent tools) over hand-editing `.prefab` YAML.
6. Never `EditorUtility.DisplayDialog` from MCP (hangs the Editor).

Official Unity 6 MCP / `com.unity.ai.assistant` stays **off** this 2022.3 project. There is no live package named UnityMCP-VCC.

Package URLs: `docs/UNITY.md`. PhysBones: `skills/vrc-dcc/references/physbones.md`.

## 3. Human publish

The human clicks VRChat SDK **Build & Publish**. Agents must not click it, must not call `upload_vrchat_avatar`, and must not store SDK cookies.

## 4. After the job

`skills/vrc-review` → `notes/` (`templates/AFTER_ACTION.md`). Chat is not memory.

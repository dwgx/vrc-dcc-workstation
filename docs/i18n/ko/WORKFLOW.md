# 워크플로（Blender → Unity → 사람이 Publish）

<!-- I18N:START -->
[English](../../WORKFLOW.md) · [简体中文](../zh-CN/WORKFLOW.md) · [日本語](../ja/WORKFLOW.md) · **한국어**
<!-- I18N:END -->

핀: `manifests/tools.json`（`scripts/refresh-pins.ps1`로 재확인. GitHub **releases**가 서드파티 VPM 카탈로그보다 우선）. 이 페이지는 2026-09 공개 파이프라인입니다.

```
Blender 5.2 LTS  --blender-mcp-->  FBX / VRM
Unity 2022.3 LTS --CoplayDev HTTP + named vrc_*-->  MA / NDMF / menus
Human: VRChat SDK Build & Publish
```

## 0. 핸드셰이크

1. [AGENTS.ko.md](../../../AGENTS.ko.md)를 읽는다. `scripts/bootstrap.ps1 -Apply`로 `local.json.example`에서 `local.json`을 채운다.
2. Blender / Unity MCP를 Claude / Codex / Cursor / Grok **사용자 전역** 설정에 **붙이지 않는다**.
3. 패키지를 넣거나 에디터를 구동할 때는 **아바타 Unity 프로젝트 전용 창**에서 연다.

## 1. Blender（메시 / 웨이트 / viseme 입모양）

목표 에디터: **Blender 5.2 LTS**. `manifests/tools.json`의 PyPI `blender-mcp` 핀으로 연결（기본 Python이 3.14+이면 `uvx` 아래 CPython **3.11**）.

1. 사람: **Interface: Blender MCP**를 켜고 N 패널에서 **Start MCP Server**（포트 9876）.
2. 클라이언트: `uvx --python 3.11 blender-mcp==<pin>`. 필요하면 `UV_PYTHON_PREFERENCE=only-managed`.
3. blender-mcp **클라이언트는 한 번에 하나**（Cursor **또는** Claude Desktop. 둘 다 금지）.
4. 웨이트, viseme, 아마추어 이름, CATS（선택 vendor `Alrauna/Cats-Blender-Plugin`）는 Blender에 둔다.
5. Unity용 FBX를 보낸다. Humanoid 본 이름은 Modular Avatar 머지 전에 **대상** 아마추어와 같아야 한다.
6. 옷이 이 몸에 **아직 맞지 않으면 멈춘다**. Unity MA는 웨이트를 고치지 못한다.

5.2가 ahujasid를 거절하면: 매니페스트의 `dcc-mcp-blender` 핀.

세부: `skills/vrc-dcc/blender.md`（스킬 본문은 영어）.

## 2. Unity 2022.3（MA / NDMF / 메뉴）

목표 에디터: **Unity 2022.3 LTS**（이 아바타 파이프라인에서는 Unity 6 아님）.

**열린 아바타 프로젝트**에서（home / 제어면 창이 아님）:

1. `manifests/tools.json`의 `upm`으로 CoplayDev MCP for Unity를 넣는다.
2. Window → **MCP for Unity** → Start（HTTP `http://localhost:8080/mcp`）.
3. lighfu UnityAgent / EditorEye / 두 번째 Unity MCP는 넣지 않는다.
4. **MA Merge Armature** / Menu Installer / Parameters로 옷을 합친다. 요청 없이 NDMF를 bake하지 않는다.
5. `.prefab` YAML을 손으로 고치지 말고 이름 있는 `vrc_*`를 쓴다. `execute_code` / `execute_csharp`를 발명하지 않는다.
6. MCP에서 `EditorUtility.DisplayDialog`를 호출하지 않는다（에디터가 멈춤）.

공식 Unity 6 MCP / `com.unity.ai.assistant`는 이 2022.3 프로젝트에서 **끔**. TunaSync UnityMCP-VCC나 swax/UnityMCP-VRC를 기본 브리지로 쓰지 마세요.

패키지 URL: [UNITY.md](UNITY.md). PhysBone: `skills/vrc-dcc/references/physbones.md`.

## 3. 사람이 Publish

사람이 VRChat SDK **Build & Publish**를 누른다. 에이전트는 누르지 않고, `upload_vrchat_avatar`를 호출하지 않고, SDK 쿠키를 저장하지 않는다.

## 4. 작업 후

`skills/vrc-review` → `notes/`（`templates/AFTER_ACTION.md`）. 채팅은 기억이 아니다.

# MCP 연결（사람 + 에이전트）

<!-- I18N:START -->
[English](../../ATTACH.md) · [简体中文](../zh-CN/ATTACH.md) · [日本語](../ja/ATTACH.md) · **한국어**
<!-- I18N:END -->

템플릿은 `mcp/*.template`. 생성된 `mcp/local.mcp.json`은 gitignore（절대 경로）. 전체 파이프라인: [WORKFLOW.md](WORKFLOW.md). Unity URL: [UNITY.md](UNITY.md).

## Blender

1. `local.json`에 `blender_exe`를 채운다.
2. blender-mcp 애드온을 켠다. N 패널에서 **Start MCP Server**.
3. 클라이언트: `uvx --python 3.11 blender-mcp==<pin from manifests/tools.json>`.
4. 프로젝트 MCP 또는 `claude --mcp-config mcp/local.mcp.json`으로 붙인다.

blender-mcp 클라이언트는 한 번에 하나.

## Unity 2022.3

**아바타 Unity 프로젝트**를 연다（home / 제어면 창이 아님）.

1. Package Manager → CoplayDev Git URL（`manifests/tools.json`의 `upm`）.
2. Window → MCP for Unity → Start（HTTP `http://localhost:8080/mcp`）.
3. 이름 있는 `vrc_*`: Unity 프로젝트 cwd에서 `scripts/install-vrc-dcc-tools.ps1`. VPM UnityAgent는 넣지 않는다.
4. 그 프로젝트의 `.cursor/mcp.json`에 서버를 복사한다.

공식 Unity MCP / Unity 6 AI Assistant를 이 2022.3 프로젝트에 넣지 않는다.

## 이 머신만

`LOCAL-THIS-PC.md`가 있으면 소유자 전용 경로. 커밋하지 않는다. bootstrap 탐지용 선택 환경 변수: `VRC_DCC_UNITY_HUB`, `VRC_DCC_BLENDER`, `VRC_DCC_UVX`.

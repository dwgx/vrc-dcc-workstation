# AI 사용 안내

<!-- I18N:START -->
[English](../../AI_USAGE_GUIDE.md) · [简体中文](../zh-CN/AI_USAGE_GUIDE.md) · [日本語](../ja/AI_USAGE_GUIDE.md) · **한국어**
<!-- I18N:END -->

clone + bootstrap 이후 에이전트는:

1. [AGENTS.ko.md](../../../AGENTS.ko.md)를 읽는다（핸드셰이크 + MCP）.
2. [WORKFLOW.md](WORKFLOW.md)와 [UNITY.md](UNITY.md)를 읽는다.
3. `local.json`이 있으면 읽고, 없으면 물어 쓴다.
4. `notes/INDEX.md`를 읽는다.
5. 라이브 DCC 작업일 때만 MCP를 붙인다（`mcp/cursor.mcp.json.template` → gitignore된 `mcp/local.mcp.json`）.
6. `skills/vrc-review`로 끝낸다.

## 기본 핀（`scripts/refresh-pins.ps1`로 재확인）

`manifests/tools.json`. GitHub **releases**가 서드파티 VPM 카탈로그보다 우선. 비로그인 GitHub REST가 제한되면 `gh api`.

## Unity 패키지（아바타 프로젝트 창. home / 제어면 아님）

- CoplayDev: `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>`
- UnityAgent: VPM `https://lighfu.github.io/vpm/`, 매니페스트의 `editor-v*`

UnityMCP-VCC라는 실제 저장소는 없다.

## Blender

사람: 3D 뷰 `N` → BlenderMCP → **Start MCP Server**. 클라이언트: `uvx --python 3.11 blender-mcp==<pin>`. 기본 Python이 3.14+이면 `UV_PYTHON_PREFERENCE=only-managed`.

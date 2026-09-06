# AI 사용 안내

<!-- I18N:START -->
[English](../../AI_USAGE_GUIDE.md) · [简体中文](../zh-CN/AI_USAGE_GUIDE.md) · [日本語](../ja/AI_USAGE_GUIDE.md) · **한국어**
<!-- I18N:END -->

clone 이후:

- **설치 / 세팅:** [AGENTS.ko.md](../../../AGENTS.ko.md) 2절 설문, [WORKFLOW.md](WORKFLOW.md) / [UNITY.md](UNITY.md), `local.json` 작성.
- **아바타 / DCC 작업:** [`templates/JOB.md`](../../../templates/JOB.md) — 의도로 분류. 암호 문구 없음. `notes/`가 있으면 설문을 타지 않는다.
- **월드 / Udon:** [`skills/vrc-world/SKILL.md`](../../../skills/vrc-world/SKILL.md) + [`docs/WORLD.md`](../../WORLD.md). 아바타 `handshake.py`는 돌리지 않는다.

그다음:

1. [AGENTS.ko.md](../../../AGENTS.ko.md)를 읽는다（MCP + 정지선）.
2. `notes/CURRENT.md`(문)을 읽는다. gitignore된 `OWNER.md`가 있으면 읽는다. handshake에서 INDEX를 쌓지 않는다.
3. 라이브 DCC 작업일 때만 MCP를 붙인다（`mcp/cursor.mcp.json.template` → gitignore된 `.cursor/mcp.json` / `.mcp.json` / `mcp/local.mcp.json`）.
4. `skills/vrc-review`로 끝낸다.

## 기본 핀（`scripts/refresh-pins.ps1`로 재확인）

`manifests/tools.json`. GitHub **releases**가 서드파티 VPM 카탈로그보다 우선. 비로그인 GitHub REST가 제한되면 `gh api`.

## Unity 패키지（아바타 프로젝트 창. home / 제어면 아님）

- CoplayDev: `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>` 및 이름 있는 `vrc_*`(`com.vrc-dcc.tools`)
- 이 2022.3 개모 파이프라인에 lighfu UnityAgent / `execute_csharp`는 넣지 않는다

TunaSync UnityMCP-VCC나 swax/UnityMCP-VRC를 이 스테이션의 기본 브리지로 쓰지 마세요. 카탈로그 pin은 발견용이지 설치 명령이 아닙니다.

## Blender

사람: 3D 뷰 `N` → BlenderMCP → **Start MCP Server**. 클라이언트: `uvx --python 3.11 blender-mcp==<pin>`. 기본 Python이 3.14+이면 `UV_PYTHON_PREFERENCE=only-managed`.

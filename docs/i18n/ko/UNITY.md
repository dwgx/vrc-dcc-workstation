# Unity 패키지（아바타 프로젝트 창）

<!-- I18N:START -->
[English](../../UNITY.md) · [简体中文](../zh-CN/UNITY.md) · [日本語](../ja/UNITY.md) · **한국어**
<!-- I18N:END -->

이 패키지는 **아바타 Unity 프로젝트 안**에서 넣는다. home / 제어면 창에서는 넣지 않는다. 핀: `manifests/tools.json`.

## CoplayDev — MCP for Unity（기본 에디터 브리지）

Package Manager Git URL:

```
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.1.2
```

그다음: Window → MCP for Unity → Start. Cursor HTTP: `http://localhost:8080/mcp`. 마법사 **Configure MCP Clients**는 **Skip** (Configure Selected / Configure All 금지). AutoRegister 끄기. HTTP는 아바타 프로젝트 `.cursor/mcp.json`만. 사용자 전역 쪽 빨간 점(설정 없음)은 정상이다.

PyPI 짝（stdio / 서버）: `mcpforunityserver==10.1.2`.

Unity 2021.3–6.x에서 동작하지만, 이 스테이션의 아바타는 **2022.3 LTS**를 유지한다.

## lighfu UnityAgent（이 2022.3 아바타 파이프라인에는 **설치하지 않음**）

개모 경로는 CoplayDev HTTP + 이름 있는 `vrc_*`（`com.vrc-dcc.tools`）. UnityAgent / `execute_csharp` / 두 번째 MCP는 넣지 않는다. `manifests/tools.json`의 VPM 핀은 카탈로그 사실일 뿐이다.

## 이 2022.3 아바타 프로젝트에서 금지

- 공식 Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant`（Unity 6）
- TunaSync UnityMCP-VCC 또는 swax/UnityMCP-VRC를 **두 번째 라이브** Editor 브리지로 쓰는 것
- 에이전트가 SDK Build & Publish를 누르는 것

## Worlds / Udon（선택）

옷 합치기의 1순위가 아니다. `skills/vrc-world`, [WORLD.md](../../WORLD.md), `manifests/tools.json`의 `swax-unitymcp-vrc`(카탈로그만). 두 번째 라이브 Unity MCP를 넣지 마세요.

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

그다음: Window → MCP for Unity → Start. Cursor HTTP: `http://localhost:8080/mcp`.

PyPI 짝（stdio / 서버）: `mcpforunityserver==10.1.2`.

Unity 2021.3–6.x에서 동작하지만, 이 스테이션의 아바타는 **2022.3 LTS**를 유지한다.

## lighfu UnityAgent（MA / NDMF 에이전트）

VPM: `https://lighfu.github.io/vpm/`

GitHub **release** 태그와 맞는 `editor-v*`를 설치한다（2026-09-01 확인 예: `editor-v0.15.0`）. 서드파티 VPM 카탈로그는 늦을 수 있다.

## 이 2022.3 아바타 프로젝트에서 금지

- 공식 Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant`（Unity 6）
- 만든 이름 “UnityMCP-VCC”
- 에이전트가 SDK Build & Publish를 누르는 것

## Worlds / Udon（선택）

옷 합치기의 1순위가 아니다. `skills/vrc-dcc/udon.md`와 `manifests/tools.json`의 `swax-unitymcp-vrc`.

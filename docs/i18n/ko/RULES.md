# 규칙

<!-- I18N:START -->
[English](../../RULES.md) · [简体中文](../zh-CN/RULES.md) · [日本語](../ja/RULES.md) · **한국어**
<!-- I18N:END -->

- 사람 검토: PhysBone 한도, 성능 등급, SDK **Build & Publish**.
- 에이전트가 VRChat 업로드를 누르거나 `upload_vrchat_avatar`를 호출하게 하지 않는다.
- 공식 Unity MCP / Unity 6 AI Assistant는 2022.3 아바타 프로젝트에 넣지 않는다.
- blender-mcp는 인스턴스 하나: Cursor **또는** Claude Desktop. 둘 다는 금지.
- 이 서버들을 사용자 전역 MCP에 넣지 않는다.
- 패키지 추가는 아바타 Unity 프로젝트 창에서. home / 제어면 창이 아님.
- 기본 Editor 브리지: CoplayDev unity-mcp + 이름 있는 `vrc_*`(`com.vrc-dcc.tools`). 이 2022.3 개모 파이프라인에 lighfu UnityAgent, TunaSync UnityMCP-VCC, swax/UnityMCP-VRC를 두 번째 라이브 브리지로 넣지 않는다. 핀은 GitHub releases. 늦은 서드파티 VPM 카탈로그는 쓰지 않는다.

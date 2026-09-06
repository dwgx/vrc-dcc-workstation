# 초기화 설문（vrc-dcc-workstation）

AI: `local.json`을 쓰거나 MCP를 붙이기 전에 묻는다. 선택지 + 권장 기본값. 영어 정본: [templates/INIT_QUESTIONNAIRE.md](../../INIT_QUESTIONNAIRE.md). 언어: [docs/i18n/ko/I18N.md](../../../docs/i18n/ko/I18N.md).

## Q0. UI 언어

에이전트는 어떤 언어로 대화하는가?
- [ ] English（`en`）
- [ ] 简体中文（`zh-CN`）
- [ ] 日本語（`ja`）
- [ ] 한국어（`ko`）
- 권장: 지금 채팅 언어에 맞춘다. gitignore된 `local.json`의 `ui_language`에 저장. git 커밋 메시지는 영어.

## Q1. 설치 루트

이 clone은 어디에 있는가?
- 권장: 이 clone 디렉터리 자체.

## Q2. Blender

- [ ] `blender.exe` 경로（목표: **5.2 LTS**）
- [ ] 이번 세션에서 blender-mcp 애드온을 설치/활성화하는가?
- 권장: 경로를 먼저 채운다. 라이브 씬이 필요할 때 사람이 **Start MCP Server**를 누른다.

## Q3. Unity

- [ ] Unity **2022.3 LTS** 에디터 경로
- [ ] 아바타 프로젝트 `.unity` / 폴더（개조 작업이 없으면 비워도 됨）
- 권장: 이 아바타 파이프라인은 2022.3. Unity 6는 쓰지 않는다.

## Q4. 이번 작업의 MCP

- [ ] 없음（문서 / 스킬만）
- [ ] Blender stdio（`manifests/tools.json`의 `blender-mcp` 핀）
- [ ] Unity HTTP（**열린** 프로젝트에서 UPM 한 뒤: `mcpforunityserver` / CoplayDev）
- [ ] 둘 다
- 권장: 라이브 씬을 고치기 전에는 없음. 사용자 전역 MCP에는 절대 넣지 않는다.

## Q5. 선택 vendors

- [ ] CATS Blender Plugin 5.2 fork（Alrauna）
- [ ] gummidot vrchat-agentic-tools 문서
- [ ] felixchaos vrchat-avatar-modding-skill
- 권장: 작업이 필요할 때 clone（`bootstrap.ps1 -Apply -CloneMcp`）.

## Q6. AI 클라이언트

Claude Code / Codex / Cursor / Gemini / Copilot / Grok — 해당 진입 파일만 만든다.

## Q7. 금지（이해했는지 확인）

- [ ] 에이전트는 VRChat Build & Publish를 누르지 않는다
- [ ] 에이전트는 이 2022.3 프로젝트에 공식 Unity 6 MCP를 넣지 않는다
- [ ] 에이전트는 SDK 쿠키를 저장하지 않는다

답을 받은 뒤 짧은 계획을 쓰고 실행한다.

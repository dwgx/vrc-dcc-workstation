# AGENTS.md — vrc-dcc-workstation

모든 AI 에이전트(Claude Code, Codex, Cursor, Gemini CLI, Copilot, Grok)의 공식 진입점입니다. 초기화하거나 스테이션을 다루기 전에 읽으세요.

이 저장소는 **뼈대**입니다. Blender / Unity / VRChat 바이너리와 아바타 프로젝트는 포함하지 않습니다.

<!-- I18N:START -->
[English](AGENTS.md) · [简体中文](AGENTS.zh-CN.md) · [日本語](AGENTS.ja.md) · **한국어**
<!-- I18N:END -->

언어 규칙은 [docs/i18n/ko/I18N.md](docs/i18n/ko/I18N.md). **사용자가 쓰는 언어로 대화**하고, git 커밋 메시지는 영어로 남깁니다.

---

## 0. 무엇인가

휴대용 **VRChat DCC** 워크스테이션: Blender(메시 / 웨이트 / 비젬) + Unity 2022.3(Modular Avatar / NDMF / PhysBone / 메뉴). 에이전트는 **지금 작업에 필요할 때만** Blender MCP 및/또는 Unity MCP를 붙입니다. Claude / Codex / Cursor / Grok **사용자 전역** MCP에 넣지 마세요.

VRChat SDK **Build & Publish는 사람이 누릅니다**. 에이전트는 누르면 안 됩니다.

---

## 1. 초기화 핸드셰이크(물어본 뒤 실행)

사용자가 초기화 / 설치 / 세팅을 요청하면:

### 1단계 — 탐색(읽기 전용)

`README.ko.md`, 이 파일, `docs/i18n/ko/WORKFLOW.md`, `manifests/tools.json`, `manifests/mcp.json`, `docs/i18n/ko/AI_USAGE_GUIDE.md`(없으면 영어)를 읽습니다. OS, `git`, `python`/`uv`, Unity Editor, Blender, `uvx`를 탐지합니다. UI 언어: 대화 → `local.json` `ui_language` → OS UI → `en`.

### 2단계 — 질문(필수)

`templates/i18n/ko/INIT_QUESTIONNAIRE.md`를 사용합니다. 최소한:

0. **UI 언어**(en / zh-CN / ja / ko). 대화가 이미 한국어면 생략 가능. 그래도 `local.json`의 `ui_language`에는 쓴다.
1. **설치 루트**(기본: 이 clone).
2. **Blender** 경로와 버전(목표 **5.2 LTS**).
3. **Unity Editor**(아바타 파이프라인은 **2022.3 LTS**, Unity 6 아님).
4. **아바타 Unity 프로젝트**(개조 작업이 없으면 비워도 됨).
5. **MCP**: 문서만 / Blender / Unity / 둘 다 / 없음.
6. **AI 클라이언트**.
7. 선택 vendors clone 여부(CATS 5.2, gummidot 문서, Codex VRC skill).

다른 사람의 Unity 트리를 추측하지 마세요.

### 3단계 — 계획

쓸 파일(`local.json`, `mcp/local.mcp.json`), clone할 vendors, 사용자 전역에 **넣지 않을** MCP. 확인을 기다립니다.

### 4단계 — 실행(확인 후)

1. `powershell -File scripts/bootstrap.ps1` (드라이런).
2. `-Apply`.
3. 선택 `-CloneMcp`.
4. 핀: `scripts/refresh-pins.ps1` (`gh api` 우선).
5. 스모크: Blender `--version`, uv가 있으면 `uvx --python 3.11 blender-mcp==<pin> --help`.
6. `skills/vrc-review`로 마무리.

### 5단계 — 보고

설치된 것, 건너뛴 것, 남은 위험(업로드는 사람). 한국어 사용자에게는 한국어로.

---

## 2. MCP 정책

- 스킬은 항상 읽기. MCP 프로세스는 지금 씬을 편집할 때만.
- blender-mcp **클라이언트는 한 번에 하나**(Cursor **또는** Claude Desktop).
- Unity: **열린 프로젝트**에서 CoplayDev unity-mcp(HTTP `http://localhost:8080/mcp`), 그리고/또는 VPM lighfu UnityAgent. 공식 Unity 6 MCP / `com.unity.ai.assistant`는 2022.3 아바타 프로젝트에 넣지 마세요.
- 실존하지 않는 이름 UnityMCP-VCC를 만들지 마세요.

---

## 3. 파이프라인

2026-09 절차는 [docs/i18n/ko/WORKFLOW.md](docs/i18n/ko/WORKFLOW.md).

```
Blender  --blender-mcp-->  FBX / VRM
Unity 2022.3  --unity-mcp / UnityAgent-->  MA / 메뉴 / 사람 검토
사람: SDK Build & Publish
```

메시 / 웨이트 / 비젬 / CATS / 본 이름 → Blender.
MA Merge Armature, 메뉴, 파라미터, PhysBone, FaceEmo, lilToon → Unity.
이 바디에 **적응되지 않은 옷**이면 중지하세요. Unity 병합은 웨이트를 고치지 못합니다.

---

## 4. 할 것 / 하지 말 것

**할 것**

- 사람이 N패널에서 **Start MCP Server**를 누른 뒤 Blender를 다룹니다.
- `.prefab` / `.unity` YAML을 손으로 고치지 말고 에디터 API를 우선합니다.
- PhysBone 한도 「수정」, MA 컴포넌트 삭제, 업로드는 먼저 묻습니다.
- 재사용할 사실은 `notes/` (`templates/AFTER_ACTION.md`). 채팅은 기억이 아닙니다.

**하지 말 것**

- Build & Publish, `upload_vrchat_avatar`, SDK 쿠키 저장.
- 2022.3 아바타 프로젝트에 공식 Unity MCP 설치.
- blender-mcp를 GUI 클라이언트 두 개에 동시에 연결.
- Blender/Unity를 네 런타임의 **사용자 전역** MCP에 넣기.
- 세션 jsonl을 현재 Unity 씬으로 착각.

---

## 5. 작업 후

`docs/AGENT_EVOLUTION.md`와 `skills/vrc-review/SKILL.md`. 노트는 `notes/`.

---

## 6. 언어

- **대화**: 사용자와 같음(이 파일은 한국어). gitignore된 `local.json`에 `ui_language`를 남긴다.
- **공개 git**: 영어가 정본.
- **경로**: 절대 경로 또는 설치 루트 상대.

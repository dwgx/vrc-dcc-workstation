# vrc-dcc-workstation

<!-- I18N:START -->
[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **한국어**
<!-- I18N:END -->

휴대용 VRChat DCC 워크스테이션 **뼈대**입니다. **Blender 5.x LTS**(메시 / 웨이트 / 비젬)와 **Unity 2022.3**(Modular Avatar / NDMF / PhysBone / 메뉴)를 MCP로 AI 에이전트가 다룹니다. 월드 / Udon은 별도 스킬(`skills/vrc-world`). 이 저장소는 사설 월드 제품이 아닙니다.

clone한 뒤 [docs/i18n/ko/I18N.md](docs/i18n/ko/I18N.md)로 UI 언어를 정하세요. **설치 / 세팅**일 때만 [AGENTS.ko.md](AGENTS.ko.md) 핸드셰이크. 아바타 작업은 `templates/JOB.md` (의도로 분류, 암호 문구 없음). 대화는 한국어, git 커밋 메시지는 영어입니다. 아바타 본체는 포함하지 않습니다. 에이전트에 건넬 영어 블록: [docs/DROP_ON_AGENT.md](docs/DROP_ON_AGENT.md). 스킬은 **이 clone**에 둡니다(사용자 전역 금지).

작업 후 `skills/vrc-review`로 점수를 매기고 `notes/`에 남깁니다. [docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md).

> **Blender / Unity / VRChat 바이너리와 아바타 프로젝트는 포함하지 않습니다.** [DISCLAIMER.ko.md](DISCLAIMER.ko.md).

---

## 이 저장소에 있는 것

| 경로 | 내용 |
| --- | --- |
| `AGENTS.ko.md` | 에이전트 계약(한국어) |
| `OWNER.example.md` | gitignore된 `OWNER.md` 템플릿 |
| `docs/EVAL.md` | 정적 계약 체크(영어) |
| `docs/i18n/ko/MAINTAIN.md` | 이 작업 사본을 고치는 법 |
| `docs/i18n/ko/WORKFLOW.md` | Blender → Unity → 사람이 Publish (2026-09) |
| `docs/i18n/ko/UNITY.md` | CoplayDev UPM과 이름 있는 `vrc_*` |
| `docs/i18n/ko/I18N.md` | 언어 규칙 |
| `skills/vrc-dcc/` / `skills/vrc-review/` / `skills/vrc-world/` | 개조 플레이북, 쌍축 리뷰, 월드/Udon(초안) |
| `maps/` | 아바타 기억 CLI(`handshake.py` / `gate.py`) + 템플릿. 살아있는 `maps/<id>/` 는 gitignore |
| `unity/vrc-dcc-tools` | 이름 있는 `vrc_*` (`com.vrc-dcc.tools`) |
| `mcp/*.template` | 필요할 때만 MCP. 사용자 전역 금지 |
| `scripts/bootstrap.ps1` | 기본은 드라이런. `-Apply`가 gitignore된 `local.json`을 씀 |

영어 표의 전문은 [README.md](README.md)에 있습니다.

## 빠른 시작

```powershell
git clone https://github.com/dwgx/vrc-dcc-workstation.git
cd vrc-dcc-workstation
powershell -File .\scripts\bootstrap.ps1
powershell -File .\scripts\bootstrap.ps1 -Apply
```

사람이 Blender에서 **Start MCP Server**, 그리고/또는 아바타 Unity 프로젝트에서 **MCP for Unity**를 시작합니다. 에이전트는 그 작업 동안에만 붙습니다. 절차: [docs/i18n/ko/WORKFLOW.md](docs/i18n/ko/WORKFLOW.md).

## 핀 (2026-09-01)

영어 README 표와 같습니다. 정본은 `manifests/tools.json`.

TunaSync UnityMCP-VCC라는 저장소는 있지만, 이 스테이션의 기본 브리지로 **쓰지 마세요**(swax/UnityMCP-VRC도 마찬가지). 아바타 MCP는 CoplayDev + 이름 있는 `vrc_*`.

## 금지

- 에이전트가 VRChat SDK **Build & Publish**를 누르는 것
- 2022.3 아바타 프로젝트에 공식 Unity 6 MCP를 넣는 것
- Blender + Unity MCP를 네 런타임 **사용자 전역** 설정에 넣는 것
- blender-mcp GUI 클라이언트를 동시에 두 개 쓰는 것

## 라이선스

뼈대는 MIT. 업스트림 도구는 각자의 라이선스입니다.

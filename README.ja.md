# vrc-dcc-workstation

<!-- I18N:START -->
[English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [한국어](README.ko.md)
<!-- I18N:END -->

ポータブルな VRChat DCC ワークステーションの**雛形**です。**Blender 5.x LTS**（メッシュ / ウェイト / ヴィセム）と **Unity 2022.3**（Modular Avatar / NDMF / PhysBone / メニュー）を、MCP 経由で AI エージェントが駆動します。ワールド / Udon は別スキル（`skills/vrc-world`）。このリポジトリは私有ワールド製品ではありません。

clone したら [docs/i18n/ja/I18N.md](docs/i18n/ja/I18N.md) で UI 言語を決める。**インストール / セットアップ**のときだけ [AGENTS.ja.md](AGENTS.ja.md) のヒアリング（確認してから `bootstrap.ps1 -Apply`）。アバター作業は [`templates/JOB.md`](templates/JOB.md)（意図で分類。合言葉は作らない）。会話は日本語で。git のコミットメッセージは英語です。アバター本体は同梱しません。エージェントに渡す英語ブロック：[docs/DROP_ON_AGENT.md](docs/DROP_ON_AGENT.md)（[日本語メモ](docs/i18n/ja/DROP_ON_AGENT.md)）。スキルは **この clone** に置く（ユーザーグローバル禁止）。Blender / Unity が無くてもドキュメントだけ使える。

仕事のあと `skills/vrc-review` で採点し、`notes/` に残します。[docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md)。工位の反復（既定アバター無し、身元失敗で停止、ツール許可リスト / JOB lease）：[docs/ITERATION.md](docs/ITERATION.md)（[公開スライス](docs/PR_SLICES.md)）。git に入れないもの：[docs/SOURCES.md](docs/SOURCES.md)。

> **Blender / Unity / VRChat のバイナリも、アバタープロジェクトも同梱しません。** [DISCLAIMER.ja.md](DISCLAIMER.ja.md)。

---

## このリポジトリの内容

| パス | 内容 |
| --- | --- |
| `AGENTS.ja.md` | エージェント契約（日本語）：適用条件、ヒアリング、MCP、ストップライン |
| `OWNER.example.md` | gitignore の `OWNER.md` テンプレート |
| `docs/i18n/ja/MAINTAIN.md` | この作業コピーの直し方 |
| `docs/EVAL.md` | 契約の静的チェック（英語） |
| `docs/BOOTSTRAP.md` | プロジェクト MCP と `local.json`（欠けているアプリは飛ばす） |
| `docs/i18n/ja/WORKFLOW.md` | Blender → Unity → 人が Publish（2026-09） |
| `docs/i18n/ja/UNITY.md` | CoplayDev UPM と指名 `vrc_*` |
| `docs/i18n/ja/I18N.md` | 言語の仕組み |
| `CLAUDE.md` / `GEMINI.md` / `.github/copilot-instructions.md` / `.cursor/rules/` | 各クライアント入口。`AGENTS.md` を指す |
| `templates/i18n/ja/INIT_QUESTIONNAIRE.md` | 日本語の導入アンケート |
| `templates/i18n/ja/JOB.md` | ジョブ初期化（意図。導入アンケートではない） |
| `maps/` | アバター記憶 CLI（`handshake.py` / `gate.py`）+ テンプレ。生きている `maps/<id>/` は gitignore |
| `unity/vrc-dcc-tools` | 指名 `vrc_*`（`com.vrc-dcc.tools`） |
| `skills/vrc-dcc/` / `skills/vrc-review/` / `skills/vrc-world/` | 改変プレイブック、双軸レビュー、ワールド/Udon（草案） |
| `docs/DOMAINS.md` / `docs/WORLD.md` / `docs/PR_SLICES.md` / `docs/ITERATION.md` | アバター vs ワールド vs 工位（英語が正文） |
| `docs/SOURCES.md` | メッシュ / ZIP は git に入れない |
| `docs/DROP_ON_AGENT.md` | 貼り付け用英語ブロック。他リポジトリを乗っ取らない |
| `manifests/` | ピン（PyPI / GitHub / VPM） |
| `mcp/*.template` | 必要時のみ MCP。ユーザーグローバル禁止 |
| `scripts/bootstrap.ps1` | 既定はドライラン。`-Apply` で gitignore の `local.json` を書く |

英語の表の全文は [README.md](README.md) にあります。

## クイックスタート

```powershell
git clone https://github.com/dwgx/vrc-dcc-workstation.git
cd vrc-dcc-workstation
# このフォルダを AI クライアントで開く。docs/DROP_ON_AGENT.md を貼るか「この clone をセットアップ」と言う。
# エージェントは templates/i18n/ja/INIT_QUESTIONNAIRE.md を聞いてから -Apply する。
powershell -File .\scripts\bootstrap.ps1
powershell -File .\scripts\bootstrap.ps1 -Apply
```

人が Blender で **Start MCP Server**、および/または アバター Unity プロジェクトで **MCP for Unity** を開始します。エージェントはその仕事の間だけ接続します。手順：[docs/i18n/ja/WORKFLOW.md](docs/i18n/ja/WORKFLOW.md)。

## ピン（2026-09-01）

英語 README の表と同じです。`manifests/tools.json` が正。

TunaSync UnityMCP-VCC というリポジトリは存在しますが、本ステーションの既定ブリッジに**しない**（swax/UnityMCP-VRC も同様）。アバター MCP は CoplayDev + 指名 `vrc_*`。カタログにあることは第二の橋を入れる指示ではない。

## 禁止

- エージェントが VRChat SDK **Build & Publish** を押すこと
- 2022.3 アバタープロジェクトへ公式 Unity 6 MCP を入れること
- Blender + Unity MCP を四系統の**ユーザーグローバル**設定に入れること
- `skills/` をユーザーグローバルのスキルディレクトリへコピーすること
- blender-mcp の GUI クライアントを同時に 2 つ使うこと

## ライセンス

雛形は MIT。上流ツールはそれぞれのライセンスです。

# vrc-dcc-workstation

<!-- I18N:START -->
[English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [한국어](README.ko.md)
<!-- I18N:END -->

ポータブルな VRChat DCC ワークステーションの**雛形**です。**Blender 5.x LTS**（メッシュ / ウェイト / ヴィセム）と **Unity 2022.3**（Modular Avatar / NDMF / PhysBone / メニュー）を、MCP 経由で AI エージェントが駆動します。

clone したら [docs/I18N.md](docs/I18N.md) で UI 言語を決め、[AGENTS.ja.md](AGENTS.ja.md) のヒアリングを実行してください。会話は日本語で。git のコミットメッセージは英語です。アバター本体は同梱しません。

仕事のあと `skills/vrc-review` で採点し、`notes/` に残します。[docs/AGENT_EVOLUTION.md](docs/AGENT_EVOLUTION.md)。

> **Blender / Unity / VRChat のバイナリも、アバタープロジェクトも同梱しません。** [DISCLAIMER.ja.md](DISCLAIMER.ja.md)。

---

## このリポジトリの内容

| パス | 内容 |
| --- | --- |
| `AGENTS.ja.md` | エージェント契約（日本語） |
| `docs/EVAL.md` | 契約の静的チェック（英語） |
| `docs/i18n/ja/WORKFLOW.md` | Blender → Unity → 人が Publish（2026-09） |
| `docs/i18n/ja/UNITY.md` | CoplayDev UPM と UnityAgent VPM |
| `docs/i18n/ja/I18N.md` | 言語の仕組み |
| `scripts/bootstrap.ps1` | 既定はドライラン。`-Apply` で gitignore の `local.json` を書く |

英語の表の全文は [README.md](README.md) にあります。

## クイックスタート

```powershell
git clone https://github.com/dwgx/vrc-dcc-workstation.git
cd vrc-dcc-workstation
powershell -File .\scripts\bootstrap.ps1
powershell -File .\scripts\bootstrap.ps1 -Apply
```

人が Blender で **Start MCP Server**、および/または アバター Unity プロジェクトで **MCP for Unity** を開始します。エージェントはその仕事の間だけ接続します。手順：[docs/i18n/ja/WORKFLOW.md](docs/i18n/ja/WORKFLOW.md)。

## ピン（2026-09-01）

英語 README の表と同じです。`manifests/tools.json` が正。

**UnityMCP-VCC** という実在リポジトリはありません。

## 禁止

- エージェントが VRChat SDK **Build & Publish** を押すこと
- 2022.3 アバタープロジェクトへ公式 Unity 6 MCP を入れること
- Blender + Unity MCP を四系統の**ユーザーグローバル**設定に入れること
- blender-mcp の GUI クライアントを同時に 2 つ使うこと

## ライセンス

雛形は MIT。上流ツールはそれぞれのライセンスです。

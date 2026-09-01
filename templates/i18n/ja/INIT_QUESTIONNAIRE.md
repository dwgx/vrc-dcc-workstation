# 初期化ヒアリング（vrc-dcc-workstation）

AI：`local.json` を書く・MCP を付ける前に聞く。選択肢 + 推奨デフォルト。英語正文：[templates/INIT_QUESTIONNAIRE.md](../../INIT_QUESTIONNAIRE.md)。言語：[docs/i18n/ja/I18N.md](../../../docs/i18n/ja/I18N.md)。

## Q0. UI 言語

エージェントはどの言語で話すか。
- [ ] English（`en`）
- [ ] 简体中文（`zh-CN`）
- [ ] 日本語（`ja`）
- [ ] 한국어（`ko`）
- 推奨：いまのチャットに合わせる。gitignore の `local.json` に `ui_language` を書く。git のコミットメッセージは英語のまま。

## Q1. インストールルート

この clone はどこか。
- 推奨：この clone ディレクトリそのもの。

## Q2. Blender

- [ ] `blender.exe` のパス（目標：**5.2 LTS**）
- [ ] このセッションで blender-mcp アドオンを入れる / 有効にするか。
- 推奨：パスを先に埋める。ライブシーンが必要になったら人が **Start MCP Server** を押す。

## Q3. Unity

- [ ] Unity **2022.3 LTS** エディタのパス
- [ ] アバタープロジェクトの `.unity` / フォルダ（改変タスクが無ければ空でよい）
- 推奨：このアバター管線は 2022.3。Unity 6 は使わない。

## Q4. この仕事の MCP

- [ ] なし（ドキュメント / スキルのみ）
- [ ] Blender stdio（`manifests/tools.json` の `blender-mcp` ピン）
- [ ] Unity HTTP（**開いている**プロジェクトで UPM したあと：`mcpforunityserver` / CoplayDev）
- [ ] 両方
- 推奨：ライブシーンを触るまでなし。ユーザーグローバル MCP には絶対入れない。

## Q5. 任意の vendors

- [ ] CATS Blender Plugin 5.2 fork（Alrauna）
- [ ] gummidot vrchat-agentic-tools ドキュメント
- [ ] felixchaos vrchat-avatar-modding-skill
- 推奨：仕事が必要になったら clone（`bootstrap.ps1 -Apply -CloneMcp`）。

## Q6. AI クライアント

Claude Code / Codex / Cursor / Gemini / Copilot / Grok — 対応する入口ファイルだけ出す。

## Q7. 禁止（理解したか確認）

- [ ] エージェントは VRChat Build & Publish を押さない
- [ ] エージェントはこの 2022.3 プロジェクトに公式 Unity 6 MCP を入れない
- [ ] エージェントは SDK cookie を保存しない

回答のあと短い計画を出し、それから実行する。

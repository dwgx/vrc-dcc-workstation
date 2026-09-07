# このリポジトリをエージェントに渡す

英語の契約（貼り付け用英語ブロック含む）：[DROP_ON_AGENT.md](../../DROP_ON_AGENT.md)。

clone 後：契約は英語の `AGENTS.md`。**所有者の言語で返答**する。作者マシンのパスをコピーしない。

- この clone の導入 → `templates/i18n/ja/INIT_QUESTIONNAIRE.md` を全部聞いてから `bootstrap.ps1`
- 改模 → `templates/JOB.md`。既定アバターは無い。`gate.py begin` のあと `VRC_DCC_JOB_HOLDER`。命名 `vrc_*` のみ
- 別リポジトリでコードを書く → **vrc-dcc を適用しない**。`skills/` をユーザーグローバルにコピーしない
- Blender / Unity が無くてもドキュメントだけ使える。無い MCP は飛ばす

英語の貼り付け文と振り分け表は正文を使う。

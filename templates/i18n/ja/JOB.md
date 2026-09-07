# ジョブ初期化（このフォルダを渡す）

英語本文：[templates/JOB.md](../../JOB.md)。会話は日本語でよい。契約とテンプレは英語のまま。

これは**ステーション導入**ではない。debugger 工位と同じ分け方：スキル `description` が**誘導プロンプト**（改模/DCC と明らかなら自動適用）。合言葉は作らない。

`INIT_QUESTIONNAIRE.md` は主人が**この clone の導入 / インストール / 初期化**を求めたときだけ。

## 意図で分類（口令表ではない）

| 主人の意図 | 経路 |
|---|---|
| この clone を初期化 / インストール / 構築 | `AGENTS.md` 第 2 節のアンケート |
| この clone を改善 / 拡張（maps CLI、スライス、i18n。Unity 改模ではない） | `docs/MAINTAIN.md` + `maintain-loop.md`；ライブ板は gitignore の `notes/HANDOFF.md` |
| VRChat アバター、服、メニュー、viseme、PhysBone、アバター Blender/Unity DCC | **このファイル** + `dcc-session.md` |
| VRChat **ワールド** / Udon / シーンの改変または監査 | `skills/vrc-world` + `docs/WORLD.md`（アバター handshake ではない） |
| **別の** git ルートの無関係なソフト（アプリ / Web / ライブラリ / 非 VRC ゲーム） | **止める。** 違う木。[DROP_ON_AGENT.md](../../../docs/DROP_ON_AGENT.md) |
| Blender / Unity だが VRChat アバター/ワールド意図がない | **止める。** 範囲外 |
| 不明、かつ probe `station_memory: yes` | ジョブへ。必要なら一句だけ聞く。導入アンケートを出さない |
| 不明、工位が空、主人が「まず組め」 | 導入へ |

固定フレーズをスイッチにしない。言い方は変わる。改模と明らかなら始める。指名を待たない。**既定アバターは無い。** `handshake.py` の `<avatar>` は `notes/CURRENT.md` か所有者の指名。

## この clone で改模するとき

cwd は home、このフォルダ、またはアバター Unity プロジェクトでよい。

1. 先に `session-probe` を quote。`kind: dcc` なら四ランタイム CONTINUE を止める。
2. この clone は**工位**（契約、スキル、`notes/` 記憶）。アバター工程そのものではない。
3. 製品書き込みは `local.json` の `unity_project`、**その工程の窓**で。home はアバター Unity プロジェクトを書かない。工位窓はこの clone だけ。
4. 先に `AGENTS.md` を一度（停止線）。工位 `notes/CURRENT.md`（扉。INDEX ではない）→ 凍結 → **改模は必読** `slice-loop.md` → `python maps/handshake.py <avatar>` → `python maps/gate.py <avatar> begin <review-id>`。指名がなければ `python maps/review.py next <avatar>`。playbook はもう一冊まで。`vrc_audit` が無い：Unity 窓で `scripts/install-vrc-dcc-tools.ps1`。`execute_code` を発明しない。新しい素体：`python maps/init_avatar.py <id>`。handshake 終了コード 2 または閉じた窓 = 止めて新窓。毎ターン読み直さない。
5. 指紋：`notes/`（いつ / なぜ / 何を）+ REVIEW。jsonl は記憶ではない。スナップショットで閉じた窓は続けない。
6. この会話に `unityMCP` があってから Hierarchy を触る。ユーザーグローバル MCP 禁止。SDK Publish は人が押す。

Cursor がすでにアバター Unity フォルダなら、主人は**任意の言い方**でこの一刀を指名すればよい。黙 MCP が約 100 ターン → **新しい会話**。

`templates/avatar-project/` を Unity にコピーする必要はない。

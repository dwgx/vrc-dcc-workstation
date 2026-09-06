# AI 利用ガイド

<!-- I18N:START -->
[English](../../AI_USAGE_GUIDE.md) · [简体中文](../zh-CN/AI_USAGE_GUIDE.md) · **日本語** · [한국어](../ko/AI_USAGE_GUIDE.md)
<!-- I18N:END -->

clone のあと：

- **インストール / セットアップ：** [AGENTS.ja.md](../../../AGENTS.ja.md) 第 2 節のヒアリング、[WORKFLOW.md](WORKFLOW.md) / [UNITY.md](UNITY.md)、`local.json` を書く。
- **アバター / DCC 作業：** [`templates/JOB.md`](../../../templates/JOB.md) — 意図で分類。合言葉は作らない。`notes/` があれば質問票は走らない。
- **ワールド / Udon：** [`skills/vrc-world/SKILL.md`](../../../skills/vrc-world/SKILL.md) + [`docs/WORLD.md`](../../WORLD.md)。アバター `handshake.py` は走らせない。

そのあと：

1. [AGENTS.ja.md](../../../AGENTS.ja.md) を読む（MCP + 停止線）。
2. `notes/CURRENT.md`（扉）を読む。gitignore の `OWNER.md` があれば読む。handshake で INDEX を積まない。
3. ライブ DCC の仕事のときだけ MCP を付ける（`mcp/cursor.mcp.json.template` → gitignore の `.cursor/mcp.json` / `.mcp.json` / `mcp/local.mcp.json`）。
4. `skills/vrc-review` で終わる。

## 既定ピン（`scripts/refresh-pins.ps1` で再確認）

`manifests/tools.json`。GitHub **releases** が第三者 VPM カタログより優先。未認証 GitHub REST がレート制限なら `gh api`。

## Unity パッケージ（アバタープロジェクトの窓。home / 制御プレーンではない）

- CoplayDev：`https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>` と指名 `vrc_*`（`com.vrc-dcc.tools`）
- この 2022.3 改模パイプラインに lighfu UnityAgent / `execute_csharp` は入れない

TunaSync UnityMCP-VCC や swax/UnityMCP-VRC を本ステーションの既定ブリッジにしない。カタログ pin は発見用であり、導入指示ではない。

## Blender

人：3D ビュー `N` → BlenderMCP → **Start MCP Server**。クライアント：`uvx --python 3.11 blender-mcp==<pin>`。既定 Python が 3.14+ なら `UV_PYTHON_PREFERENCE=only-managed`。

# AI 利用ガイド

<!-- I18N:START -->
[English](../../AI_USAGE_GUIDE.md) · [简体中文](../zh-CN/AI_USAGE_GUIDE.md) · **日本語** · [한국어](../ko/AI_USAGE_GUIDE.md)
<!-- I18N:END -->

clone + bootstrap のあと、エージェントは：

1. [AGENTS.ja.md](../../../AGENTS.ja.md) を読む（ヒアリング + MCP）。
2. [WORKFLOW.md](WORKFLOW.md) と [UNITY.md](UNITY.md) を読む。
3. `local.json` があれば読む。無ければ聞いて書く。
4. `notes/INDEX.md` を読む。
5. ライブ DCC の仕事のときだけ MCP を付ける（`mcp/cursor.mcp.json.template` → gitignore の `mcp/local.mcp.json`）。
6. `skills/vrc-review` で終わる。

## 既定ピン（`scripts/refresh-pins.ps1` で再確認）

`manifests/tools.json`。GitHub **releases** が第三者 VPM カタログより優先。未認証 GitHub REST がレート制限なら `gh api`。

## Unity パッケージ（アバタープロジェクトの窓。home / 制御プレーンではない）

- CoplayDev：`https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<pin>`
- UnityAgent：VPM `https://lighfu.github.io/vpm/`、マニフェストの `editor-v*`

UnityMCP-VCC という実在リポジトリはない。

## Blender

人：3D ビュー `N` → BlenderMCP → **Start MCP Server**。クライアント：`uvx --python 3.11 blender-mcp==<pin>`。既定 Python が 3.14+ なら `UV_PYTHON_PREFERENCE=only-managed`。

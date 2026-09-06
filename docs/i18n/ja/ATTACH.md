# MCP 接続（人 + エージェント）

<!-- I18N:START -->
[English](../../ATTACH.md) · [简体中文](../zh-CN/ATTACH.md) · **日本語** · [한국어](../ko/ATTACH.md)
<!-- I18N:END -->

テンプレートは `mcp/*.template`。生成された `mcp/local.mcp.json` は gitignore（絶対パス）。全体：[WORKFLOW.md](WORKFLOW.md)。Unity URL：[UNITY.md](UNITY.md)。

## Blender

1. `local.json` に `blender_exe` を書く。
2. blender-mcp アドオンを有効化。N パネルで **Start MCP Server**。
3. クライアント：`uvx --python 3.11 blender-mcp==<pin from manifests/tools.json>`。
4. プロジェクト MCP または `claude --mcp-config mcp/local.mcp.json` で付ける。

blender-mcp クライアントは同時に 1 つ。

## Unity 2022.3

**アバター Unity プロジェクト**を開く（home / 制御プレーンの窓ではない）。

1. Package Manager → CoplayDev の Git URL（`manifests/tools.json` の `upm`）。
2. Window → MCP for Unity → Start（HTTP `http://localhost:8080/mcp`）。
3. 指名 `vrc_*`：Unity プロジェクト cwd で `scripts/install-vrc-dcc-tools.ps1`。VPM UnityAgent は入れない。
4. そのプロジェクトの `.cursor/mcp.json` にサーバを書く。

公式 Unity MCP / Unity 6 AI Assistant をこの 2022.3 プロジェクトに入れない。

## このマシンだけ

`LOCAL-THIS-PC.md` があれば所有者専用パス。コミットしない。bootstrap の任意環境変数：`VRC_DCC_UNITY_HUB`、`VRC_DCC_BLENDER`、`VRC_DCC_UVX`。

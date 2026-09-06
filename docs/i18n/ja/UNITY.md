# Unity パッケージ（アバタープロジェクトの窓）

<!-- I18N:START -->
[English](../../UNITY.md) · [简体中文](../zh-CN/UNITY.md) · **日本語** · [한국어](../ko/UNITY.md)
<!-- I18N:END -->

**アバター Unity プロジェクトの中**で追加する。home / 制御プレーンの窓からは入れない。ピン：`manifests/tools.json`。

## CoplayDev — MCP for Unity（既定の Editor 橋）

Package Manager の Git URL：

```
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.1.2
```

その後：Window → MCP for Unity → Start。Cursor HTTP：`http://localhost:8080/mcp`。セットアップの **Configure MCP Clients** は **Skip**（Configure Selected / Configure All は押さない）。AutoRegister を切る。HTTP はアバタープロジェクトの `.cursor/mcp.json` のみ。ユーザーグローバル側の赤い欠落表示は想定どおり。

PyPI 側（stdio / サーバ）：`mcpforunityserver==10.1.2`。

Unity 2021.3–6.x で動くが、このステーションのアバターは **2022.3 LTS** のまま。

## lighfu UnityAgent（この 2022.3 アバターパイプラインでは**入れない**）

改模は CoplayDev HTTP + 指名 `vrc_*`（`com.vrc-dcc.tools`）。UnityAgent / `execute_csharp` / 第二 MCP は足さない。`manifests/tools.json` の VPM ピンはカタログ事実のみ。

## この 2022.3 アバタープロジェクトでは禁止

- 公式 Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant`（Unity 6）
- TunaSync UnityMCP-VCC や swax/UnityMCP-VRC を**第二のライブ** Editor ブリッジにすること
- エージェントが SDK Build & Publish を押すこと

## Worlds / Udon（任意）

服合わせの第一選択ではない。`skills/vrc-world`、[WORLD.md](../../WORLD.md)、`manifests/tools.json` の `swax-unitymcp-vrc`（カタログのみ）。第二のライブ Unity MCP を足さない。

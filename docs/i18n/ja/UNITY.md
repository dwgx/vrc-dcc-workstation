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

その後：Window → MCP for Unity → Start。Cursor HTTP：`http://localhost:8080/mcp`。

PyPI 側（stdio / サーバ）：`mcpforunityserver==10.1.2`。

Unity 2021.3–6.x で動くが、このステーションのアバターは **2022.3 LTS** のまま。

## lighfu UnityAgent（MA / NDMF エージェント）

VPM：`https://lighfu.github.io/vpm/`

GitHub **release** タグと一致する `editor-v*` を入れる（2026-09-01 確認例：`editor-v0.15.0`）。第三者 VPM カタログは遅れうる。

## この 2022.3 アバタープロジェクトでは禁止

- 公式 Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant`（Unity 6）
- 作った名前 “UnityMCP-VCC”
- エージェントが SDK Build & Publish を押すこと

## Worlds / Udon（任意）

服合わせの第一選択ではない。`skills/vrc-dcc/udon.md` と `manifests/tools.json` の `swax-unitymcp-vrc`。

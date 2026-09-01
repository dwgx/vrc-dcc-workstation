# Unity packages (avatar project window)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/UNITY.md) · [日本語](i18n/ja/UNITY.md) · [한국어](i18n/ko/UNITY.md)
<!-- I18N:END -->

Add these **inside the avatar Unity project**, not from a home/control-plane window. Pins: `manifests/tools.json`.

## CoplayDev — MCP for Unity (default Editor bridge)

Git URL (Package Manager):

```
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.1.2
```

Then: Window → MCP for Unity → Start. Cursor HTTP: `http://localhost:8080/mcp`.

PyPI companion (stdio/server side): `mcpforunityserver==10.1.2`.

Works on Unity 2021.3–6.x; this station still targets **2022.3 LTS** for VRChat avatars.

## lighfu UnityAgent (MA / NDMF agent)

VPM registry: `https://lighfu.github.io/vpm/`

Install the `editor-v*` package that matches the GitHub **release** tag (example verified 2026-09-01: `editor-v0.15.0`). Third-party VPM catalogs can lag.

## Forbidden in this 2022.3 avatar project

- Official Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant` (Unity 6)
- Invented name “UnityMCP-VCC”
- Agent-driven SDK Build & Publish

## Worlds / Udon (optional)

Not first pick for clothes. See `skills/vrc-dcc/udon.md` and `manifests/tools.json` `swax-unitymcp-vrc`.

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

Then: Window → MCP for Unity → Start. Cursor HTTP: `http://localhost:8080/mcp`. Setup wizard **Configure MCP Clients**: click **Skip** (never Configure Selected / Configure All). Turn AutoRegister off so the next Editor load does not rewrite user-global MCP. Keep HTTP only in the avatar project `.cursor/mcp.json`. A red missing-config dot against user-global Cursor config is expected.

PyPI companion (stdio/server side): `mcpforunityserver==10.1.2`.

Works on Unity 2021.3–6.x; this station still targets **2022.3 LTS** for VRChat avatars.

## lighfu UnityAgent (do **not** install on this 2022.3 avatar pipeline)

改模 path is CoplayDev HTTP + named `vrc_*` (`com.vrc-dcc.tools`). Do not add UnityAgent / `execute_csharp` / a second MCP. The VPM pin in `manifests/tools.json` is a catalog fact only.

## Forbidden in this 2022.3 avatar project

- Official Unity MCP / Unity CLI Pipeline / `com.unity.ai.assistant` (Unity 6)
- TunaSync UnityMCP-VCC or swax/UnityMCP-VRC as a **second live** Editor bridge
- Agent-driven SDK Build & Publish

## Worlds / Udon (optional)

Not first pick for clothes. See `skills/vrc-world`, [WORLD.md](WORLD.md), and `manifests/tools.json` `swax-unitymcp-vrc` (catalog only). Do not add a second live Unity MCP.

## Clothing menus (MA)

Outfit Int + strip Bools + color Int radios. Bit budget, CN shop layout, MaterialSwap vs Setter: [CLOTHING_MENU.md](CLOTHING_MENU.md) · [简体中文](i18n/zh-CN/CLOTHING_MENU.md). Skill pointer: `skills/vrc-dcc/references/clothing-menu.md`.

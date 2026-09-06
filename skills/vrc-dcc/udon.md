# Udon / worlds (secondary)

This station is **avatars-first**. Worlds / Udon: [`skills/vrc-world/SKILL.md`](../vrc-world/SKILL.md) and [`docs/WORLD.md`](../../docs/WORLD.md). Architecture: [`docs/DOMAINS.md`](../../docs/DOMAINS.md).

- Official: [VRChat Creator Docs — Udon](https://creators.vrchat.com/worlds/udon/)
- UdonSharp compiles C# → Udon. Stay on the SDK version **that project** locked.
- Default Editor bridge remains CoplayDev + named `vrc_*` on avatars. Do not add TunaSync UnityMCP-VCC or swax/UnityMCP-VRC as a second live MCP. The `swax-unitymcp-vrc` pin in `manifests/tools.json` is catalog-only.

If the job is avatar-only, do not install Worlds SDK into the avatar project. If the job is a world, do not install Avatar SDK / Modular Avatar to satisfy avatar `vrc_*` assemblies.

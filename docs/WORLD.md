# Worlds pipeline (optional)

<!-- I18N:START -->
**English** — this page is the public stub. Locale siblings are not required until a world job is the default product.
<!-- I18N:END -->

Avatar clothes stay [WORKFLOW.md](WORKFLOW.md). This page is Worlds / Udon only.

```
Unity 2022.3 Worlds SDK  --read-only probe-->  scene / Udon / net inventory
Optional later: owned, reversible edits
Human: SDK Build & Test / Publish
```

## 0. Identity

A world target is **project path + Editor instance + loaded scene GUIDs + descriptor**. A display name or port `8080` is not identity. Two Editors with the same scene name → `AMBIGUOUS_TARGET`, do not pick the first `VRCSceneDescriptor`.

## 1. Read-only first

Load `skills/vrc-world`. Do not open Unity, import, Play, bake, or publish merely to inspect. Disk can prove declared versions and file hashes. It cannot prove unsaved Editor state, compiled Udon, or live multiplayer.

## 2. MCP

Same CoplayDev HTTP rule as avatars: attach **per job**, never user-global. Do not add a second Unity MCP (lighfu, EditorEye, TunaSync UnityMCP-VCC, swax/UnityMCP-VRC as a parallel live bridge) to “cover worlds”. Optional catalog pin `swax-unitymcp-vrc` in `manifests/tools.json` is **not** the default.

Named world tools (`world_probe`, …) are **not implemented** on `com.vrc-dcc.tools` yet. Do not invent `execute_code` / `execute_csharp`.

## 3. Evidence layers (do not collapse)

STATIC_SOURCE → Editor C# compile → UdonSharp compile → ClientSim → local Desktop → PCVR → real multiplayer / late join. ClientSim is not remote deserialization. Human Publish is a separate observation.

## 4. Human publish

Agents must not click VRChat SDK **Build & Publish**, must not call `upload_vrchat_avatar`, and must not store SDK cookies. A future World **Build & Test** grant is not Publish.

Playbook: `skills/vrc-world/SKILL.md`. Architecture: [DOMAINS.md](DOMAINS.md).

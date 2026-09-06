# Evidence layers (any avatar)

Station labels for dumps and REVIEW rows. Inspired by the MIT [VRChatEditorSkill](https://github.com/XiaoboooOvO/VRChatEditorSkill) ladder; rewritten here so we do not vendor that skill. Worlds / Udon: `skills/vrc-world`, not this file.

Never promote one layer into another. `PASS` only for a layer that actually ran. Unrun = `NOT_RUN` / `MCP_REQUIRED` / `BLOCKED` / `STALE`.

| Layer | Proves | Does not prove | Our usual REVIEW `gate` |
|---|---|---|---|
| `STATIC_SOURCE` | YAML / GUID literals on disk | Prefab instance, NDMF output, VRChat | none (routing only) |
| `UNITY_RESOLVED` | Named `vrc_*` / Editor APIs on the **selected** avatar | Built clone, PCVR, multiplayer | `edit` |
| `PROVIDER_PREVIEW` | FaceEmo / MA / inventory preview before later passes | SDK bits, in-world | `edit` |
| `NDMF_BUILT` | Generated menu / params / meshes after NDMF | Client, upload | `edit` (still not `world`) |
| `SDK_BUILD` | SDK window validation / exact bundle | Desktop vs PCVR vs others | `world` needs more |
| `CLIENT_RUNTIME` | Named runtime: Gesture Manager, Play, Build & Test, desktop, PCVR | Other clients; upload | `world` only with `owner_ok` after **upload** if that is the claim |
| `UPLOAD_CONFIRMED` | Human SDK Publish + owner look in VRChat | Later edits | `world` + `owner_ok` |

Inspect / audit / diagnose is read-only. Permission to inspect or even Build & Test is **not** permission to Publish. No Unity MCP in this chat → Editor claims are `MCP_REQUIRED`; do not POST `8080` onto a foreign Editor; do not invent `execute_code`.

Duplicate Hierarchy names, empty `POLICY.unity_root_name`, or two `Nipple_` meshes: refuse (`AMBIGUOUS_*` / `NO_AVATAR_IDENTITY`), do not pick the first. [ITERATION.md](../../../docs/ITERATION.md).

Do not treat `Library/`, `Temp/`, or an old SDK cache as current identity (`AMBIGUOUS_TARGET`).

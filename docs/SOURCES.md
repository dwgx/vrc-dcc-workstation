# What the public skeleton stores (and what it does not)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/SOURCES.md)
<!-- I18N:END -->

The workstation is a **reusable agent contract + playbooks + named Editor tools**. It is not a mesh library and not a private world product.

## Do we need a huge base-model dump in git?

**No.** Live bodies, Booth packs, USB shelves, FBX/VRM, `.unitypackage`, textures, and 15-file world kits stay in the clone-owner overlay / Unity project / `F:` shelf. Public git must stay small enough to clone. Per-body facts live in gitignored `maps/<id>/`.

What *does* belong in git: how to handshake any named avatar, fail-closed identity, MA/bit/GoGo/nipple **rules**, named `vrc_*`, and the iteration loop ([ITERATION.md](ITERATION.md)).

## How web / Astra research enters this tree

1. Research zips and GitHub clones in `Downloads/` are **data**. Do not `git add` the zip, the vendor skill tree, or world ENV-001 assets.
2. Dual-axis review: steal a **rule** only if the next foreign clone would hit it. Rewrite in this station's voice. Cite the primary URL. Do not paste a third-party `SKILL.md` as a second constitution.
3. ChatGPT / Codex web can keep searching. Promotion happens here after a slice, not by accumulating unread archives.
4. Optional vendors (CATS fork, gummidot docs) stay out of the default install. Catalog pins are discovery, not “copy this package into the avatar project”.

## Public sources (steal vs refuse)

| Source | Use | Do not |
|---|---|---|
| This repo + [PR_SLICES.md](PR_SLICES.md) | Canonical loop | Rename to a private world |
| [CoplayDev unity-mcp](https://github.com/CoplayDev/unity-mcp) | Default Editor bridge + named `vrc_*` | Second MCP, wizard Configure All |
| [felixchaos/vrchat-avatar-modding-skill](https://github.com/felixchaos/vrchat-avatar-modding-skill) | Unadapted mesh → Blender stop | Install as a second skill constitution |
| [sentfromspace blog](https://sentfromspace.xyz/blog/claude-vrchat-avatar/) / gummidot fork | INDEX split, dangling params, evidence after Play | `execute_csharp` package, port 14523, WD-ON as a law |
| [XiaoboooOvO/VRChatEditorSkill](https://github.com/XiaoboooOvO/VRChatEditorSkill) (MIT) | Evidence ladder, inspect≠upload, detect toolchain before loading a plugin playbook, menu-first trace | Vendor the zip; make lilycalInventory the default wardrobe (this station’s CN-shop default is Modular Avatar) |
| Official MA / NDMF / VRChat SDK docs | API truth | Agent Build & Publish |
| TunaSync / swax UnityMCP-VRC / lighfu / EditorEye | Catalog / later experiment | Default live bridge on 2022.3 |
| Private world handoff (ENV-001, 源栈织网, 15 PNGs) | Overlay only | Commit IDs, textures, or that product name as this GitHub repo |

Evidence labels we use on dumps: [evidence-layers.md](../skills/vrc-dcc/references/evidence-layers.md).

## Quality bar

A zip in Downloads is not `verified`. `STATIC_SOURCE` ≠ `CLIENT_RUNTIME`. `eval-agent-contract.py` + synthetic CLI tests are `PASS` for the **station**. An avatar is `world` only with `owner_ok` after SDK upload ([review-board.md](../skills/vrc-dcc/references/review-board.md)).

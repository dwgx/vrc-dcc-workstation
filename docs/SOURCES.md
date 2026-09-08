# What the public skeleton stores (and what it does not)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/SOURCES.md)
<!-- I18N:END -->

The workstation is a **reusable agent contract + playbooks + named Editor tools**. It is not a mesh library and not a private world product.

## Do we need a huge base-model dump in git?

**No.** Live bodies, Booth packs, USB shelves, FBX/VRM, `.unitypackage`, textures, and 15-file world kits stay in the clone-owner overlay / Unity project / `F:` shelf. Public git must stay small enough to clone. Per-body facts live in gitignored `maps/<id>/`.

What *does* belong in git: how to handshake any named avatar, fail-closed identity, MA/bit/GoGo/nipple **rules**, named `vrc_*`, the drop-on-agent paste ([DROP_ON_AGENT.md](DROP_ON_AGENT.md)), and the iteration loop ([ITERATION.md](ITERATION.md)).

## How web / Astra research enters this tree

1. Research zips and GitHub clones in `Downloads/` are **data**. Do not `git add` the zip, the vendor skill tree, or world ENV-001 assets.
2. Dual-axis review: steal a **rule** only if the next foreign clone would hit it. Rewrite in this station's voice. Cite the primary URL. Do not paste a third-party `SKILL.md` as a second constitution.
3. ChatGPT / Codex web can keep searching. Promotion happens here after a slice, not by accumulating unread archives.
4. Optional vendors (CATS fork, gummidot docs) stay out of the default install. Catalog pins are discovery, not “copy this package into the avatar project”.

## Public sources (steal vs refuse)

| Source | Use | Do not |
|---|---|---|
| This repo + [PR_SLICES.md](PR_SLICES.md) | Canonical loop | Rename to a private world |
| [CoplayDev unity-mcp](https://github.com/CoplayDev/unity-mcp) | Default Editor bridge + named `vrc_*`. Custom-tool scan, [multi-instance](https://coplaydev.github.io/unity-mcp/guides/multi-instance), [instance routing](https://coplaydev.github.io/unity-mcp/architecture/instance-routing) | Second MCP, wizard Configure All, first-session fallback, deleting `Mcp-Session-Id` to chase MCP 2026-07-28 |
| [felixchaos/vrchat-avatar-modding-skill](https://github.com/felixchaos/vrchat-avatar-modding-skill) | Unadapted mesh → Blender stop | Install as a second skill constitution |
| [sentfromspace blog](https://sentfromspace.xyz/blog/claude-vrchat-avatar/) / gummidot fork | INDEX split, dangling params, evidence after Play | `execute_csharp` package, port 14523, WD-ON as a law |
| [XiaoboooOvO/VRChatEditorSkill](https://github.com/XiaoboooOvO/VRChatEditorSkill) (MIT) | Evidence ladder, inspect≠upload, detect toolchain before loading a plugin playbook, menu-first trace | Vendor the zip; make lilycalInventory the default wardrobe (this station’s CN-shop default is Modular Avatar) |
| Official MA / NDMF / VRChat SDK docs | API truth. [ClientSim](https://creators.vrchat.com/worlds/clientsim/), [Build & Test](https://creators.vrchat.com/worlds/udon/using-build-test/), [late joiners](https://creators.vrchat.com/worlds/udon/networking/late-joiners/), UdonSharp bundled in Worlds SDK | Agent Build & Publish; treating ClientSim as late-join; reinstalling legacy `com.vrchat.udonsharp` |
| [Unity 2022.3 GlobalObjectId](https://docs.unity3d.com/2022.3/Documentation/ScriptReference/GlobalObjectId.html) / Prefab Stage | World identity fields | First `VRCSceneDescriptor`; auto-save to mint a scene GUID |
| [Official Unity MCP](https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.19/manual/integration/unity-mcp-get-started.html) | Know it is Unity 6 and **deprecated** | Install on 2022.3; treat deprecation as a reason to upgrade this avatar pipeline |
| TunaSync / swax UnityMCP-VRC / lighfu / EditorEye | Catalog / later experiment | Default live bridge on 2022.3 |
| Private world handoffs and production assets | Overlay only | Commit private IDs, textures, or use a product name as this GitHub repo |

## Resource libraries and implementation candidates

These sources help discover and develop methods; the catalog is not an install
queue. Use [source-learning.md](../skills/vrc-dcc/references/source-learning.md)
and the optional [research executor brief](../templates/RESEARCH_EXECUTOR.md)
for question-led collection and a usable return to the coordinator.

| Source | Useful input | Check before adoption |
|---|---|---|
| [vrc-mod-guide](https://dwgx.github.io/vrc-mod-guide/) / [source](https://github.com/dwgx/vrc-mod-guide) | World/avatar resource discovery, authored tutorial bodies, video metadata and archive pointers | Inspect the relevant body; historical link/credibility labels do not verify current technical claims. Keep third-party asset rights separate from the catalog. |
| [blender-copilot](https://github.com/dwgx/blender-copilot) | Measurement, mesh checks, UV/material operations, export and avatar-parameter implementation patterns | Trace actual registration, handler and result; distinguish heuristics/templates from measured behavior. Verify target routing and installed versions before a live task. |
| [VRCD documentation entry](https://docs.vrcd.org.cn/books/vrc-YcF/page/vrc) | Chinese community documentation and leads to related World/avatar methods | Record which pages were actually read; verify consequential SDK/tool claims against current original documentation. |

Evidence labels we use on dumps: [evidence-layers.md](../skills/vrc-dcc/references/evidence-layers.md).

## Quality bar

A zip in Downloads is not `verified`. `STATIC_SOURCE` ≠ `CLIENT_RUNTIME`. `eval-agent-contract.py` + synthetic CLI tests are `PASS` for the **station**. An avatar is `world` only with `owner_ok` after SDK upload ([review-board.md](../skills/vrc-dcc/references/review-board.md)).

Chat / Codex export zips are the same rule: extract locally under gitignored `notes/packs/`, rewrite decisions into this tree, do not `git add` the zip or the JSON dump. 2026-09-07 S01 research landed as [FRAMEWORK.md](FRAMEWORK.md) + allowlist `IMPLEMENTED_WORLD`.

# Domain framework (avatar + world)

This is the **station adapter architecture**. World production uses [installed tools](WORLD_PRODUCTION.md) now; S01-b/c are optional adapter development, not production prerequisites. This public repository holds reusable workflows and tools.

A clone-owner **live-test avatar** (any body in `local.json`) is overlay. It is not the public skeleton’s counterpart and not a default character.

ChatGPT research (2026-09-07) is **data**. This page is the rewritten station contract. Unity compile / Editor / VRChat runtime stay `NOT_RUN` until fixtures run.

## Three installable packages (S01-b, not compiled here)

Do **not** one mega-asmdef with `#if`, empty `versionDefines`, or `autoReferenced=false` pretending isolation. Compile conditions are not package dependencies. UdonSharp is **bundled in Worlds SDK**; do not reinstall legacy `com.vrchat.udonsharp`. CoplayDev scans Editor assemblies ([custom tools](https://coplaydev.github.io/unity-mcp/guides/custom-tools)).

| Package | Assembly | Allowed direct deps |
|---|---|---|
| `com.vrc-dcc.core` (proposed) | `VrcDcc.Core.Editor` | Unity 2022.3 Editor + JSON. Identity, POLICY, lease, evidence. **No** VRChat / MA / NDMF / MCP types |
| `com.vrc-dcc.tools` (keep) | `VrcDcc.Tools.Editor` | Core + current MCP + MA + Avatar SDK. Named `vrc_*` only |
| `com.vrc-dcc.worlds` (proposed) | `VrcDcc.Worlds.Editor` | Core + MCP + Worlds/Base/Udon. Named `world_*` only. **No** Avatar SDK / MA / NDMF |

Python Core pieces already in this tree: `maps/lease.py`, `maps/evidence.py`, `maps/allowlist.py`, `maps/policy.py` / `world_policy.py`. Avatar named tools stay on the existing package until S01-b lands compile fixtures (`NOT_RUN` without an Editor).

Do **not** add Avatar SDK or MA to a Worlds project so the avatar adapter compiles. Do **not** add Worlds SDK to an avatar project because a playbook mentioned Udon. Do not ship a meta-package that installs both adapters.

## Two Editors, optional shared HTTP

Prefixes can coexist in **one** Editor’s tool table. That is **not** isolation. Avatar and World jobs **must use different Unity projects and Editors**.

One CoplayDev HTTP server may be reused **only** after routing with an **opaque discovered instance id**. Do not rebuild `Name@hash`. Do not send “first session” / “the remaining Editor”. REST `/api/command` without a target picks the first session ([instance routing](https://coplaydev.github.io/unity-mcp/architecture/instance-routing)). Watch `execute_custom_tool` wrappers — do not open arbitrary dispatch.

`maps/unity_mcp_call.py` keeps `Mcp-Session-Id`. MCP 2026-07-28 dropped protocol sessions; do not delete the current handshake to chase the spec. Official Unity MCP is Unity 6 and **deprecated** — stay off 2022.3.

The proposed station adapter needs two-Editor routing tests before release. Production with an installed provider follows [WORLD_PRODUCTION.md](WORLD_PRODUCTION.md): discover its tools, select the observed instance and read back the project. Station maintenance itself does not operate the product Editor.

## Station CLI

| Domain | Seed | Handshake | Lease |
|---|---|---|---|
| Avatar | `python maps/init_avatar.py <id>` | `python maps/handshake.py <id>` | `python maps/gate.py <id> begin <review-id>` + `VRC_DCC_JOB_HOLDER` |
| World | `python maps/init_world.py <id>` | `python maps/world_handshake.py <id>` | `python maps/world_gate.py <id> begin <review-id>` + same env |

World maps live at gitignored `maps/worlds/<id>/`. Handshake prints `implemented_world_tools: false`. Allowlist: avatar jobs refuse `world_*`; world jobs refuse `vrc_*`; **unimplemented `world_*` refuse even with a matching prefix or POLICY allow list**. This describes `maps/allowlist.py` and the station named-tool client only. Its callable set = implemented ∩ POLICY ∩ domain. Native MCP, provider CLI/SDK and project-owned builders use the production route; this allowlist is not a global capability filter.

## Proposed `world_*` (not callable)

`world_probe` · `world_scene_dump` · `world_udon_inventory`

The proposed S01-c adapter slice covers **`world_probe` only**, after S01-b **and** an authorized Worlds Unity path: versions, identity, scene/descriptor list, Udon summary. No compile / fix / Play / Save. Truncation → `complete=false`. `is_compiling=false` is not compile success. Keep `implemented_world_tools: false` until that acceptance.

World identity = project instance + Editor epoch + **all loaded scenes** (GUID, path, dirty, order, active) + POLICY target scene + descriptor `GlobalObjectId` + Main vs Prefab Stage. Not first `VRCSceneDescriptor`, not port `8080`. Unsaved scene: `guid: null`, do not auto-save. Identity fingerprint ≠ content freshness.

## Evidence (S01-d schema)

`maps/evidence.py`: fingerprint (layer + sha256 + holder + lease id + optional `mutation_revision`), `STALE_MUTATED` / `STALE_LEASE`, owned `PLAN.json` (`apply_allowed`). After Editor mutate: bump `mutation_revision`; recapture that layer (and downstream). Timestamp-washing an old dump is still `STALE_MUTATED`. This is **not** a complete freshness engine: payload is not rehashed against disk; empty lease compare is weak; `apply_allowed` does not match PLAN fingerprints.

Layers include avatar NDMF/SDK plus `UDON_COMPILED` / `CLIENTSIM` / `MULTIPLAYER`. A Python `PASS` is not ClientSim and not in-world. [ClientSim](https://creators.vrchat.com/worlds/clientsim/) ≠ real late-join. [Build & Test](https://creators.vrchat.com/worlds/udon/using-build-test/) ≠ Publish.

## Library v2 (later)

Compatibility is `asset_id × profile_id` plus revisions and evidence refs. Live-test instances stay overlay. No public default body.

## Chat / web research

High-ambiguity decisions go to a **web-research model**. Pack shape: [`templates/CHAT_RESEARCH.md`](../templates/CHAT_RESEARCH.md). Do not commit a filled pack or research zip; copy to gitignored `notes/packs/`.

Human still clicks SDK **Build & Publish** on both domains.

# Base iteration (how this skeleton gets better)

<!-- I18N:START -->
**English** · [简体中文](i18n/zh-CN/ITERATION.md)
<!-- I18N:END -->

This is the **station** loop, not a 改模 mutate and not a Worlds live edit. Public git stays English. Overlay (`OWNER.md`, `local.json`, `maps/<id>/`, dated `notes/`) stays gitignored.

Locked product name: **`vrc-dcc-workstation`**. Do not rename the remote to a private world.

## What “best base” means

A foreign clone and a public PR can 改模 **any** named avatar without inheriting one shop body. Agents follow `templates/JOB.md` → `handshake.py <avatar>` → `gate.py` → named `vrc_*`. Humans click SDK **Build & Publish**.

Live Editor proof (Play / Gesture Manager / PCVR) is still required before saying an avatar is fixed. Offline tests are `PASS`; Unity compile without an Editor is `NOT_RUN`.

## Slice order (Astra + this repo)

Do not skip ahead to World live dumps or a second Unity MCP. Land one slice, test it, then the next.

| Slice | Status | What it is |
|---|---|---|
| **S00-a** | Landed on `9ba91ca` | No default avatar; dump names stay unresolved; `--on-body` refused; overlay out of git |
| **S00-b** | Landed this tree | Fail-closed identity and POLICY (wrong / duplicate / bad schema). No first-`VRCAvatarDescriptor`, no first `Nipple_` / first `GogoLoco` |
| **Drop-on-agent** | Landed this tree | Foreign clone paste block; ask-then-act install; skills stay in-clone so they do not hijack other repos |
| **S00-c** | Landed this tree | Tool allowlist (`vrc_*` only), nonzero MCP errors, matching request id, JOB chat lease |
| **S01-a** | Framework this tree | World maps CLI + proposed `world_*`. Not live dumps |
| **S01-b** | Later | Core / Avatar / World assemblies. Do not add Avatar SDK to a Worlds project to compile |
| **S01-c** | Later | Read-only `world_*` after an authorized Worlds Unity path |
| **S01-d** | Schema this tree | Evidence fingerprints / STALE / owned plan-apply (`maps/evidence.py`) |
| Library v2 | Later | `on_avatars` per asset × profile. Live-test overlay id stays clone-local |

Details: [PR_SLICES.md](PR_SLICES.md). Architecture: [FRAMEWORK.md](FRAMEWORK.md). This clone’s live next-action (uncommitted, overlay, expansion lanes) is gitignored `notes/HANDOFF.md` — not this file. High-ambiguity research: [CHAT_RESEARCH.md](../templates/CHAT_RESEARCH.md).

## How to land a slice

1. Quote `session-probe`. Station cwd → patch **this clone** only. Do not write the avatar Unity project. Do not POST `8080` from station.
2. Failing fixture first when the change is code (`tests/`). Synthetic maps only (`example-*`), never `maps/<live-id>/`.
3. Fix. Keep overlay gitignored. Do not teach `handshake.py` a shop character.
4. `python scripts/eval-agent-contract.py` and the regression runner. Record expected vs actual exit per command.
5. Dual-axis `skills/vrc-review`. Offline `PASS` ≠ `world` fitted.
6. Commit only when the owner asks. English message. Do not force-push unless they asked to wash history again.

## Absorb research (no mesh dumps)

Do **not** commit FBX, VRM, unitypackages, world texture kits, or a vendor skill zip. [SOURCES.md](SOURCES.md): web/Astra may keep searching; this tree only takes **rewritten rules** that the next foreign clone will hit. Cite the primary URL. lilycalInventory / FaceEmo playbooks load only when that provider is on *this* avatar — they are not the station default (MA CN-shop menus are).

Promote a lesson the same way as [slice-loop.md](../skills/vrc-dcc/references/slice-loop.md): this body → `maps/<avatar>/`; next body → a playbook; control loop → templates + `unity/vrc-dcc-tools`.

## Identity contract (S00-b)

- `POLICY.json` `avatar` must equal the maps folder id. `unity_root_name` must be a real Hierarchy name, not `AVATAR_ID`.
- Named `vrc_*` resolve **one** root with that name. Zero → `NO_AVATAR`. Two+ → `AMBIGUOUS_AVATAR`. Empty name → `NO_AVATAR_IDENTITY` (never “first descriptor in the scene”).
- Nipple / GoGo: POLICY path if set (missing path is not a search). Else unique candidate. Zero → `not_applicable` (do not invent weights). Two+ → `ambiguous` (do not take the first).
- Overlay may set `nipple_smr_path` / `gogo_root_path` for one body. Public templates leave them empty.

## Tool fence and JOB lease (S00-c)

- Allowlist: named `vrc_*` only. POLICY `allow_mcp_tools` is still a `vrc_*` subset (generic mutators stay refused). `world_*`, CoplayDev generic mutators, `execute_code` / `execute_csharp`, and any tool whose name contains upload/publish as a path segment are refused **before** HTTP.
- `unity_mcp_call.py` treats JSON-RPC `error` and MCP `isError` as failure. Notifications without a matching request id are not a result. Library `call_tool()` needs a live JOB lease (tests use `skip_lease=True` against fake MCP).
- `gate.py begin` writes `JOB.json` `lease` under a file lock. Set `VRC_DCC_JOB_HOLDER` (required). A second holder while the lease is live gets `LEASE_HELD`. `reset` needs the holder or `--force`. Expiry (default 3600s, POLICY `job_lease_ttl_sec`) lets a new named holder take it.

## Never on the public base

Secrets, SDK cookies, live `maps/<id>/`, USB `catalog.json`, a private fusion dump as the default example, agent Build & Publish, Unity 6 MCP on 2022.3, a second live Editor bridge.

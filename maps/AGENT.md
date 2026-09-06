# Agent playbook — index library

Load on 改模 after `maps/<avatar>/STATE.md` if that file exists. Do not re-read this mid-job. Caps: `skills/vrc-dcc/references/token-budget.md`. Layout: [README.md](README.md).

```
cd maps
python query.py <avatar> SPS
python query.py <avatar> --confirmed
python query.py <avatar> --id plugin.pcs
python booth.py --search Fallen Servant
python booth.py https://booth.pm/ja/items/123456
python query.py library 毛衣
python query.py library --fusion
python library/scan.py
python library/ingest.py
powershell ../scripts/graphs-ready.ps1
```

`--kaguya` on library queries is **overlay-only**: it filters notes.json key `kaguya` for one historical profile. It is not a generic on-this-avatar API. Missing key is unset, not `never`. Other bodies: `query.py <avatar>`.

## What this is

A **living catalog** of the current avatar: folders, plugins, outfits, menus, params, plus **remarks that survive a regen**.

| Layer | Truth |
|---|---|
| `maps/<avatar>/graph.json` | Structure (can be replaced) |
| `maps/<avatar>/notes.json` | Remarks. Key = node `id`. Never wipe |
| `maps/<avatar>/MAP.md` | Generated. Agents Read this |
| `maps/<avatar>/REVIEW.json` | Proven vs new. `python review.py render <avatar>` |
| `maps/<avatar>/REVIEW.md` | Generated |
| `maps/library/catalog.json` | USB shelf structure (scan; gitignored) |
| `maps/library/notes.json` | Shelf remarks. Never wipe. Gitignored |
| `maps/library/LIBRARY.md` | Generated. Gitignored |
| `notes/*.md` | Dated evidence (often gitignored). CURRENT wins on conflict |
| `.codegraph/` on this clone | Station **Python**. [GRAPHS.md](GRAPHS.md) |
| Avatar Unity `.codegraph/` | **C#** in Packages + avatar scripts. Unity window only. Not 轮盘 |

**确定 / confirmed** = Owner lock or verified Edit dump. **observed** = lead. Chat jsonl is not an index.

## Session order (fits 改模 init)

Same as `dcc-session.md`. Find / Booth / dispatch do **not** re-read AGENTS or SKILL.

1. Quote `session-probe` once if the Cursor rule requires it.
2. `AGENTS.md` once → `OWNER.md` → `notes/CURRENT.md` (door) → `python maps/handshake.py <avatar>` → `slice-loop.md`. Do **not** dump `MAP.md` + `LIBRARY.md` on handshake. Snapshot only if CURRENT names it.
3. This file **once** when the slice is find / refresh / Booth / harvest. `MAP.md` / `LIBRARY.md` on demand (`query.py`), not every init.
4. On-demand skill for the named slice only (`clothing-menu.md`, …).

Home cwd must not write the avatar Unity project (`local.json` `unity_project`). Index files live in **this clone**.

## Find (parent, no subagent)

**On the avatar** (already wired): `query.py <avatar>` / `MAP.md`.

**On the USB shelf** (owned, not necessarily installed): `query.py library` / `LIBRARY.md`. Same Booth id in two collections collapses to **one** node; extra copies stay in `copies`.

1. Adding clothes: `query.py library --fusion` then the named words.
2. Already on this avatar: `query.py <avatar>` (not a library `--on-body` flag).
3. Miss: `notes/INDEX.md` then one skill reference (`clothing-menu.md`, `params-256.md`).
4. Still miss: YAML/grep in the **avatar window**, or named `vrc_*`.
5. Web / Booth **last**. Do not spawn a subagent to grep MAP.md or walk the USB root.
6. C# / “how does ObjectToggle work” / station Python internals: `codegraph_explore` with `projectPath` ([GRAPHS.md](GRAPHS.md)). Do not grep `Packages/` first. No avatar C# index yet → Unity window inits it, or Read the named `.cs`.

## Continue / update the index

After a **material** Hierarchy / menu / bit change (same slice as the Unity edit):

1. Avatar Unity window. `unityMCP` already discovered **once**.
2. Named `vrc_*` if the package is imported; else Unity cwd `install-vrc-dcc-tools.ps1` then Reload. Do not `python maps/audit.py`. Handshake: `python maps/handshake.py <avatar>` then `python maps/gate.py <avatar> begin <id>`.
3. `python refresh.py <avatar> --from-dump that.txt` — merges **keeping ids**, then render. Do not wipe `notes.json`.
4. `--mark-missing` only on a **live** dump, never on an empty file.
5. New lock: patch `notes.json` `"status":"confirmed"` + `source`.
6. Patch `maps/<avatar>/STATE.md` when / why / what.

JSON dumps with a `nodes` array also merge by `id`.

## Continue / update the USB catalog

After packs land on the shelf (`local.json` `unityvrchat_library`; Owner confirmed ingest). **Not** the same stack as a Unity mutate.

1. `python maps/library/scan.py` — catalog regen, `notes.json` kept.
2. Overlay historical profile only: patch `maps/library/notes.json` key `kaguya` + `map_id`. Do not treat that key as installed-on-whatever-avatar-is-selected.
3. Optional `item.json` in the pack folder on the shelf. Scan fills empty keys only.

## Booth / web

No official public Booth search API we ship. Do **not** add BoothMate, Apify, or mass scrapers.

Order:

0. `query.py library <name>` — if it is already on the USB, stop. Do not WebSearch an owned pack.
1. Owner pasted `https://booth.pm/.../items/123456` → `python booth.py <url>` **or** one `WebFetch`. Extract: item id, title, shop, price, listed body, MA vs VRCFury vs prefab-only.
2. No URL → `python booth.py --search <name>` prints the one `WebSearch` query (`site:booth.pm … VRChat`). Then one Fetch / `booth.py` of the best item page.
3. Body fit: shop scale charts between named bases are **not** a fusion body unless the owner said so. Record in `notes.json` as observed until the owner keeps the mesh in Edit.
4. Write `source`: `booth.pm/items/<id>`. Do not git avatar zips. Do not buy. Do not download paid files.

If Fetch / `booth.py` is blocked: tell the owner the URL and stop. Do not invent a listing.

## Dispatch (subagents)

Parent stays on the **named slice**. Subagents are for **parallel harvest**, not Unity mutation.

| Job | Who | Writes |
|---|---|---|
| query.py / Read MAP or LIBRARY | **parent** | none |
| USB scan | **parent** `python maps/library/scan.py` | catalog.json + LIBRARY.md (notes kept) |
| Unity dump / MA / menus | **parent** in the avatar Unity window + `unityMCP` | avatar tree + then `refresh.py` |
| Survey `Assets/` names | `Task` `explore` cwd avatar, read-only | none (return a list) |
| Booth / docs harvest | one `Task` `generalPurpose` | optional `notes.json` patch only, this clone |
| C# / station Python “how does X work” | parent `codegraph_explore` + `projectPath` | none |

Envelope every subagent must get (copy):

```
Station: <this clone>
Find: python maps/query.py <avatar> <words>
Shelf: python maps/query.py library <words>
Booth: python maps/booth.py --search <name>  then one item URL
Do not write the avatar Unity project from a home cwd.
Do not SDK Publish. Do not user-global MCP.
Return: bullet hits + any notes.json id patches (confirmed vs observed).
Do not re-read AGENTS.md / SKILL.md. One WebSearch max if Booth.
```

One subagent per question. Cap: if the parent already has ~100 silent turns, **new chat** instead of dispatch. Do **not** spawn Bugbot / security-review on a Unity tree that is not git. Empty Task stubs are a miss — do the harvest in the parent or skip.

## Do not

- `codegraph init` on `Assets/*.unity` expecting 轮盘
- `codegraph init` the avatar Unity tree from a home cwd
- `codegraph upgrade` unless the owner named it this turn
- Wipe `notes.json` when replacing `graph.json`
- WebSearch before query.py (avatar **or** library)
- Continue chats that `CURRENT.md` marks closed
- Mix “refresh index” with “install three Booth packs” in one stack
- Treat `wear_fusion` as fitted
- `refresh.py --mark-missing` without a real Editor dump

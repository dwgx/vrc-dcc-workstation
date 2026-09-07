# USB shelf catalog

Same contract as `maps/<avatar>`: **catalog** (structure) + **notes** (remarks) + **LIBRARY.md** (what you Read). Scan output is gitignored on the public skeleton.

| File | Who writes it |
|---|---|
| `catalog.json` | `scan.py` only. Folder names + Booth ids. Gitignored. |
| `notes.json` | Humans/agents. Key = node `id`. **Never wipe on scan.** Gitignored. |
| `seed.json` | Known installed/removed facts. Scan fills *empty* keys only. Gitignored. Copy from `seed.example.json`. |
| `LIBRARY.md` | `render.py` only. Do not hand-edit. Gitignored. |
| `item.json` | Optional sidecar **inside a pack folder on the shelf**. Scan copies empty keys into notes. |

USB path: `local.json` `unityvrchat_library` (or env `UNITYVRCHAT_LIBRARY`). Index stays in **this clone** so agents do not walk the shelf every chat.

```
python maps/query.py library 毛衣
python maps/query.py library --fusion
python maps/library/scan.py
python maps/library/ingest.py
```

`--on-body` is not a generic API and exits 2. Use `python maps/query.py <avatar>` for the named body. `--kaguya` is an overlay-only legacy filter for the local `notes.json` key `kaguya`; a missing key displays as `unset` and does not match `never`.

Humans: open generated `LIBRARY.md`. Agents: same file, or `query.py library`. C# / scan.py internals: [GRAPHS.md](../GRAPHS.md), not this catalog.

Do not rearrange the shelf by body. Do not Ultra. Do not unpack unitypackages on the shelf. Skip huge dump folders the owner marked unindexed.

World / map kits (Owner-named top-level `世界\\`): `地图` (complete worlds), `建筑家具` (house/furniture), `功能` (world Udon). Do not file those under `通用散件\\道具` (avatar-held items only). Query: `python maps/query.py library Modern`.
## World and Avatar asset identity

World entries use `world.booth.<id>` or `world.pack.<name>`. Avatar entries keep
their existing IDs. Equal Booth IDs or pack names across domains remain separate;
same-domain duplicates retain the `copies` behavior. On the next scan, legacy
World notes migrate only when the old catalog establishes their domain. Ambiguous
old notes and existing destination notes are preserved without guessing ownership.

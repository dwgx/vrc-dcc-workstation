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

`--kaguya` filters overlay `notes.json` key `kaguya` (one historical profile). Not a generic on-body API. Missing key is unset, not confirmed `never`.

Humans: open generated `LIBRARY.md`. Agents: same file, or `query.py library`. C# / scan.py internals: [GRAPHS.md](../GRAPHS.md), not this catalog.

Do not rearrange the shelf by body. Do not Ultra. Do not unpack unitypackages on the shelf. Skip huge dump folders the owner marked unindexed.

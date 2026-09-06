# Three graphs (C# vs clothes vs USB)

Codegraph, `maps/<avatar>`, and `maps/library` are **not substitutes**. Pick one.

| Question | Graph | How |
|---|---|---|
| Clothes / 轮盘 / bits / “is this on the live body” | **Avatar map** | `python maps/query.py <avatar>` / `maps/<avatar>/MAP.md` |
| “Do we already own this Booth pack” | **USB shelf** | `python maps/query.py library` / generated `library/LIBRARY.md` |
| “How does Modular Avatar ObjectToggle work in C#” | **Codegraph** | MCP `codegraph_explore` with **`projectPath`** |
| Station Python (`scan.py` / `query.py`) | **Codegraph** on this clone | `projectPath` = this clone |
| YAML / Hierarchy / `.unity` | none of these | named `vrc_*` in the avatar Unity window |

Tree-sitter languages include **C# and Python** (30+). Codegraph does **not** parse MA menus, PhysBone, or prefabs. A Unity scene init will index `*.cs` only and skip 轮盘.

## Handshake (new agent)

If `session-probe` exists it already prints `graphs:`, `codegraph_station:`, `codegraph_avatar:` (some hosts also print a product-specific alias), `codegraph_mcp:`. Do not rediscover.

```
powershell -File .\scripts\graphs-ready.ps1
```

Always pass **`projectPath`**. A home / maps cwd has no default `.codegraph`.

No index at `projectPath` → fail-open to rg / Read. Do not invent symbols.

## This clone (station Python)

Optional local index: `.codegraph/` (gitignored except `.gitignore`). `codegraph.json` in this repo excludes generated MAP/catalog JSON.

After station Python edits: `codegraph sync` in the clone (or wait for the daemon).

## Avatar Unity C# index (Unity window only)

Copy [`templates/avatar-codegraph.json`](../templates/avatar-codegraph.json) to `<unity-project>/codegraph.json`, then from **that** Unity cwd:

```
powershell -File <station>/scripts/install-avatar-codegraph.ps1
```

The template **keeps** Modular Avatar, NDMF, VRCFury (not `com.vrcfury.temp`), FaceEmo, and avatar `*.cs`. It **excludes** VRChat SDK, Unity packages, lilToon, Av3Emulator, Gesture Manager, AV3Manager, VRSuya, and VRCFury temp — those C# trees drown ObjectToggle. Prefabs and `.unity` are not tree-sitter languages; they are skipped anyway.

If a new VPM folder appears under `Packages/`, add it to the template **exclude** unless it is MA / NDMF / VRCFury / FaceEmo.

Home / station cwd: that script **exits 2**. Missing avatar index → Read the named `.cs` or paste for a Unity window.

## MCP vs CLI

If the owner opted into user-global Cursor MCP `codegraph serve --mcp`, expect **one** listed tool: `codegraph_explore`. Extra CLI verbs (`query`, `callers`, …) stay in the shell. Do **not** dump extra MCP tools into user-global config unless the owner names that change.

Do not edit `~\.cursor\mcp.json` from a public-skeleton script.

## Do not

- `codegraph init` on `Assets/*.unity` expecting 衣服/轮盘
- Init a whole Unity tree without the exclude template
- `codegraph init` on the user-profile home folder
- `codegraph index` an avatar Unity tree from a home cwd (writes the product tree)
- Walk the USB shelf or grep MAP.md because codegraph missed a dress
- Mix “init codegraph” with “install a Booth pack” in one stack
- `codegraph upgrade` unless the owner named it this turn

# VRC DCC maps — architecture

Not `notes/INDEX.md` (dated archive). Not the Unity tree.

This folder is the **per-project memory**. Skills stay reusable. A second avatar gets its own folder; it does not inherit another body's Clothes Int or freeze stops.

## Four layers

```
station clone (vrc-dcc)
├── skills/            reusable playbooks (clothing-menu, gogoloco, perf-vram, …)
├── notes/             dated evidence + CURRENT.md door (often gitignored)
└── maps/
    ├── README.md      this file
    ├── INDEX.md       commands
    ├── AGENT.md       find / Booth / USB
    ├── library/       owned packs (all avatars)
    ├── templates/     seed a new avatar
    └── <avatar>/      one product’s live map + board + snapshot (gitignored)
```

| Layer | What | Who writes | Evolve how |
|---|---|---|---|
| **Skills** | How to 改模 (any body) | Patch playbook when a lesson will hit the *next* avatar | skill file + optional parent `sync-skills.ps1` |
| **notes/** | When / why / what (dated) | `templates/AFTER_ACTION.md` | Stay; fold triples into a playbook |
| **maps/library** | USB shelf | `scan.py` / `ingest.py` | Shared; catalog gitignored |
| **maps/\<avatar\>** | *This* body: structure, locks, proven vs new | Same slice as the Unity write | `refresh.py` + `review.py` |

Unity product tree (`local.json` `unity_project`) is **not** memory. Home cwd does not write the avatar Unity project.

## Per-avatar folder

| File | Role |
|---|---|
| `STATE.md` | Live snapshot (when / why / what). |
| `graph.json` | Structure. Regenerated. |
| `notes.json` | Remarks keyed by node `id`. **Never wipe.** |
| `MAP.md` | Generated. **确定** vs observed. |
| `REVIEW.json` | Proven vs new + `lessons[]`. |
| `JOB.json` | One-chat sku quota. `python maps/gate.py <avatar>`. |
| `POLICY.json` | Per-body overlay: root name, body_token, disable_mcp_tools, leftover_needles. Copied to Unity `Assets/VrcDcc/POLICY.json`. |
| `conflicts.json` | Owner lane winners (AFK / loco / audio). Agent asks if a lane is missing. |
| `REVIEW.md` | Generated. |
| `audit-dump.txt` etc. | Editor pastes. |

`python maps/init_avatar.py <id>` copies `templates/` here. Id = lowercase folder (`my-avatar`, `rurune`). Live folders stay gitignored on the public skeleton. There is no default character.

## Iterate (one slice)

```
Owner names a slice
    → python maps/handshake.py <avatar>
    → python maps/gate.py <avatar> begin <id>
    → one playbook (slice-loop.md)
    → Unity Edit named vrc_* (product window) or station docs only
    → one dump
    → python maps/refresh.py <avatar> --from-dump …
    → upsert REVIEW.json (never world without Owner)
    → python maps/review.py lint <avatar> && python maps/review.py render <avatar>
    → STATE.md when / why / what
    → vrc-review
    → reusable? copy lesson into skills/references
    → control-loop change? dual-axis then patch templates / unity/vrc-dcc-tools
```

`python maps/review.py next <avatar>` is the queue, not a write permit. Freeze file (if CURRENT names one) wins on Unity writes.

## Learn / upgrade (three promotions)

| Hit | Store here | Promote when |
|---|---|---|
| This body only | `maps/<avatar>/` notes + REVIEW row + POLICY overlay | Never into a generic playbook as a default |
| Will happen on the next body | `REVIEW.json` `lessons[]` then **skills** | Same week, English playbook |
| Control loop (handshake, gate, named tools, POLICY schema) | `maps/templates/` + `unity/vrc-dcc-tools` | Dual-axis, then patch |
| Chat jsonl | nowhere | — |

Station evolution: `docs/AGENT_EVOLUTION.md`. Dual-axis: `vrc-review`. Human SDK Publish.

## First product is overlay, not the type

Live door: gitignored `notes/CURRENT.md`. Live map: gitignored `maps/<avatar>/`. Commands: [INDEX.md](INDEX.md). New product: [templates/AVATAR.md](templates/AVATAR.md).

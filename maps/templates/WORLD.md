# New world map (overlay)

Not station install. Not a Unity copy. Not this public repo’s product.

Live folders stay gitignored (`maps/worlds/<id>/`). Do not commit scene dumps, textures, or platform world IDs.

Suggested overlay files (create when the owner names a world id):

| File | Role |
|---|---|
| `PROFILE.json` | Stable product id, Unity path fingerprint, platform (e.g. PC Desktop + PCVR) |
| `STATE.md` | When / why / what |
| `JOB.json` | Current writer lease, slice and persistent mutation revision |
| `REVIEW.json` | Proven vs new; `world` rows need human in-world evidence |
| `POLICY.json` | Optional station named-tool client policy and project identity |

Station framework (no Unity): `python maps/init_world.py <id>` then `world_handshake.py` / `world_gate.py`. Named `world_*` stay proposed; `world_probe` is not callable until S01-c. Identity is project + Editor + all loaded scenes + descriptor, not port `8080`.

Existing project task records and tools can be used directly; this overlay is optional. Production: [WORLD_PRODUCTION.md](../../docs/WORLD_PRODUCTION.md). Same-holder `begin` can continue to another slice; `reset` releases the lease while preserving mutation history.

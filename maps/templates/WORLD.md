# New world map (overlay)

Not station install. Not a Unity copy. Not this public repo’s product.

Live folders stay gitignored (`maps/worlds/<id>/`). Do not commit scene dumps, textures, or platform world IDs.

Suggested overlay files (create when the owner names a world id):

| File | Role |
|---|---|
| `PROFILE.json` | Stable product id, Unity path fingerprint, platform (e.g. PC Desktop + PCVR) |
| `STATE.md` | When / why / what |
| `JOB.json` | One-chat operation quota |
| `REVIEW.json` | Proven vs new; `world` rows need human in-world evidence |
| `POLICY.json` | Disable raw execute tools; directory bounds |

Station framework (no Unity): `python maps/init_world.py <id>` then `world_handshake.py` / `world_gate.py`. Named `world_*` stay proposed.

Station skills: `skills/vrc-world`. Pipeline: `docs/WORLD.md`.

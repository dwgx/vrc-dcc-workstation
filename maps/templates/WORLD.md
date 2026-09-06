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

Do not copy an avatar `POLICY.json` onto a world. Do not copy one world’s freeze onto another.

Station skills: `skills/vrc-world`. Pipeline: `docs/WORLD.md`.

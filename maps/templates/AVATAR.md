# New avatar map

Not station install. Not a Unity copy.

```
cd maps
python init_avatar.py <id>
```

`<id>` = lowercase, `[a-z][a-z0-9-]*` (example: `my-avatar`, `rurune`). Creates `maps/<id>/` from this folder. Refuses if the directory already exists. There is no default character.

Then:

1. `python handshake.py <id>`
2. Point `local.json` `unity_project` at that Unity tree (or a new Cursor window on it).
3. First dump → `python refresh.py <id> --from-dump …` (keep `notes.json`).
4. Door: either a line in gitignored `notes/CURRENT.md`, or this avatar’s own freeze note. Do not copy another body's POLICY/freeze onto a new body.
5. `python review.py next <id>`.
6. Unity window: `scripts/install-vrc-dcc-tools.ps1` (copies POLICY into `Assets/VrcDcc/POLICY.json`).

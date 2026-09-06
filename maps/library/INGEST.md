# Ingest (new packs)

Index lives in this clone. The USB path is the shelf. **This script does not move files.**

1. Drop the zip / folder in `local.json` `unityvrchat_stage` (create if missing). Name it with the Booth id if you have one: `6071820-example.zip`.
2. `python maps/library/ingest.py` — prints a **proposed** bucket. The owner names the collection folder.
3. Owner says yes. Then move into `unityvrchat_library\...`. Do not invent a new top-level bucket.
4. `python maps/library/scan.py` — catalog grows; `notes.json` stays.
5. After the mesh is on the live avatar in Edit: patch `notes.json` on-body status + `map_id`.

Do not Ultra. Do not unpack `.unitypackage` on the shelf unless the owner asked.

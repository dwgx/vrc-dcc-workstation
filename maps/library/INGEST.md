# Ingest (new packs)

Index lives in this clone. The USB path is the shelf. **This script does not move files.**

1. Drop the zip / folder in `local.json` `unityvrchat_stage` (create if missing). Name it with the Booth id if you have one: `6071820-example.zip`.
2. `python maps/library/ingest.py` — prints a **proposed** bucket. The owner names the collection folder.
3. Owner says yes. Then move into `unityvrchat_library\...`. Do not invent a new top-level bucket **except** the Owner-named world root `世界\`.
4. Avatar clothes/hair/gizmos: `角色\` / `通用散件\` / `工具与插件\`. VRChat **world** maps, house kits, furniture packs, world Udon: `世界\地图\` / `世界\建筑家具\` / `世界\功能\`. Do not drop world kits into `通用散件\道具`.
5. `python maps/library/scan.py` — catalog grows; `notes.json` stays.
6. After the mesh is on the live avatar in Edit: patch `notes.json` on-body status + `map_id`.

Do not Ultra. Do not unpack `.unitypackage` on the shelf unless the owner asked.

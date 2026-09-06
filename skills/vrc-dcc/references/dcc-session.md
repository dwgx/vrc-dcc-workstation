# DCC session (load on an avatar job)

A VRChat / avatar / DCC ask **is** job init. Classify by intent (`templates/JOB.md`); do not require a passphrase. Quote `session-probe` once if it exists. `kind: dcc` → stop estate CONTINUE. `kind: home` / station cwd → patch this clone only; do **not** write the avatar Unity project (`local.json` `unity_project`); paste for a Unity window.

**Door:** `notes/CURRENT.md` (not INDEX). Closed chats listed there. Do not mine jsonl. Snapshot / freeze / MAP / REVIEW conflict rules live in CURRENT. An HTTP dump without Set/Save is **not** a visual change. Mid-job: [slice-loop.md](slice-loop.md) — `python maps/handshake.py <avatar>` then `python maps/gate.py <avatar> begin <id>` then **one** named `vrc_*`. Queue is not a write permit.

## If cwd is home or this station clone

1. Quote `session-probe`. Stop estate CONTINUE. Do **not** run `INIT_QUESTIONNAIRE`. `station_memory: yes` means this clone already has DCC job notes. `graphs:` / `codegraph_station` / `codegraph_mcp` is the three-graph handshake. Missing avatar C# index → do not `codegraph init` from home; Read named `.cs` or paste for a Unity window (`scripts/install-avatar-codegraph.ps1`).
2. Station docs/skills may be patched in this clone. Do **not** write the avatar Unity project.
3. Give a Unity **new chat** paste from `notes/CURRENT.md`. Do not continue chats CURRENT marks closed.

## If cwd is the avatar Unity project

1. **Do not** read CORE / WORKFLOW as this job. Quote `session-probe` once. Read **`notes/CURRENT.md`**, then freeze if CURRENT says so, then **one** playbook for the named slice, plus `token-budget.md`. Do not load INDEX + MAP + intake + three clothing files on handshake.
2. VPM packages are in `Packages/vpm-manifest.json`. A short UPM `manifest.json` does not mean “not a VRC project”.
3. If the user already named a 改模 task, do not `AskQuestion` “what job next”.
4. Speak with **menu and Hierarchy names the owner sees**. Map jargon to a visible radial item, or say it is **not in the current menu**.
5. **One slice.** Do not mix 改模 with a second product. Finish or defer the first named job before starting the second. Two gizmos on the same playable: [plugin-conflicts.md](plugin-conflicts.md) + `maps/<avatar>/conflicts.json`. Do not silently pick a winner. After the first Unity mutation cluster, a **second named product** (new Booth SKU, new plugin, shelf harvest, station maps architecture) is a **new chat** — one paragraph in the owner locale, do not absorb. One Booth SKU until the Owner looks in Edit. If they paste N IDs, install **0** until they name one. `wear_fusion` is not fitted; `NEED_PREFAB_PATH` / no POLICY `body_token` match → do not Instantiate.
6. After a material Unity change: patch `maps/<avatar>/STATE.md` **in that same slice**. Upsert `maps/<avatar>/REVIEW.json`. `python maps/review.py lint <avatar> && python maps/review.py render <avatar>`. `python maps/render_map.py <avatar>`. Do not wipe `notes.json`.
7. Hard stops in CURRENT are **stops**. Delta mx < 0.01 → wait. Do not “upgrade” the playbook in the same turn as the failed cutter.

## MCP before mutation

1. `GetDynamicTools` for `unityMCP` **once** per chat (or after Reload; Reload ≠ fresh `tools/list` — quit the client if names stay stale). If `unityMCP` is missing or Unity MCP is **off**: station-only / paste. Do **not** POST `8080` and do **not** Start CoplayDev on a foreign Editor. If `vrc_audit` is **not** in the catalog **and** this cwd is the **avatar** Unity project the owner opened for that job: `powershell -File <station>/scripts/install-vrc-dcc-tools.ps1`, wait compile, MCP Start (Skip), Reload. Do **not** invent `execute_code`. YAML/grep is analysis only. Do not run `python maps/audit.py`.
2. CoplayDev wizard: **Skip**. Never Configure Selected / Configure All. Turn **AutoRegister** off. HTTP stays in the avatar project `.cursor/mcp.json`. A red “Missing MCPForUnity Config” against user-global `~\.cursor\mcp.json` is expected.
3. Never dump Blender/Unity MCP into user-global client config.
4. One Editor dump: named `vrc_audit` / `vrc_ma_wiring`. Emergency paste only if named tools missing.

## Do not invent

- Rest-OFF meshes (ObjectToggle closed) are not “missing pieces”.
- Do not add body blendshapes to clothing clips the vendor clip did not drive.
- Body identity first. Generic vendor “All” prefabs are wrong until matched. Shop scale charts between named bases are **between those bases**, not a fusion body unless the owner said so.
- Default-off gizmos need a MenuItem. Path is project-specific (MAP / OWNER). Marshmallow vs holes: [marshmallow-erp.md](marshmallow-erp.md). Loco: [gogoloco.md](gogoloco.md). Upload test: [upload-test.md](upload-test.md).
- Follow this project's folders (`Assets/功能`, `Assets/衣服`, `菜单/功能` when that is how the shop laid them out). Per-body “do not delete / do not MoveAsset” locks live in `OWNER.md` and `POLICY.json`.
- Do not delete bake-only prefabs just because scene `GetDependencies` is empty (`motchiri Prefab_FX` is the usual miss). After unused-sweep, the next SDK fail is often Instantiate-null, not PhysBone cyclic.
- After the Owner **hand-deletes** an outfit: dump leftover MenuItems, ObjectToggle `targetObject=0`, and MA Parameter names on the menu host **before** other edits (`editor-reports.md`).
- Inverted nipple ShapeChanger belongs on bra **MenuItems**, never on rest-OFF bra mesh. Covering tops get **non-inverted** `Nipple_Small=100`. Never outfit Int. `Nipple_On=0` is not “no nipple geo”. If Nipple_* max |delta| < 0.01, **stop Unity** — do not VertexFilterByShape those keys the same turn.
- New outfit: Merge + turn it on in **Edit** and let the owner look. Do not wire extra synced bits until they say the mesh is keepable.

## Done means Edit proof or Play — not SPS bake

Clothes / leftover menus: prove in **Edit** (ObjectToggle on/off, read the blendshapes the playbook names). Do not sit in Play waiting for VRCFury **haptic** bake (SPS/PCS). That hang is not a clothes failure.

A dual-axis self-score without Edit blendshape proof **or** Gesture Manager stays **observed**. Do not tell the owner “修好了” on YAML or Editor API writes alone.

If you do enter Play and it is not idle within ~60s: `manage_editor` exit Play, report `blocked`, continue in Edit. Never save the scene in Play.

## MCP budget

Past windows that burned schema refetch + Play haptic wait + stacking: [token-budget.md](token-budget.md). One dump: [editor-reports.md](editor-reports.md). Bits: [params-256.md](params-256.md). Do not continue chats CURRENT marks closed.

After **~100 silent** assistant turns: stop the job, tell the owner to **new chat**. Do not keep stacking. Do not dispatch Bugbot / security-review on a Unity tree that **is not git**.

If you edit station `skills/` playbooks, patch this clone. If a parent workstation syncs a second copy, patch both the same slice.

Human clicks SDK Publish. 显存 / VRAM / Poor rank: [perf-vram.md](perf-vram.md) — unload unused packs, do not Crunch remaining 2K.

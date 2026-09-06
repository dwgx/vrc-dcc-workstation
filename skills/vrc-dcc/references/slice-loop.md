# slice-loop (one 改模 slice)

Load this instead of re-reading the whole skill stack mid-job. Default path is **named `vrc_*` tools**, not invented `execute_code`. No second MCP. No EditorEye. No SDK Publish.

Same numbered map as the estate: probe → doors → one mission → record → promote. This file is the DCC slice, not a second constitution.

## 0. Where you are

| Cwd | Allowed |
|---|---|
| Avatar Unity project | Named `vrc_*` (after package import) or emergency paste. Mutate that one REVIEW row. |
| This station clone | `handshake.py`, `gate.py`, playbooks, `unity/vrc-dcc-tools` source. Do not write the avatar Unity project. |
| Home (user profile) | Same as station docs. **Do not** `python maps/audit.py`. |

`<avatar>` is the maps folder id (`python maps/init_avatar.py <id>` for a new body). Do not copy one body's POLICY/freeze onto another.

If `vrc_audit` is missing, Unity window: `scripts/install-vrc-dcc-tools.ps1` then Reload. If you authored new C# this turn, the slice missed the named tool.

## 1. Handshake (Python, no Unity write)

```
python maps/handshake.py <avatar>
python maps/gate.py <avatar> begin <review-id>
python maps/gate.py <avatar> consume-sku <booth-id>
```

`handshake.py` is the product `session-probe`: POLICY, JOB, REVIEW next, map/state paths. Exit 2 = stop. A chat id CURRENT marks closed = stop, new window. Do not re-init inside that jsonl.

`begin` must be an **existing** REVIEW row id. `sku_quota` comes from POLICY. Second `begin` with a different id = new chat. `consume-sku` / `mutated` without `begin` = exit 2. After first mutate: `python maps/gate.py <avatar> mutated`. New chat: `python maps/gate.py <avatar> reset`.

`review.py next` is the queue, not a write permit. Freeze in `notes/CURRENT.md` (if this clone names one) wins on Unity writes.

Chat in the owner's locale (zh-CN / ja / en / ko). Tracked files stay English. Public git is optional.

## 2. Handshake Unity once

`GetDynamicTools` for `unityMCP` **once** (or after Reload). CoplayDev wizard: **Skip**. Port 8080 LISTEN is not enough: the Editor websocket must `register_tools` (`VrcDccMcpBoot` starts HTTP then `Bridge.StartAsync`; do not call `StartLocalHttpServer` if the port is already up). **Reload Window is not a fresh `tools/list`** — if the IDE catalog still lacks `vrc_audit` after Reload, full-quit the client. If Unity MCP is **off**, or 8080 belongs to another product: **do not POST 8080**, do not Start CoplayDev from station. Call **one** tool:

| Need | Tool |
|---|---|
| Bits / missOT / nipples / GoGo | `vrc_audit` |
| MergeAnimator | `vrc_ma_wiring` |
| Clothes toggle | `vrc_ot_inventory` |
| Dead FX param | `vrc_dangling_params` (menu+PB+contact+driver+clip; skip `VF*`) |
| Broken clip path | `vrc_clip_missing_paths` (Transform, blendshape, material slot) |
| Before Instantiate | `vrc_prefab_identity` (`prefabPath` required) |
| Accessory pose | `vrc_pose_bounds` (BakeMesh, not AABB) |
| After Owner hand-delete | `vrc_leftover_menu` |

Empty `avatar=` uses `POLICY.json` `unity_root_name` only. Missing or duplicate Hierarchy names refuse (`NO_AVATAR_IDENTITY` / `NO_AVATAR` / `AMBIGUOUS_AVATAR`). Never the first `VRCAvatarDescriptor` in the scene. `vrc_audit.fitted` is always false. Nipple / GoGo fields carry `nippleIdentity` / `gogoIdentity` (`ok` / `not_applicable` / `ambiguous` / `missing_policy_path`); weights stay `-1` unless `ok`. `isSynced=0` is not fitted. `NEED_PREFAB_PATH` / `NO_BODY_PREFAB` / `WRIST_NOT_GRIP` / `ZERO_WEIGHT_CONSTRAINT` / `LEFTOVER_MENU` = do not hang the SKU.

POLICY `disable_mcp_tools` (default `execute_code`) is applied when the package loads. Do not re-enable it to skip identity.

## 3. Mutate one row

Only the REVIEW id from `begin`. One Booth SKU until the Owner looks in Edit. Pose BoneProxy in Edit.

Unadapted mesh / weights → stop, Blender. Never MA Merge as a fit.

## 4. Close the slice

Upsert `REVIEW.json` + `STATE.md`. `python maps/review.py lint <avatar> && python maps/review.py render <avatar>`. `world` only with `owner_ok`. ~100 silent → new chat.

Fail a named check → add a **C# refuse** or POLICY overlay, then promote:

| Hit | Store |
|---|---|
| This body only | `maps/<avatar>/` (POLICY, REVIEW, notes.json) |
| Next body will hit it | `skills/vrc-dcc/references/` + `sync-skills.ps1` |
| Control loop | station templates + `unity/vrc-dcc-tools` (dual-axis first) |

Not a 12th CURRENT bullet.

## Never

Second Unity MCP, EditorEye `:50050`, sentfromspace `:14523` / `UnityMcpBridge` / `execute_csharp`, lighfu 400-tool soup, Unity 6 MCP on 2022.3, agent SDK Publish, `maps/audit.py` HTTP, screenshot loops, Play-wait on VRCFury haptic for clothes.

v2 (not this package until Owner names it): Gesture Manager toggle-diff, NDMF baked-clone `AvatarTypeChecker`, one screenshot cap.

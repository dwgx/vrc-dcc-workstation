# Editor reports (named `vrc_*`)

Default path after `com.vrc-dcc.tools`: **named MCP tools**, not `execute_code`. Loop: [slice-loop.md](slice-loop.md). Handshake: `python maps/handshake.py <avatar>`.

| Need | Tool |
|---|---|
| Bits / missOT / nipples / GoGo | `vrc_audit` (`{}` or POLICY root) |
| MergeAnimator | `vrc_ma_wiring` |
| Clothes toggle | `vrc_ot_inventory` |
| Dead FX param | `vrc_dangling_params` |
| Broken clip path | `vrc_clip_missing_paths` |
| Before Instantiate | `vrc_prefab_identity` (`prefabPath` required) |
| Accessory pose | `vrc_pose_bounds` (BakeMesh) |
| After Owner hand-delete | `vrc_leftover_menu` |

If `vrc_audit` is missing **in an avatar Unity chat that already has unityMCP**: Unity cwd `scripts/install-vrc-dcc-tools.ps1`, compile, MCP Start (**Skip**), Cursor Reload. Reload ≠ fresh `tools/list` (quit client if still stale). Do **not** `python maps/audit.py`. If Unity MCP is off: do not Start it from station.

Do not invent a new C# dump. Named tools missing + MCP off = YAML/grep analysis only.

Public loops (EditorEye screenshots; GM toggle-diff needs Play): `notes/2026-09-03-editoreye-and-verify-loops.md`. Do not install sentfromspace/gummidot/EditorEye packages.

Do not screenshot. Do not enter Play to dump these. `fitted` is always false. Owner Edit look still required.

`GameObject.Find` misses rest-OFF parents. Named tools walk `GetComponentsInChildren(..., true)`.

## Bit table

**Two** costs: source `CalcTotalCost` (Edit) and last Play bake. Flag MenuItem `isSynced` vs MA `localOnly` (`WantSynced |=`). Flag `VF*` on the **source** asset (Play-save leak). Details: [params-256.md](params-256.md).

Face = mesh `Body`. Source Menu.asset empty. NDMF mip: set `streamingMipmaps` in Edit; do not click 自动修复 / 进行测试构建. Intake: [avatar-intake.md](avatar-intake.md).

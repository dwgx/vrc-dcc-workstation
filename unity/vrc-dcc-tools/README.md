# VRC DCC Tools (`com.vrc-dcc.tools`)

Named 改模 MCP tools on the **existing** CoplayDev HTTP server (`http://127.0.0.1:8080/mcp`). Not a second MCP. Not EditorEye. Not `execute_code` as the default path.

Requires Unity **2022.3**, CoplayDev `com.coplaydev.unity-mcp`, Modular Avatar, VRChat Avatars SDK. `AutoRegister=true`, Group `core`.

Works for **any** avatar Unity project that imports this package. Per-body overlay: `maps/<avatar>/POLICY.json` copied to `Assets/VrcDcc/POLICY.json`.

## Install (Unity window only)

Home / station cwd must **not** write the Unity tree. In the **avatar Unity** Cursor chat:

```
powershell -File <station>/scripts/install-vrc-dcc-tools.ps1
```

That adds `file:` `com.vrc-dcc.tools` to `Packages/manifest.json`, copies POLICY, and a `.cursor/rules` pointer. Then:

1. Wait Unity compile
2. Window → MCP for Unity → Start (wizard: **Skip**)
3. Cursor Reload Window
4. `GetDynamicTools` once — expect `vrc_audit` … `vrc_leftover_menu`

Manual fallback: Package Manager → Add package from disk → `unity/vrc-dcc-tools/package.json`.

## Tools

| Tool | Refuses / dumps |
|---|---|
| `vrc_audit` | bits, missOT, nipples, GoGo Base. `fitted=false`. ErrorResponse `PLAYING` / `NO_DESC` / `MISS_OT` |
| `vrc_ma_wiring` | every MergeAnimator enabled/mode/layer |
| `vrc_ot_inventory` | ObjectToggle miss via `AvatarObjectReference.Get` |
| `vrc_dangling_params` | FX params with no menu/PB/contact driver (skip `VF*`) |
| `vrc_clip_missing_paths` | source FX bindings whose Transform is missing |
| `vrc_prefab_identity` | `NEED_PREFAB_PATH` without `prefabPath`; `NO_BODY_PREFAB` if token mismatch |
| `vrc_pose_bounds` | BakeMesh vs Humanoid bone; wrist `dRH≈0`; weight-0 ParentConstraint |
| `vrc_leftover_menu` | MenuItem / OT / MA param after Owner hand-delete (`POLICY leftover_needles`) |

None of these Instantiate. POLICY `disable_mcp_tools` (default `execute_code`, `execute_csharp`) is applied on Editor load via CoplayDev `EditorPrefs`. Station `unity_mcp_call.py` also refuse-closes non-`vrc_*` names.

## Python (station, no Unity write)

```
python maps/handshake.py <avatar>
python maps/gate.py <avatar> begin <review-id>
python maps/gate.py <avatar> consume-sku <booth-id>
python maps/gate.py <avatar> reset
```

Playbook: `skills/vrc-dcc/references/slice-loop.md`.

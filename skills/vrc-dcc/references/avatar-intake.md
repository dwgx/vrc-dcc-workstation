# Avatar intake (every 改模 chat)

This skeleton has **no default character**. Per-body facts live in gitignored `maps/<avatar>/` and `OWNER.md`. [docs/AVATAR_PROFILE.md](../../../docs/AVATAR_PROFILE.md).

Do not hunt jsonl. Do not WebSearch the live prefab. One `vrc_audit` dump beats a screenshot. Do not assume another clone’s shop name, `Body_b`, or `paryi_Loco`. Detect what is **on this prefab** (MA vs FaceEmo vs lilycalInventory vs vendor FX) before loading a plugin playbook. Empty `unityMCP` → `MCP_REQUIRED`, not invented `execute_code`.

Worked example (not a handshake default): [examples/composite-avatar.md](examples/composite-avatar.md).

## 0. Name the body

1. Id from the Owner, or `notes/CURRENT.md` Products table.
2. No folder: `python maps/init_avatar.py <id>`.
3. `python maps/handshake.py <id>` (required; CLIs do not default a product).
4. Read `maps/<id>/STATE.md` + MAP **确定**. Snapshot wins over older notes. Freeze note wins on Unity writes.

## 1. Eat this prefab (dump, then table)

Fill or refresh the overlay. Typical questions:

| Ask | How |
|---|---|
| Face vs body meshes | Which SMR has visemes / eye look vs breast / clothes shrink |
| Armature | Shop names (`Shoulder_L`) vs Unity Humanoid (`LeftShoulder`) |
| Menu source | Empty `Menu.asset` + MA installers vs FaceEmo vs vendor FX |
| Face params | Shop Int vs GoGo `VRCEmote` — do not wire them together |
| Default loco | Shop Base vs GoGo Replace vs Append+passthrough ([gogoloco.md](gogoloco.md)) |
| Plugins on/off | On-avatar vs prefab-only in Assets (disabled children still bake `isSynced`) |
| Folders | Often `Assets/功能` + `Assets/衣服` + `菜单/` on CN shops — confirm MAP |

Vendor “limit / none” prefabs are often **parameter SKUs**, not other meshes. Do not swap them to “simplify”.

## 2. NDMF console

Yellow **Mip Streaming** + 自动修复 = textures with mipmaps but `streamingMipmaps=false`. **Agent enables `TextureImporter.streamingMipmaps` in Edit** (batch `StartAssetEditing`). Do not ask the owner to click 自动修复. Do not click **进行测试构建** (same VF haptic hang as Play). Human SDK Build.

## 3. First dump

`visemeMesh, faceParam, FaceEmoCount, menuAssetControls, installersOn, gogoBaseMode, leftover synced MenuItems, mipStreamingLeft`

Then clothes/bits in [editor-reports.md](editor-reports.md).

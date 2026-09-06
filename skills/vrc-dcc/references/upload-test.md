# In-world upload test (Editor cannot prove this)

Play may hang on VRCFury **haptic** bake. Clothes/乳首 stay Edit-proven. **Human** SDK Build & Publish. Agent never clicks it. VRAM bands: [perf-vram.md](perf-vram.md). Checklist items that are body-specific come from `maps/<avatar>/` + `conflicts.json`.

## Before you click Build

- Do not delete bake-only prefabs the MAP says to keep (motchiri `Prefab_FX` is the usual miss).
- If SDK says parameters overflow, **do not** re-enable a third Base (ABT). Cut a gizmo or set a size Int `localOnly`.
- Default walk / AFK / ABT: [gogoloco.md](gogoloco.md) + `conflicts.json`. Do not Base **Replace** unless the Owner named that cost.

## What only VRChat can prove (order)

1. SDK Build succeeds. If it fails, stop and send the console line.
2. **Walk / crouch / prone** = MAP default. Menu Bool `VrcDcc/GoGoLoco` (if wired) switches GoGo. Do **not** use GoGo’s own `Go/Locomotion` Toggle as the shop↔GoGo switch.
3. **Headset AFK** = the `conflicts.json` `afk` winner, not a guessed GoGo lie-down.
4. Clothes Int 0 = shop original restored (mesh **and** FX Bools). Added outfits hide shop original. Shoes-in-ground + multi-region clip = Blender / [clothing-convert.md](clothing-convert.md).
5. Marshmallow jiggle if installed. Blend vs body rest: MAP.
6. SPS/PCS on Head/Chest/Hips if installed. Audio: 3-source cap.
7. Remote: synced colors the Owner wanted others to see.

Play in Editor: if VF haptic >60s, **exit Play, do not save**.

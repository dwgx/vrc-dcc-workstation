# GoGoLoco vs shop loco

Default walk is **whatever this avatar’s MAP / OWNER / `conflicts.json` names** — not a baked-in shop character. Many JP bodies ship a custom Base (`paryi_Loco` is one pattern). A **menu toggle** may switch to GoGo loco. GoGo **actions / emotes** still need Action **Replace** if the shop Action already uses `VRCEmote`. ABT and AFK winners: [plugin-conflicts.md](plugin-conflicts.md). One fusion worked example: [examples/composite-avatar.md](examples/composite-avatar.md).

Booth [franada 3290806](https://franada.booth.pm/items/3290806) 1.8.6. Synced **16/256** (`VRCEmote` + `Go/Float`; Beyond +1). Shop↔GoGo walk switch is **`VrcDcc/GoGoLoco`** (local Bool). Do **not** reuse **`Go/Locomotion`** (GoGo Stand Idle / disable-walk). Do **not** add a new **synced** bit (bake is often already tight).

## Failed approach (do not repeat)

MA `GetComponentsInChildren<ModularAvatarMergeAnimator>(true)` does **not** skip `enabled=false`. **Disabled Base + `mergeAnimatorMode=Replace` still wipes the descriptor shop loco** (example: `paryi_Loco`) and installs `GoLocoBaseWD`. Same class of bug as disabled MenuItems still baking `isSynced`.

`animator=null` while mode stays Replace: `MergeSingle` returns early, **RemoveLayerPass still clears Base**.

Inactive GameObjects are included (`includeInactive: true`). ObjectToggle of a MergeAnimator GO does not un-bake it.

## Action: still Replace, never Append

`GoLocoActionWD` L0 `Action&AFK` defaultWeight **1**. After MA **Append**, those layers sit **behind** shop Action layer 0. GoGo `VRCAnimatorLayerControl` talks to **layer index 0** (now the shop). Result: GoGo buttons **smash** shop Action **and** GoGo clips do not play.

MA **Replace** on Action wipes shop Action then installs `GoLocoActionWD`. Cost: shop Action emotes/AFK are gone in-world. **Often accepted.** Gesture/FX stay shop.

## Base: Append + WD-OFF passthrough (not Replace, not “disable”)

`VRCAnimatorLayerControl.BlendableLayer` has Action / FX / Gesture / Additive only. **It cannot drive the Base playable.** Dual loco is not “layer weight 0 on paryi layer 0”.

Working pattern (any body that keeps shop walk as default):

1. Descriptor Base stays **shop loco**.
2. GoGo Base MergeAnimator **enabled**, **`Append`** `GoLocoBaseWD` (never Replace).
3. NDMF plugin `vrc-dcc.loco-switch` (after MA): if Base has both GoGo marker state `Avatar 3D Thumbnail` **and** shop marker `standing`, insert `VrcDccShopPassthrough` (empty clip, **Write Defaults OFF**) as that GoGo Locomotion layer’s default. Drive a **new local** param **`VrcDcc/GoGoLoco`** (Bool, `localOnly`, not a synced bit). `≤ 0.5` stays passthrough → shop walk/crouch/prone. `> 0.5` goes to **`VrcDccClearGoLoco`** (0.05s hold clip so ParameterDriver is not skipped in one Update) then child SM **`( 3-4 pt )` / `( 5+ pt )`**. **Not** Thumbnail (SDK idle). **Not** Local/Remote `go_Idle`. **Not `Go/Locomotion`**: inside `Stand Motion` that param **Greater 0.5 → Stand Idle** (GoGo’s own disable-walk). Reusing it for the shop↔GoGo switch makes ON = no walk clip. On the avatar instance, set GoGo All MA Parameters **`Go/Locomotion` saved=false** (vendor prefab stays saved=1; do not ApplyPrefab). Passthrough and clear each `VRCAvatarParameterDriver` local Set **`Go/Locomotion=0`**. Editor `Animator.Update` does not run that driver. If TrackingType/AFK gates miss, last resort is still `( 3-4 pt )` for the local player — never a Loc-only catch-all onto Thumbnail. Desktop `TrackingType` &lt; 3 also enters `( 3-4 pt )`.
4. Same gate on GoGo **Poses** (Additive). **Do not** add AnyState on nested child SMs (that fight stole walk).
5. Optional component `VrcDccLocoSwitch` documents param names. Auto-detect works without it if both markers exist.
6. If Thumbnail exists **without** `standing`, plugin **skips** (Replace still on → passthrough would T-pose).

| Base MergeAnimator | Walk the player gets | Do not |
|---|---|---|
| **Append** + loco-switch passthrough | Shop default; `VrcDcc/GoGoLoco` ON = GoGo walk | Forget the plugin / leave Replace / reuse `Go/Locomotion` |
| **Replace** `GoLocoBaseWD` | GoGo owns walk. `Go/Locomotion` OFF is GoGo still/FBT, **not** shop crouch/prone | Owner wants shop default |
| **Disabled Replace** | Still GoGo walk at bake | “I turned it off” |
| **Append** without passthrough | Dual walk (GoGo first appended layer weight 1, WD ON Thumbnail) | Never |

Stock MA All prefab defaults all three merges to Append. One fusion live: Base **Append** + plugin; Action **Replace**; Sitting **Append**. Fill the table from `maps/<avatar>/`.

Menu: `菜单/功能/GoGo走路` Toggle `VrcDcc/GoGoLoco=1`, default **off**, `isSynced=false`. Last VRCFury bake still had that button writing `Go/Locomotion` — that is the world build. Live scene is retargeted. `VrcDccLocoSdkHook` (after VF compressor) strips remaining `Go/Locomotion` toggles (main + `subParameters`) and unsaves the baked param. Vendor `Assets/` menus are Instantiated; bake clones (empty path / `com.vrcfury.temp` / NDMF temp) are stripped **in place** so the SDK `ctx=null` pass does not drop an unsaved copy. Do **not** edit vendor `GoMenuLoco.asset` / `GoAllParameters.asset` or ApplyPrefab.

`GoLocoBaseWD` default state is **Avatar 3D Thumbnail** until `TrackingType>2`. Editor Play is **not** proof (VF haptic hang). In-world: [upload-test.md](upload-test.md). Board: [review-board.md](review-board.md).

## Live wiring

Do not copy another body's Hierarchy into this avatar. Record the live GOs in `maps/<avatar>/STATE.md`. A filled fusion example: [examples/composite-avatar.md](examples/composite-avatar.md).

Descriptor still *references* shop loco in Edit either way. After Append+passthrough, bake **keeps** shop Base layers. Do not clear Gesture/FX unless the Owner named that cost.

## Do not

- Leave Base **Replace** (enabled or not).
- Append GoGo Base **without** the passthrough plugin (dual walk).
- Append GoGo Action onto a custom Action that already uses `VRCEmote`.
- Add a new **synced** bit for the switch. Local `VrcDcc/GoGoLoco` is required; `Go/Locomotion` is GoGo idle.
- Set `Go/Locomotion` **saved=true** again, or ApplyPrefab the All prefab (would restore vendor saved=1).
- Turn on ABT (third Base + 256). Pack = prefab only, not a disabled child.
- Edit vendor `GoLocoActionWD` AFK states, or unmute Action `AFK==true` without Owner. Headset AFK is `vrc-dcc.afk-owner`.
- Use Beyond unless Owner asks (extra FX + 1 bit).
- Parent SPS/PCS to GoGo height puppet.
- Expect Editor Play to prove loco. World: [upload-test.md](upload-test.md).

Write Defaults: avatar root already has VRCFury Fix/Auto. GoGo **All** uses `*WD`. Match WD. The passthrough state is the **one** WD-OFF overlay on GoGo’s appended layers.

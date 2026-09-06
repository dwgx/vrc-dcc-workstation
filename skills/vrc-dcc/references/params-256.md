# Synced parameters (256)

Edit descriptor cost ≠ Play bake cost. Always dump **both**. Live numbers: `maps/<avatar>/` + `vrc_audit`.

## Two numbers

- **Edit** `VRCExpressionParameters.CalcTotalCost` on the source asset.
- **Bake** after NDMF/VRCFury. Never save the scene in Play — compressor leftovers (`VF53_*`) get written into the source asset.

## WantSynced OR

NDMF `ParameterInfo`: `oldP.WantSynced |= newP.WantSynced`. A MenuItem with `isSynced=true` **overrides** MA Parameters `localOnly`. Fix the MenuItems (or both). Scene overrides on a vendor prefab (ABT) are lost if that prefab is re-instantiated.

## Clothes vs gizmos

Playbook: `clothing-menu.md` / `docs/CLOTHING_MENU.md`. Strip Bools 1 bit; Int/Float always 8. Group pieces before unsyncing colors the Owner wants others to see. Size radios (`SPS_DickSize`) are 8 bits unless `localOnly`.

VRCFury Parameter Compressor: set EditorPrefs to **Compress**, never **Ask** (`DisplayDialog` hangs MCP). It runs when over 256; under 256 it stays off (no extra sync delay).

## Find in Edit

`GameObject.Find` skips inactive parents. Rest-OFF gizmos: `GetComponentsInChildren(..., true)` from the avatar root.

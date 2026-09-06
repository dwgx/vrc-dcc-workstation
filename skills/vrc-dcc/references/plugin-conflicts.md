# Plugin conflicts (lanes)

Two gizmos that both write the **same playable** (AFK, Base loco, Action emotes, 3-audio, 256 bits, face morphs) are a **lane**. The agent does not silently pick. The Owner names a winner; that goes in `maps/<avatar>/conflicts.json`. Unity implements the winner with an NDMF owner plugin when the loser would still bake.

## Do this when a new overlap shows up

1. Name the **lane** (one word: `afk`, `loco`, `action_emotes`, `sitting`, `audio`, `bits`, `face`).
2. Table in Chinese: who wants it, what breaks if both, recommended winner, cost.
3. Wait unless `conflicts.json` already has that lane.
4. Write the ruling into `conflicts.json` the same slice. Do not leave it only in chat.
5. If the loser still bakes while disabled (MA `GetComponentsInChildren(true)`), **mute / remove / mode-change** — do not “turn the checkbox off”.

## Example bias (Owner fills `conflicts.json`)

Do not copy another body's winners. One fusion table that used this station: [examples/composite-avatar.md](examples/composite-avatar.md). Pattern:

| Lane | Typical choice | Loser | How |
|---|---|---|---|
| `loco` | shop Base default | GoGo Base Replace | `vrc-dcc.loco-switch` + local menu Bool |
| `action_emotes` | GoGo | shop Action AFK/emotes | Action **Replace** (accepted cost) |
| `afk` | Owner-named face/sleep gizmo | GoGo Action `AFK==true` | `vrc-dcc.afk-owner` |
| `audio` | Owner-named | the other AudioSources | 3-source cap |
| `bits` | stay under 256 | new synced Int/Bool | cut first |

Suyasuya (if that is the AFK winner) is **face** on FX, not a second full-body lie-down. Headset off + face winner = sleepy face, **not** GoGo floor sleep. GoGo **manual** AFK / emote buttons (`VRCEmote`) stay. Only VRChat `AFK` (headset) is taken from GoGo Action when `vrc-dcc.afk-owner` is on.

## NDMF

- Marker `VrcDccAfkOwner` on the same GO as `VrcDccLocoSwitch` when both exist. Winner string comes from `conflicts.json`.
- Do **not** edit vendor GoGo / sleep controllers. Bake-time mute / AnyState only.
- If the named AFK face gizmo is not merged, the pass still mutes GoGo AFK and logs a warning.

## File

`maps/<avatar>/conflicts.json` — copy from `maps/templates/conflicts.json` (`init_avatar.py`). MAP renders the bias table. Unknown lane → ask, do not invent.

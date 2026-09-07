# Station maintain loop (not 改模)

Load this when the owner asks to improve / expand **this clone**, or after compaction on a station window. Not a Unity mutate. Not Worlds live dumps.

`notes/CURRENT.md` is the **avatar job door**. This loop’s live board is gitignored `notes/HANDOFF.md` (copy `templates/HANDOFF.md` if missing). Expansion lanes: gitignored `notes/tracks/` (`templates/TRACK.md`).

Public queue: `docs/ITERATION.md` / `docs/PR_SLICES.md`. Overlay facts stay out of git (`docs/MAINTAIN.md`).

## 0. Where you are

Quote `session-probe`. `kind: station` → patch **this clone** only. Do not write the avatar Unity project. Do not POST `8080`. Do not run `handshake.py` for a shop body unless the owner named that 改模 job in this chat.

| Ask | Door |
|---|---|
| Clothes / menus / visemes / this avatar | `CURRENT.md` → `slice-loop.md` → `handshake.py <avatar>` |
| Pins / skills / i18n / maps CLI / slices / “what next for the station” | `HANDOFF.md` → this file |
| Worlds / Udon | `skills/vrc-world` — still not live `world_*` until that slice |

## 1. Read (once)

1. `AGENTS.md` stop lines. Gitignored `OWNER.md` if present.
2. `notes/HANDOFF.md` (present tense). Then **one** track file if the mission is that lane.
3. `git status` — uncommitted overlay vs skeleton.
4. `docs/ITERATION.md` only for the named public slice. Do not skip ahead to World live or a second Unity MCP.

## 2. One mission

Write the exact next action on `HANDOFF.md` **before** starting a second track. Dual-axis after landing (`skills/vrc-review`). Offline `PASS` ≠ Unity compile; compile without Editor is `NOT_RUN`.

Commit only when the owner asks. English message. Do not force-push.

## 3. Memory (local, not git)

| Live | Gitignored | Public |
|---|---|---|
| Next station action | `notes/HANDOFF.md` + `notes/tracks/` | `ITERATION.md` status row |
| 改模 freeze / products | `notes/CURRENT.md` + dated notes | — |
| Lesson for the next body | — | `skills/vrc-dcc/references/` |
| Control loop | — | `maps/` + `unity/vrc-dcc-tools` |

High-ambiguity SDK/Udon/MCP facts: copy [`templates/CHAT_RESEARCH.md`](../../../templates/CHAT_RESEARCH.md) into gitignored `notes/packs/` and give it to a web-research chat. Do not skip ahead to live `world_*` HTTP.

## Never

SDK Publish, user-global MCP/skills, Unity 6 MCP on 2022.3, `execute_code` teachers, copying Kaguya freeze onto a new body, promoting overlay into `dwgx/vrc-dcc-workstation`.

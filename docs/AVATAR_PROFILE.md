# Avatar profile (any body)

This skeleton has **no default avatar**. Foreign clones and public PRs must not treat one shop character (including the author’s live body) as the product.

| Layer | Where | Tracked in git? |
|---|---|---|
| How to 改模 | `skills/vrc-dcc/references/` | Yes — generic |
| *This* body | gitignored `maps/<avatar>/` + `OWNER.md` | No |
| Synthetic structure example | `skills/vrc-dcc/references/examples/composite-avatar.md` | Yes — labeled example only; no user project |

## Door

1. Owner names an id, or `notes/CURRENT.md` Products table does.
2. **Read / audit / inspect:** if `maps/<id>/` is missing, report the gap and stop. Do **not** run `init_avatar.py` just because a playbook was opened.
3. **Create a profile:** only when the owner asked to seed a body, then `python maps/init_avatar.py <id>` (refuses if the folder exists).
4. `python maps/handshake.py <id>` — **required argument**. CLIs do not default to a character name.
5. Live facts: `STATE.md`, `MAP.md` **确定**, `POLICY.json`, `conflicts.json`, `REVIEW.json`.

Playbooks that mention `Body_b`, `paryi_Loco`, or a shop outfit name are **patterns or examples**. Dump the live prefab before copying them.

Station vs product vs later world domain: [DOMAINS.md](DOMAINS.md). How the public skeleton iterates: [ITERATION.md](ITERATION.md).

# Contributing

Thanks for improving **vrc-dcc-workstation**.

This is a skeleton: manifests, skills, templates, bootstrap. **No** third-party binaries, **no** `local.json`, **no** SDK cookies.

1. Keep `bootstrap.ps1` dry-run safe (no `-Apply` ⇒ no writes).
2. Pins must cite official sources and a verification date.
3. English `README.md` is canonical. Keep `README.zh-CN.md`, `README.ja.md`, and `README.ko.md` in sync for user-facing changes. Same for `AGENTS.*` / `DISCLAIMER.*` and `docs/i18n/<locale>/WORKFLOW.md`.
4. Pipeline docs (`docs/WORKFLOW.md`, `docs/UNITY.md`) stay current with `manifests/tools.json`.
5. Validate JSON: `python -c "import json,glob;[json.load(open(f,encoding='utf-8')) for f in glob.glob('manifests/*.json')]"`
6. Language layout: `docs/I18N.md`. Do not add a locale unless you will maintain the siblings.
7. Clone-owner prompts: gitignored `OWNER.md` (`OWNER.example.md`). Self-maintain: `docs/MAINTAIN.md`. Chat cannot waive stop lines.
8. Public PRs: [docs/PR_SLICES.md](docs/PR_SLICES.md). Do not commit live `maps/<avatar>/`, world overlays, research ZIPs, or chat archives. Avatar vs world: [docs/DOMAINS.md](docs/DOMAINS.md). No default character: [docs/AVATAR_PROFILE.md](docs/AVATAR_PROFILE.md).

See `AGENTS.md` for the agent handshake.

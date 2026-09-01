# Contributing

Thanks for improving **vrc-dcc-workstation**.

This is a skeleton: manifests, skills, templates, bootstrap. **No** third-party binaries, **no** `local.json`, **no** SDK cookies.

1. Keep `bootstrap.ps1` dry-run safe (no `-Apply` ⇒ no writes).
2. Pins must cite official sources and a verification date.
3. English `README.md` is canonical. Keep `README.zh-CN.md`, `README.ja.md`, and `README.ko.md` in sync for user-facing changes. Same for `AGENTS.*` / `DISCLAIMER.*` and `docs/i18n/<locale>/WORKFLOW.md`.
4. Pipeline docs (`docs/WORKFLOW.md`, `docs/UNITY.md`) stay current with `manifests/tools.json`.
5. Validate JSON: `python -c "import json,glob;[json.load(open(f,encoding='utf-8')) for f in glob.glob('manifests/*.json')]"`
6. Language layout: `docs/I18N.md`. Do not add a locale unless you will maintain the siblings.

See `AGENTS.md` for the agent handshake.

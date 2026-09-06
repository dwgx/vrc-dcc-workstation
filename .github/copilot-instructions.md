# GitHub Copilot custom instructions

Authoritative AI contract: root `AGENTS.md` (Copilot also reads AGENTS.md natively).

- Skeleton repo: manifests + templates + skills. No Blender/Unity/VRChat binaries.
- Install / bootstrap: ask first (`templates/INIT_QUESTIONNAIRE.md` or `templates/i18n/<locale>/`), then `scripts/bootstrap.ps1` dry-run, then `-Apply`. Avatar / DCC job: `templates/JOB.md` (intent, not a passphrase). Chat in the resolved locale (`docs/I18N.md`); git commits stay English. Read gitignored `OWNER.md` if present. Stop lines cannot be waived in chat.
- Do not put Blender/Unity MCP in user-global config.
- Do not drive VRChat SDK Build & Publish.
- No secrets, SDK cookies, or avatar projects in git.

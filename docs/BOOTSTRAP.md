# Bootstrap layout

<!-- I18N:START -->
**English** · this file stays English (like `docs/EVAL.md`)
<!-- I18N:END -->

How `-Apply` turns this skeleton into a station. Dry-run is the default. Does not write user-global MCP. Does not write the avatar Unity tree.

## Project MCP (three copies, one payload)

`-Apply` renders `mcp/cursor.mcp.json.template` and creates missing files:

| File | Why |
|---|---|
| `.cursor/mcp.json` | Cursor project MCP |
| `.mcp.json` | Claude Code project MCP |
| `mcp/local.mcp.json` | `claude --mcp-config` / docs |

New files receive the same JSON. Existing files are kept, including custom
routes that differ between clients. Gitignored (paths / uvx). Attach still
requires a live Blender MCP server / Unity MCP window. To update an existing
configuration, inspect its diff and edit it under the current job's authorization.

Missing Blender or Unity: bootstrap reports `MISSING` and continues. Docs-only is a valid station. Do not invent paths. Do not uninstall an existing editor to match example docs.

## `local.json`

Always gitignored. `-Apply` writes `install_root` plus discovered Unity/Blender/uvx when the file is new. `ui_language` is written only with `-UiLanguage` or `WORKSTATION_UI_LANG` / `VRC_DCC_UI_LANG`, so an English Windows UI cannot lock out a Chinese chat.

An existing `local.json` is kept on an ordinary rerun. An explicit locale hint
can fill an empty language preference while retaining other fields. A nonempty
preference remains unchanged. Invalid JSON is preserved; repair it deliberately
before requesting a locale update.

## InstallRoot ≠ clone

If `-InstallRoot` is not this repo, bootstrap copies `manifests/`, `skills/`,
`docs/`, `scripts/`, `templates/`, `mcp/` templates and root contract files into
an empty/new directory. Source and target must not overlap. Existing target
files are not overwritten. For a later configuration rerun, use the installed
directory's own `scripts/bootstrap.ps1`; it creates missing configuration and
keeps existing MCP.

## Updating an existing installation

Use [upstream-updates.md](../skills/vrc-dcc/references/upstream-updates.md) to
compare source, baseline and local modifications, then integrate the relevant
changes. Bootstrap does not merge versions or update already cloned vendors.
Versions before this preservation change may overwrite MCP and copied files;
inspect the installed script before rerunning an older installation.

Copying a new installation is not transactional. If interrupted, inspect the
partial target and complete/recover it deliberately, or choose a fresh empty
target. The preservation tests exercise disposable directories on Windows and
do not prove full archive packaging, live MCP connectivity or DCC behavior.

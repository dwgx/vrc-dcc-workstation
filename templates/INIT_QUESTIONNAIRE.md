# Init questionnaire (vrc-dcc-workstation)

AI: ask these before writing `local.json` or attaching MCP. Structured options + a recommended default.

## Q1. Install root

Where does this clone live?
- Recommended: the clone directory itself.

## Q2. Blender

- [ ] Path to `blender.exe` (target: **5.2 LTS**)
- [ ] Install/enable blender-mcp addon this session?
- Recommended: fill path; human starts **Start MCP Server** when a live scene is needed.

## Q3. Unity

- [ ] Unity **2022.3 LTS** editor path
- [ ] Avatar project `.unity` / project folder (optional until a DCC job)
- Recommended: 2022.3, not Unity 6, for this avatar pipeline.

## Q4. MCP for this job

- [ ] None (docs/skills only)
- [ ] Blender stdio (`blender-mcp` pin in `manifests/tools.json`)
- [ ] Unity HTTP (`mcpforunityserver` / CoplayDev after UPM in the **open** project)
- [ ] Both
- Recommended: none until the job edits a scene. Never user-global MCP.

## Q5. Optional vendors

- [ ] CATS Blender Plugin 5.2 fork (Alrauna)
- [ ] gummidot vrchat-agentic-tools docs
- [ ] felixchaos vrchat-avatar-modding-skill
- Recommended: clone when the job needs them (`bootstrap.ps1 -Apply -CloneMcp`).

## Q6. AI client

Claude Code / Codex / Cursor / Gemini / Copilot / Grok — so we emit the matching entry file only.

## Q7. Forbidden (confirm understood)

- [ ] Agent will not click VRChat Build & Publish
- [ ] Agent will not install official Unity 6 MCP into this 2022.3 project
- [ ] Agent will not store SDK cookies

After answers: write a short plan, then execute.

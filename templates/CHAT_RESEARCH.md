# Chat / web-research pack (copy, do not commit the filled one)

Use a **web-enabled, high-reasoning** chat (ChatGPT, etc.) for decisions that need current docs, SDK assembly facts, or Udon/MCP research. This station implements after that answer is dual-axis reviewed. Do not treat the chat reply as `AGENTS.md`.

## How

For a delegated browser researcher, wrap this prompt in [WEB_TASK.md](WEB_TASK.md) with `artifact_class=research`. The [web handoff workflow](../skills/vrc-dcc/references/web-handoff.md) records dispatch identity, actual prompts, interrupted sends, saved research and file checks. Keep source verification separate from file integrity.

1. Copy this file’s “Paste block” into gitignored `notes/packs/<date>/PROMPT.md` and fill the clone-local blanks (no SDK cookies, no `C:\Users\…` unless the owner wants that machine in the research).
2. Attach or paste [`docs/FRAMEWORK.md`](../docs/FRAMEWORK.md), [`docs/DOMAINS.md`](../docs/DOMAINS.md), [`docs/PR_SLICES.md`](../docs/PR_SLICES.md), [`docs/WORLD.md`](../docs/WORLD.md), [`skills/vrc-dcc/references/evidence-layers.md`](../skills/vrc-dcc/references/evidence-layers.md).
3. Ask for **decisions**, not a second constitution. Promote a rule here only if the next foreign clone would hit it (`docs/SOURCES.md`). The 2026-09-07 pack is already absorbed in [FRAMEWORK.md](../docs/FRAMEWORK.md); re-run only if Unity / CoplayDev / MCP / Worlds SDK facts changed.

## Paste block (English)

```text
You are a research analyst for vrc-dcc-workstation (public VRChat DCC agent station).
Reply with decisions + cited URLs. Do not write malware, exploits, or VRChat upload/cookie tooling.

Constraints (hard):
- Public repo is a skeleton: no default avatar, no world product rename.
- Human clicks VRChat SDK Build & Publish. No upload_* APIs. No execute_code / execute_csharp.
- CoplayDev unity-mcp is the default Editor bridge. No second Unity MCP. No Unity 6 MCP on 2022.3 avatars.
- Do not add Avatar SDK / Modular Avatar to a Worlds project to compile avatar tools.
- Do not add Worlds SDK to an avatar project because a playbook mentioned Udon.
- Named station avatar tools are vrc_*. Station world tools (world_probe, world_scene_dump, world_udon_inventory) are PROPOSED. Prefix is not callable until IMPLEMENTED_WORLD lists them. This adapter roadmap does not block production through installed native MCP, provider CLI/SDK or project-owned builders; see docs/WORLD_PRODUCTION.md.
- Avatar and World jobs use different Unity projects and Editors. A shared CoplayDev HTTP server needs an opaque discovered instance id; first-session fallback is refuse.
- Keep Mcp-Session-Id on the station client. Do not install official Unity 6 MCP on 2022.3.
- Python already has: JOB lease + file lock, tool allowlist (cross-domain), evidence fingerprints + STALE + owned plan/apply, world handshake/gate without HTTP.

Need you to web-search and decide:

1. Core vs Avatar vs World C# assemblies in 2022.3: recommended asmdef references so World adapter does not import VRCSDK3A / MA, and Avatar adapter does not import Worlds/Udon. Cite current VRChat / UdonSharp / MA package IDs.

2. Evidence STALE: after Editor mutate, which layers must be recaptured for avatars (NDMF) vs worlds (UdonSharp compile, ClientSim, late join)? Map to our layers: STATIC_SOURCE, UNITY_RESOLVED, NDMF_BUILT, UDON_COMPILED, CLIENTSIM, CLIENT_RUNTIME, MULTIPLAYER, UPLOAD_CONFIRMED.

3. CoplayDev unity-mcp (current major): can two Editor packages register disjoint tool prefixes (vrc_* vs world_*) on one HTTP 8080, or must world jobs use a separate Editor instance? Cite migration/networking docs.

4. Identity: first VRCSceneDescriptor is forbidden (same as first VRCAvatarDescriptor). Official or community guidance for “which scene is loaded” fingerprints (GUID + Editor instance) in 2026.

5. Library v2: asset × avatar profile without making one live-test body the public default. Any existing VRChat catalog patterns to copy (names only, no meshes).

Output format:
- Decision (one sentence)
- Evidence (URLs + what you verified)
- Alternatives we should reject
- Suggested next public slice text for PR_SLICES.md (S01-b and/or S01-c)
- What must stay overlay-only
```

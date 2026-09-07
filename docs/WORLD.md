# Worlds pipeline

Production starts at [WORLD_PRODUCTION.md](WORLD_PRODUCTION.md)
([简体中文](i18n/zh-CN/WORLD_PRODUCTION.md)). Use the owner's current project and
installed Unity/Blender tools to build and verify complete World slices.

## Current production route

1. Recover the requested result, writer, project root and accepted scene/assets.
2. Discover installed tools; select the observed Editor instance and read back
   its project and scenes. Use native MCP, an installed provider CLI/SDK or
   inspectable project-owned builders as appropriate.
3. Implement the authorized work, inspect it, compile and test as relevant,
   save and reopen for readback. Continue useful slices in the same task.
4. Record actual outputs and remaining checks in the project handoff.

An explicitly read-only intake stays read-only. Station maintenance edits this
clone; production writes belong to the authorized World project writer. World
work has no Avatar handshake or Booth SKU quota.

## Target identity

Identify the project instance and loaded scenes before an Editor operation.
Record scene GUID/path, dirty state, order and active scene as relevant. Resolve
the intended descriptor and Main/Prefab Stage for descriptor changes. A port or
display name alone cannot select the target. Preserve unrelated dirty scenes;
an unsaved scene has no saved GUID until an authorized save.

Use the existing CoplayDev bridge with explicit instance routing. Keep target
selection and operations in the same session, or use a supported per-call
instance selector. Recheck after reconnect/reload. Avatar and World SDKs belong
in their respective projects. See the [multi-instance guide](https://coplaydev.github.io/unity-mcp/guides/multi-instance).

## Optional station adapter and maps

The [FRAMEWORK.md](FRAMEWORK.md) package split and S01-b/c milestones describe
future **station** tools. `world_probe`, `world_scene_dump` and
`world_udon_inventory` are proposed. `IMPLEMENTED_WORLD` stays empty until an
adapter is implemented and tested. This does not disable installed provider
tools or project-owned Editor code.

Optional local records:

```text
python maps/init_world.py <world-id>
python maps/world_handshake.py <world-id>
python maps/world_gate.py <world-id> begin <review-id>
```

Set `VRC_DCC_JOB_HOLDER` when using the ledger. The same holder can advance to
another REVIEW row without resetting. A competing live holder is rejected.
`mutated` advances the project revision; `reset` releases the lease and open
slice while preserving change history. Existing project records need not migrate.

Handshake reports both `implemented_world_tools: false` and
`production_route: discover_installed_editor_tools`. The first field describes
only the station adapter. S01-c's proposed read-only probe still needs its own
compile and two-Editor routing evidence before release.

## Evidence and delivery

Keep static files, C# compilation, UdonSharp compilation, ClientSim, Desktop,
PCVR and real multiplayer evidence separate. Test what the feature needs:
shared state includes ownership, late join and owner-leave behavior. Recapture
affected evidence after changes.

Agents can perform authorized Play and [Build & Test](https://creators.vrchat.com/worlds/udon/using-build-test/).
SDK **Build & Publish** remains the owner's step. Save a usable project handoff
with outputs, verification and the next action. Private project details and
assets stay in the project or ignored overlay.

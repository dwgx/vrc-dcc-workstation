# World production with installed tools

Use this workflow to build a VRChat World in the project the owner named.
The existing Unity and Blender toolchain can support production today. S01-b
and S01-c describe future **station adapter** work; they are not prerequisites
for modeling, scene editing, Udon development, import, compilation or testing.

English · [简体中文](i18n/zh-CN/WORLD_PRODUCTION.md)

## Start from the current project

Recover the requested result, actual project root, current writer, accepted
scene/assets, latest saved state and remaining acceptance from the project
handoff. Inspect disk and Editor state before replaying an action. Without Git,
use file hashes and a backup of affected scene/assets. Existing project records
are sufficient; station maps are optional.

An authorized production request includes necessary reversible implementation
and checks within its scope. Reuse authorization already given. Ask only when a
missing decision changes the target, ownership, external publication or intended
result. An explicitly read-only intake remains read-only. Station maintenance
changes this clone; the World project writer performs project changes.

World work has no Avatar handshake, Booth SKU quota or fixed tool-call/chat cap.
Continue through useful slices in the same task. Checkpoint when a result is
saved, before a risky transition, or when handing work to another writer.

## Discover and use available tools

Prefer the project's connected native MCP tools. If that client is unavailable,
use an already installed provider CLI or the MCP SDK against the same bridge.
Discover tools/resources and read actual schemas before calling them. A missing
station `world_probe` does not mean the provider's tools are unavailable. Use
the installed version; a documentation example is not proof of a local tool.

Select the observed instance identifier, then read back its project root and
loaded scenes. A listening port is insufficient. With multiple Editors, keep
target selection and operations in the same MCP session, or use a supported
per-call instance selector. Read identity again after reconnect or domain reload.
See the provider's [multi-instance guide](https://coplaydev.github.io/unity-mcp/guides/multi-instance).

Record scene paths/GUIDs, active scene and dirty state relevant to the change.
For descriptor operations, resolve the intended descriptor and Main/Prefab Stage.
Preserve other dirty scenes. Keep Avatar and Worlds SDKs in their respective
projects; a World does not need the station's Avatar Editor package.

Use available scene, object, component, asset, script, console and Editor tools
for the requested work. Project-owned Editor C# or Blender builder scripts are
appropriate for reproducible geometry or repeated changes. Keep their source
inspectable and write set explicit. A generic execution tool, when actually
exposed and authorized, is evaluated by its operation and target; its name alone
is not a reason to disable World production. Custom tools can be registered
through the provider's [Editor extension mechanism](https://coplaydev.github.io/unity-mcp/guides/custom-tools).

`maps/allowlist.py` governs only `maps/unity_mcp_call.py`, the station's optional
named-tool client. It does not configure or disable native MCP, provider CLI/SDK
or project-owned builders. Its empty `IMPLEMENTED_WORLD` accurately means that
the proposed **station** `world_*` tools have not shipped.

## Build a complete, reviewable slice

Choose a concrete visible or playable result, such as one furnished room or one
working interaction. Record its dimensions, behavior and acceptance in the
project. Reuse suitable assets and accepted work. Gather specific missing
information while continuing independent implementation. A concept image is
input to construction.

Keep one writer for a shared Editor or overlapping assets. Independent research,
asset preparation and review can run in parallel when delegated. For uncertain
imports or generated models, a project-owned review scene makes inspection and
rollback easier. Build, inspect proportions/materials/colliders, save, reopen and
read back before promoting the result into the accepted scene.

After a timeout or disconnect, inspect effects before retrying: the Editor may
have applied the change without returning a response. Record saved paths and
actual results, then continue the next authorized slice. Avoid repeating completed
imports, generation or setup after compaction.

## Verify what the change needs

Separate file integrity, visual inspection, Editor C# compilation, UdonSharp
compilation, ClientSim, Desktop, PCVR and real multiplayer evidence. Run checks
relevant to the change. A static model needs geometry/material/collision inspection;
a synced interaction also needs ownership, late join and owner-leave checks.
A screenshot or `is_compiling=false` alone proves neither compilation nor
playability. Record unavailable checks as not tested with a useful next action.

Agent-driven Play, save, import and **Build & Test** can be part of authorized
production. [VRChat Build & Test](https://creators.vrchat.com/worlds/udon/using-build-test/)
supports local client testing. The owner performs SDK **Build & Publish**.

## Recoverable outputs, compatible records

Preserve original research/image/model outputs and prompts actually sent. Use
[web-handoff.md](../skills/vrc-dcc/references/web-handoff.md) when a shared producer
contract is useful. Existing project task cards and receipts can remain in their
current format. The optional checker verifies its own bundle format; it is not
a permission gate or a requirement to redo otherwise valid work.

If using station maps, `world_gate.py <id> begin <review-id>` records the current
slice with the same holder across a task. `mutated` advances the project change
revision. `reset` releases the lease and open slice while preserving mutation
history. Legacy Avatar SKU fields are ignored and removed on the next JOB save.
Capture new evidence after relevant changes; resetting a lease does not refresh it.

End a slice with saved outputs, relevant checks, unresolved observations and the
next implementation action in the project handoff. Keep private paths, assets,
conversation IDs and world identifiers in the project or ignored station overlay.

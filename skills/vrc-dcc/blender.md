# Blender (VRC)

- Exe path: `local.json` `blender_exe` (handshake). Target: **5.2 LTS**.
- MCP add-on: enable **Interface: Blender MCP**, then N-panel **Start MCP Server** (port 9876).
- Client: `uvx --python 3.11 blender-mcp==<pin>` with `UV_PYTHON_PREFERENCE=only-managed` if default Python is 3.14+.
- Optional CATS 5.2: `bootstrap.ps1 -Apply -CloneMcp` → `vendors/upstream/cats-blender-plugin-5.2` (gitignored). Install the zip in Blender only if the job needs CATS.
- Export FBX for Unity. Humanoid names must match the **target** armature before MA merge. Extra clothing breast chains (`Breast_L.002`) are a weight job — [references/clothing-fit.md](references/clothing-fit.md).
- Shapekeys / visemes: finish in Blender. Do not expect Unity to rebuild mouth shapes.
- Fallback if 5.2 rejects ahujasid: `dcc-mcp-blender` pin in `manifests/tools.json`. One blender MCP server per client.
- Extra search paths (optional env, not git): `VRC_DCC_BLENDER`, `VRC_DCC_UVX`.

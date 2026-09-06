# Unity / Modular Avatar

Project path: `local.json` `unity_project`. Editor: Unity **2022.3 LTS**. Package adds happen in that project's window. URLs: `docs/UNITY.md`.

## Non-destructive first

- Merge clothes with **MA Merge Armature** / Merge Animator / Menu Installer / Parameters. Do not bake NDMF unless asked.
- Keep vendor prefabs intact. Work copies under a work folder. Follow the project’s **`Assets/功能`** and **`菜单/功能`** layout; do not dump gizmos on the avatar root.
- Body identity first (Booth / fusion mesh). Generic vendor “All” prefabs are wrong until matched.
- Synced parameters: audit bit cost before adding toggles. Group strip Bools (上衣+领+袖), do not default to one synced Bool per ribbon.
- PhysBones / Contacts: diagnose; human approves deletes. See [references/physbones.md](references/physbones.md).
- FaceEmo + MA menus: do not duplicate the same parameter in two owners.
- Clothing menus (outfit Int / strip Bools / color radios, 256-bit budget): [references/clothing-menu.md](references/clothing-menu.md). **Fit / chest / extra bones:** [references/clothing-fit.md](references/clothing-fit.md). **Marshmallow vs SPS/PCS:** [references/marshmallow-erp.md](references/marshmallow-erp.md). **Reactive components on a MenuItem follow that item's parameter, even if the submenu is closed and another outfit is on.** MeshCutter / body ShapeChanger belong on the **clothing mesh** (inactive with the piece). Last ObjectToggle in hierarchy wins.
- Do not add body blendshapes to clothing clips the vendor clip did not drive.
- Default-off gizmos need a MenuItem. Rest-OFF meshes are not “missing”.
- lilToon / materials: do not swap shaders unless the job is materials.
- Session rules: [references/dcc-session.md](references/dcc-session.md). Token caps: [references/token-budget.md](references/token-budget.md).
- VRCFury mixed Write Defaults: Fix Write Defaults / Auto on the avatar root. PCS/SPS menu clicks need MA Parameters on that installer before bake.
- Bits: [references/params-256.md](references/params-256.md). Do not save the scene in Play. **Do not re-add `ABT.prefab`.** Loco: [references/gogoloco.md](references/gogoloco.md). In-world test: [references/upload-test.md](references/upload-test.md). Intake: [references/avatar-intake.md](references/avatar-intake.md).

## MCP / C# in Editor

1. CoplayDev unity-mcp — pin in `manifests/tools.json`. HTTP `localhost:8080/mcp`. Named `vrc_*` after `com.vrc-dcc.tools`.
2. Do **not** install lighfu UnityAgent / `execute_csharp` `:14523` / EditorEye on this 2022.3 avatar project.
3. Never `EditorUtility.DisplayDialog` from MCP (hangs the Editor).
4. Prefer named `vrc_*` (then CoplayDev `manage_gameobject` **modify** if needed) over editing `.prefab` / `.unity` YAML by hand. Do **not** invent `execute_code`. Do **not** use `execute_csharp`, `ExecuteMenuItem`, or VRC SDK builder APIs to Build & Publish.
5. Before the first Unity mutation, `GetDynamicTools` must list `unityMCP` in this chat. CoplayDev wizard: Skip; AutoRegister off. If `vrc_audit` missing: Unity cwd `scripts/install-vrc-dcc-tools.ps1`, Reload.

Do not install official Unity MCP (Unity 6) into this 2022.3 avatar project. Extra Hub path: env `VRC_DCC_UNITY_HUB`.

## Upload

Human clicks SDK Publish. No cookies in notes/git/chat.

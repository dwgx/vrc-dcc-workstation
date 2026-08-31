# Unity / Modular Avatar

Project path: `local.json` `unity_project`. Editor: Unity **2022.3 LTS**. Package adds happen in that project's window. URLs: `docs/UNITY.md`.

## Non-destructive first

- Merge clothes with **MA Merge Armature** / Merge Animator / Menu Installer / Parameters. Do not bake NDMF unless asked.
- Keep vendor prefabs intact. Work copies under a work folder.
- Synced parameters: audit bit cost before adding toggles.
- PhysBones / Contacts: diagnose; human approves deletes. See [references/physbones.md](references/physbones.md).
- FaceEmo + MA menus: do not duplicate the same parameter in two owners.
- lilToon / materials: do not swap shaders unless the job is materials.

## MCP / C# in Editor

1. CoplayDev unity-mcp — pin in `manifests/tools.json`. HTTP `localhost:8080/mcp`.
2. lighfu UnityAgent `editor-v*` — VPM `https://lighfu.github.io/vpm/`.
3. Never `EditorUtility.DisplayDialog` from MCP (hangs the Editor).
4. Prefer `execute_csharp` / UnityAgent tools over editing `.prefab` / `.unity` YAML by hand.

Do not install official Unity MCP (Unity 6) into this 2022.3 avatar project. Extra Hub path: env `VRC_DCC_UNITY_HUB`.

## Upload

Human clicks SDK Publish. No cookies in notes/git/chat.

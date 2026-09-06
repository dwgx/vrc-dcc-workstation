# PhysBones (thin)

When implementing, read the full gummidot `physbones.md` under `vendors/upstream/vrchat-agentic-tools/` if that vendor was cloned.

- List existing `VRCPhysBone` / colliders before adding any.
- New bones only for **this outfit**. Do not PhysBone fingers, toes, twist bones, or another outfit's chains.
- After copy tools: `rootTransform` may still point at the **source** avatar. Fix to a child of the target, or null if self.
- Hair usually needs a chest capsule collider. Scale to this body.
- Stay under VRChat performance limits. Agent diagnoses; human approves deletes.
- Never `EditorUtility.DisplayDialog` from MCP (hangs the Editor).

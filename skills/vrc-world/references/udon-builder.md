# Udon builder boundaries

Keep three contexts separate:

1. Workstation Python / Editor C#
2. UdonSharp proxy + serialized public variables
3. Compiled Udon runtime

A feature that works as ordinary C# or an Editor initializer is not necessarily valid in Udon.

Use the **installed** SDK’s UdonSharp Editor APIs. Do not generate a plausible MonoBehaviour and infer it is a working Udon program. Validate program asset references, compiled programs, serialized variables, save/reload, and prefab overrides.

Plan before mutation. Preserve GUIDs. Avoid duplicate components. Register Undo where supported. Undo does not reverse importer, lighting bake, or external process effects.

Compile matrix (when assemblies exist): Core without SDK; Avatar with Avatar SDK only; World with Worlds SDK only. Missing SDK → actionable fail, not a silent Avatar fallback.

References: [UdonSharp Editor Scripting](https://udonsharp.docs.vrchat.com/editor-scripting/), [Detecting the SDK](https://creators.vrchat.com/sdk/detecting-vrcsdk/).

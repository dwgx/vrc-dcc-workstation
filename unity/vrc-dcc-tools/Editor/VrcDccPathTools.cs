using System.Collections.Generic;
using MCPForUnity.Editor.Helpers;
using MCPForUnity.Editor.Tools;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;
using VRC.SDK3.Avatars.Components;
using nadena.dev.modular_avatar.core;

namespace VrcDcc.Tools.Editor
{
    [McpForUnityTool("vrc_dangling_params", Description = "FX params with no menu/PB/contact/ParameterDriver/clip-Animator source. Skip VF*.", Group = "core")]
    public static class VrcDanglingParamsTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            return VrcDccCommon.Run(() => Handle(p));
        }

        static object Handle(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var driven = new HashSet<string>();
            var desc = av.GetComponent<VRCAvatarDescriptor>();
            var exprN = 0;
            if (desc != null && desc.expressionParameters != null && desc.expressionParameters.parameters != null)
            {
                exprN = desc.expressionParameters.parameters.Length;
                for (var i = 0; i < exprN; i++)
                {
                    var n = desc.expressionParameters.parameters[i] != null
                        ? desc.expressionParameters.parameters[i].name
                        : null;
                    if (!string.IsNullOrEmpty(n)) driven.Add(n);
                }
            }
            var mis = av.GetComponentsInChildren<ModularAvatarMenuItem>(true);
            for (var i = 0; i < mis.Length; i++)
            {
                if (mis[i] == null || mis[i].Control == null || mis[i].Control.parameter == null) continue;
                var n = mis[i].Control.parameter.name;
                if (!string.IsNullOrEmpty(n)) driven.Add(n);
            }
            VrcDccCommon.CollectParamsByTypeName(av, "VRCPhysBone", "parameter", driven);
            VrcDccCommon.CollectParamsByTypeName(av, "VRCContactReceiver", "parameter", driven);
            var dang = new List<string>();
            var fxN = 0;
            if (desc != null && desc.baseAnimationLayers != null)
            {
                for (var li = 0; li < desc.baseAnimationLayers.Length; li++)
                {
                    var layer = desc.baseAnimationLayers[li];
                    if (layer.type != VRCAvatarDescriptor.AnimLayerType.FX) continue;
                    var ac = layer.animatorController as AnimatorController;
                    if (ac == null) continue;
                    CollectDriversAndClipParams(ac, driven);
                    if (ac.parameters == null) continue;
                    for (var ai = 0; ai < ac.parameters.Length; ai++)
                    {
                        var pn = ac.parameters[ai].name;
                        if (string.IsNullOrEmpty(pn) || pn.StartsWith("VF")) continue;
                        fxN++;
                        if (!driven.Contains(pn)) dang.Add(pn);
                    }
                }
            }
            var cap = dang.Count > 24 ? 24 : dang.Count;
            var shown = dang.GetRange(0, cap);
            return new SuccessResponse("vrc_dangling_params", new
            {
                exprN,
                driven = driven.Count,
                fxN,
                danglingN = dang.Count,
                dangling = shown,
                note = "Menu counts as a source (改模). Driver+clip-Animator also. VF FullController Global still looks dangling until bake."
            });
        }

        static void CollectDriversAndClipParams(AnimatorController ac, HashSet<string> driven)
        {
            var seen = new HashSet<int>();
            if (ac.layers != null)
            {
                for (var i = 0; i < ac.layers.Length; i++)
                    WalkSm(ac.layers[i].stateMachine, driven, seen);
            }
            var clips = ac.animationClips;
            if (clips == null) return;
            for (var ci = 0; ci < clips.Length; ci++)
            {
                var clip = clips[ci];
                if (clip == null) continue;
                var binds = AnimationUtility.GetCurveBindings(clip);
                for (var bi = 0; bi < binds.Length; bi++)
                {
                    if (binds[bi].type != typeof(Animator)) continue;
                    if (!string.IsNullOrEmpty(binds[bi].propertyName))
                        driven.Add(binds[bi].propertyName);
                }
            }
        }

        static void WalkSm(AnimatorStateMachine sm, HashSet<string> driven, HashSet<int> seen)
        {
            if (sm == null || !seen.Add(sm.GetInstanceID())) return;
            var states = sm.states;
            for (var i = 0; i < states.Length; i++)
            {
                var st = states[i].state;
                if (st == null || st.behaviours == null) continue;
                for (var b = 0; b < st.behaviours.Length; b++)
                    CollectDriver(st.behaviours[b], driven);
            }
            var children = sm.stateMachines;
            for (var i = 0; i < children.Length; i++)
                WalkSm(children[i].stateMachine, driven, seen);
        }

        static void CollectDriver(StateMachineBehaviour beh, HashSet<string> driven)
        {
            if (beh == null || beh.GetType().Name.IndexOf("ParameterDriver") < 0) return;
            var so = new SerializedObject(beh);
            var list = so.FindProperty("parameters");
            if (list == null || !list.isArray) return;
            for (var i = 0; i < list.arraySize; i++)
            {
                var el = list.GetArrayElementAtIndex(i);
                AddStringProp(el, "name", driven);
                AddStringProp(el, "source", driven);
            }
        }

        static void AddStringProp(SerializedProperty el, string field, HashSet<string> driven)
        {
            var sp = el.FindPropertyRelative(field);
            if (sp != null && !string.IsNullOrEmpty(sp.stringValue))
                driven.Add(sp.stringValue);
        }
    }

    [McpForUnityTool("vrc_clip_missing_paths", Description = "Source FX clip bindings: missing Transform, blendshape, material slot. False+ on bake-only clips.", Group = "core")]
    public static class VrcClipMissingPathsTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            return VrcDccCommon.Run(() => Handle(p));
        }

        static object Handle(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var desc = av.GetComponent<VRCAvatarDescriptor>();
            if (desc == null || desc.baseAnimationLayers == null)
                return new ErrorResponse("NO_DESC");
            AnimatorController fx = null;
            for (var li = 0; li < desc.baseAnimationLayers.Length; li++)
            {
                var layer = desc.baseAnimationLayers[li];
                if (layer.type != VRCAvatarDescriptor.AnimLayerType.FX) continue;
                fx = layer.animatorController as AnimatorController;
                break;
            }
            if (fx == null) return new ErrorResponse("NO_FX");
            var seenPath = new HashSet<string>();
            var miss = new List<string>();
            var missShape = new List<string>();
            var missMat = new List<string>();
            var bindN = 0;
            var clips = fx.animationClips;
            if (clips != null)
            {
                for (var ci = 0; ci < clips.Length; ci++)
                {
                    var clip = clips[ci];
                    if (clip == null) continue;
                    ScanBinds(av.transform, clip, AnimationUtility.GetCurveBindings(clip),
                        ref bindN, seenPath, miss, missShape, missMat);
                    ScanBinds(av.transform, clip, AnimationUtility.GetObjectReferenceCurveBindings(clip),
                        ref bindN, seenPath, miss, missShape, missMat);
                }
            }
            return new SuccessResponse("vrc_clip_missing_paths", new
            {
                bindN,
                uniquePaths = seenPath.Count,
                missN = miss.Count,
                miss,
                missShape,
                missMat,
                note = "False positives on MA/VF bake-only clips. Constraint type swap is not an error."
            });
        }

        static void ScanBinds(
            Transform root,
            AnimationClip clip,
            EditorCurveBinding[] binds,
            ref int bindN,
            HashSet<string> seenPath,
            List<string> miss,
            List<string> missShape,
            List<string> missMat)
        {
            if (binds == null) return;
            for (var bi = 0; bi < binds.Length; bi++)
            {
                bindN++;
                var path = binds[bi].path;
                if (string.IsNullOrEmpty(path)) continue;
                if (path.IndexOf("ThisHopefullyDoesntExist") >= 0) continue;
                var t = FindInactive(root, path);
                if (t == null)
                {
                    if (seenPath.Add(path) && miss.Count < 32)
                        miss.Add(clip.name + " :: " + path);
                    continue;
                }
                seenPath.Add(path);
                var prop = binds[bi].propertyName ?? "";
                if (prop.StartsWith("blendShape.") && missShape.Count < 12)
                {
                    var shape = prop.Substring("blendShape.".Length);
                    var smr = t.GetComponent<SkinnedMeshRenderer>();
                    if (smr == null || smr.sharedMesh == null || smr.sharedMesh.GetBlendShapeIndex(shape) < 0)
                        missShape.Add(clip.name + " :: " + path + "." + shape);
                }
                var matAt = prop.IndexOf("m_Materials.Array.data[");
                if (matAt >= 0 && missMat.Count < 8)
                {
                    var close = prop.IndexOf(']', matAt);
                    int slot;
                    if (close > matAt && int.TryParse(
                            prop.Substring(matAt + "m_Materials.Array.data[".Length, close - matAt - "m_Materials.Array.data[".Length),
                            out slot))
                    {
                        var r = t.GetComponent<Renderer>();
                        var n = r != null && r.sharedMaterials != null ? r.sharedMaterials.Length : 0;
                        if (slot >= n)
                            missMat.Add(clip.name + " :: " + path + " slot " + slot + "/" + n);
                    }
                }
            }
        }

        static Transform FindInactive(Transform root, string path)
        {
            if (string.IsNullOrEmpty(path)) return root;
            var parts = path.Split('/');
            var t = root;
            for (var pi = 0; pi < parts.Length; pi++)
            {
                Transform next = null;
                for (var c = 0; c < t.childCount; c++)
                {
                    if (t.GetChild(c).name == parts[pi]) { next = t.GetChild(c); break; }
                }
                if (next == null) return null;
                t = next;
            }
            return t;
        }
    }
}

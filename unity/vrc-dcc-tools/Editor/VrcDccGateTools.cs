using System;
using System.Collections.Generic;
using MCPForUnity.Editor.Helpers;
using MCPForUnity.Editor.Tools;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;
using nadena.dev.modular_avatar.core;

namespace VrcDcc.Tools.Editor
{
    [McpForUnityTool("vrc_prefab_identity", Description = "Refuse Instantiate unless prefabPath is this SKU and matches POLICY body_token. wear_fusion is not fitted.", Group = "core")]
    public static class VrcPrefabIdentityTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
            [ToolParameter("Prefab name/path must contain this token. Empty = POLICY body_token.", Required = false)]
            public string token { get; set; }
            [ToolParameter("Exact prefab asset path. Required when POLICY require_prefab_path is true.", Required = false)]
            public string prefabPath { get; set; }
            [ToolParameter("Expected Hips world Y. Empty = POLICY expected_hips_y.", Required = false)]
            public float? expectedHipsY { get; set; }
            [ToolParameter("Hips Y slack.", Required = false, DefaultValue = "0.05")]
            public float? hipsSlack { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            return VrcDccCommon.Run(() => Handle(p));
        }

        static object Handle(JObject p)
        {
            var path = VrcDccCommon.Param(p, "prefabPath", "path", "");
            if (VrcDccPolicy.RequirePrefabPath && string.IsNullOrEmpty(path))
            {
                return new ErrorResponse("NEED_PREFAB_PATH", new
                {
                    instantiate = false,
                    note = "Pass prefabPath of this SKU. Project-wide token search is not identity."
                });
            }
            var token = VrcDccCommon.Param(p, "requireContains", "token", "");
            if (string.IsNullOrEmpty(token))
                token = VrcDccPolicy.BodyToken;
            token = (token ?? "").ToLowerInvariant();
            var hits = new List<object>();
            var tokenHits = 0;
            if (string.IsNullOrEmpty(path))
            {
                return new ErrorResponse("NEED_PREFAB_PATH", new
                {
                    instantiate = false,
                    note = "prefabPath required."
                });
            }
            var obj = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            if (obj == null) return new ErrorResponse("NO_PREFAB", new { path });
            var ok = string.IsNullOrEmpty(token) ||
                     obj.name.ToLowerInvariant().IndexOf(token) >= 0 ||
                     path.ToLowerInvariant().IndexOf(token) >= 0;
            if (ok) tokenHits++;
            hits.Add(new { path, name = obj.name, ok });
            var hipsY = -1f;
            var av = VrcDccCommon.FindAvatar(VrcDccCommon.AvatarName(p));
            if (av != null)
            {
                var anim = av.GetComponent<Animator>();
                var hips = anim != null ? anim.GetBoneTransform(HumanBodyBones.Hips) : null;
                if (hips != null) hipsY = hips.position.y;
            }
            if (tokenHits == 0)
            {
                return new ErrorResponse("NO_BODY_PREFAB", new
                {
                    token,
                    hits,
                    hipsY,
                    instantiate = false,
                    note = "wear_fusion / library row is not fitted. Do not Instantiate."
                });
            }
            float? expected = null;
            if (p != null && p["expectedHipsY"] != null)
                expected = p.Value<float>("expectedHipsY");
            else if (VrcDccPolicy.Current != null)
                expected = VrcDccPolicy.Current.expected_hips_y;
            if (expected != null && hipsY >= 0f)
            {
                var slack = VrcDccCommon.ParamFloat(p, "hipsSlack", VrcDccPolicy.Current != null ? VrcDccPolicy.Current.hips_slack : 0.05f);
                if (Mathf.Abs(hipsY - expected.Value) > slack)
                {
                    return new ErrorResponse("HIPS_Y_MISMATCH", new
                    {
                        token,
                        hipsY,
                        expected = expected.Value,
                        slack,
                        instantiate = false,
                        note = "Fusion hips are not the shop body. Do not Instantiate a generic SKU."
                    });
                }
            }
            return new SuccessResponse("vrc_prefab_identity", new
            {
                token,
                tokenHits,
                hipsY,
                instantiate = false,
                note = "Identity OK to consider. Still pose in Edit and dump vrc_pose_bounds before hang. Do not Instantiate from this tool.",
                hits
            });
        }
    }

    [McpForUnityTool("vrc_pose_bounds", Description = "BakeMesh centroid vs named Humanoid bone. dRH~0 at wrist is refuse. Dump every constraint source.", Group = "core")]
    public static class VrcPoseBoundsTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
            [ToolParameter("SkinnedMeshRenderer GameObject name.", Required = false)]
            public string renderer { get; set; }
            [ToolParameter("Humanoid bone name. Default RightHand.", Required = false, DefaultValue = "RightHand")]
            public string bone { get; set; }
            [ToolParameter("Max BakeMesh-centroid-to-bone distance.", Required = false, DefaultValue = "0.08")]
            public float? maxDistance { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            return VrcDccCommon.Run(() => HandlePose(p));
        }

        static object HandlePose(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var rendererName = VrcDccCommon.Param(p, "renderer", "mesh", "");
            var boneName = VrcDccCommon.Param(p, "bone", "humanBone", "RightHand");
            var maxDist = VrcDccCommon.ParamFloat(p, "maxDistance", 0.08f);
            var anim = av.GetComponent<Animator>();
            if (anim == null) return new ErrorResponse("NO_ANIMATOR");
            HumanBodyBones hb;
            if (!System.Enum.TryParse(boneName, true, out hb))
                hb = HumanBodyBones.RightHand;
            var bone = anim.GetBoneTransform(hb);
            if (bone == null) return new ErrorResponse("NO_BONE", new { bone = boneName });
            SkinnedMeshRenderer smr = null;
            if (!string.IsNullOrEmpty(rendererName))
            {
                var all = av.GetComponentsInChildren<SkinnedMeshRenderer>(true);
                for (var i = 0; i < all.Length; i++)
                {
                    if (all[i] != null && all[i].gameObject.name.IndexOf(rendererName) >= 0)
                    { smr = all[i]; break; }
                }
            }
            if (smr == null) return new ErrorResponse("NO_RENDERER", new { renderer = rendererName });
            var baked = new Mesh();
            smr.BakeMesh(baked);
            var verts = baked.vertices;
            UnityEngine.Object.DestroyImmediate(baked);
            if (verts == null || verts.Length == 0) return new ErrorResponse("EMPTY_MESH");
            var acc = Vector3.zero;
            for (var i = 0; i < verts.Length; i++) acc += smr.transform.TransformPoint(verts[i]);
            var centroid = acc / verts.Length;
            var dist = Vector3.Distance(centroid, bone.position);
            var handLocal = bone.InverseTransformPoint(centroid);
            var wristLike = hb == HumanBodyBones.RightHand || hb == HumanBodyBones.LeftHand;
            var refuseWrist = wristLike && dist < 0.04f && Mathf.Abs(handLocal.y) < 0.04f && Mathf.Abs(handLocal.z) < 0.05f;
            int nSrc;
            float maxW;
            var sources = DumpConstraints(smr.transform, out nSrc, out maxW);
            var ok = dist <= maxDist && !refuseWrist;
            var data = new
            {
                renderer = VrcDccCommon.PathOf(smr.transform),
                bone = bone.name,
                humanBone = hb.ToString(),
                centroid = V3(centroid),
                bonePos = V3(bone.position),
                dist = Mathf.Round(dist * 1000f) / 1000f,
                handLocal = V3(handLocal),
                aabbCenter = V3(smr.bounds.center),
                aabbNote = "Do not use renderer.bounds as fit. This tool uses BakeMesh.",
                refuseWrist,
                nSrc,
                maxW,
                constraintSources = sources,
                ok,
                fitted = false
            };
            if (nSrc > 0 && maxW < 0.01f)
                return new ErrorResponse("ZERO_WEIGHT_CONSTRAINT", data);
            if (!ok)
                return new ErrorResponse(refuseWrist ? "WRIST_NOT_GRIP" : "BOUNDS_FAR", data);
            return new SuccessResponse("vrc_pose_bounds", data);
        }

        static string V3(Vector3 v)
        {
            return (Mathf.Round(v.x * 1000f) / 1000f) + "," +
                   (Mathf.Round(v.y * 1000f) / 1000f) + "," +
                   (Mathf.Round(v.z * 1000f) / 1000f);
        }

        static List<object> DumpConstraints(Transform start, out int nSrc, out float maxW)
        {
            var rows = new List<object>();
            nSrc = 0;
            maxW = 0f;
            var t = start;
            while (t != null)
            {
                var comps = t.GetComponents<Component>();
                for (var i = 0; i < comps.Length; i++)
                {
                    if (comps[i] == null) continue;
                    var tn = comps[i].GetType().Name;
                    if (tn.IndexOf("ParentConstraint") < 0) continue;
                    var src = ReadConstraintSources(comps[i], ref nSrc, ref maxW);
                    var so = new SerializedObject(comps[i]);
                    so.Update();
                    var locked = so.FindProperty("Locked") ?? so.FindProperty("m_Locked");
                    var active = so.FindProperty("IsActive") ?? so.FindProperty("m_IsActive") ?? so.FindProperty("m_Active");
                    rows.Add(new
                    {
                        host = VrcDccCommon.PathOf(t),
                        type = tn,
                        locked = locked != null && locked.boolValue ? 1 : 0,
                        active = active != null && active.boolValue ? 1 : 0,
                        src
                    });
                }
                t = t.parent;
            }
            return rows;
        }

        static List<object> ReadConstraintSources(Component c, ref int nSrc, ref float maxW)
        {
            var src = new List<object>();
            var sourcesProp = c.GetType().GetProperty("Sources");
            if (sourcesProp != null)
            {
                var list = sourcesProp.GetValue(c, null) as System.Collections.IList;
                if (list != null)
                {
                    var n = list.Count > 8 ? 8 : list.Count;
                    for (var si = 0; si < n; si++)
                    {
                        var item = list[si];
                        if (item == null) continue;
                        var it = item.GetType();
                        var stProp = it.GetProperty("SourceTransform") ?? it.GetProperty("sourceTransform");
                        var wProp = it.GetProperty("Weight") ?? it.GetProperty("weight");
                        var st = stProp != null ? stProp.GetValue(item, null) as Transform : null;
                        var w = wProp != null ? Convert.ToSingle(wProp.GetValue(item, null)) : 0f;
                        nSrc++;
                        if (w > maxW) maxW = w;
                        src.Add(new { i = si, n = st != null ? st.name : "", wp = st != null ? V3(st.position) : "", w = Mathf.Round(w * 1000f) / 1000f });
                    }
                    if (src.Count > 0) return src;
                }
            }
            var ic = c as UnityEngine.Animations.IConstraint;
            if (ic != null)
            {
                var n = ic.sourceCount > 8 ? 8 : ic.sourceCount;
                for (var si = 0; si < n; si++)
                {
                    var s = ic.GetSource(si);
                    nSrc++;
                    if (s.weight > maxW) maxW = s.weight;
                    var st = s.sourceTransform;
                    src.Add(new { i = si, n = st != null ? st.name : "", wp = st != null ? V3(st.position) : "", w = Mathf.Round(s.weight * 1000f) / 1000f });
                }
                if (src.Count > 0) return src;
            }
            var so = new SerializedObject(c);
            so.Update();
            var sources = so.FindProperty("Sources") ?? so.FindProperty("m_Sources");
            if (sources != null && sources.isArray)
            {
                var n = sources.arraySize > 8 ? 8 : sources.arraySize;
                for (var si = 0; si < n; si++)
                {
                    var el = sources.GetArrayElementAtIndex(si);
                    var tf = el.FindPropertyRelative("SourceTransform") ?? el.FindPropertyRelative("sourceTransform") ?? el.FindPropertyRelative("m_SourceTransform");
                    var w = el.FindPropertyRelative("Weight") ?? el.FindPropertyRelative("weight") ?? el.FindPropertyRelative("m_Weight");
                    var st = tf != null ? tf.objectReferenceValue as Transform : null;
                    var wv = w != null ? w.floatValue : 0f;
                    nSrc++;
                    if (wv > maxW) maxW = wv;
                    src.Add(new { i = si, n = st != null ? st.name : "", wp = st != null ? V3(st.position) : "", w = Mathf.Round(wv * 1000f) / 1000f });
                }
            }
            return src;
        }
    }

    [McpForUnityTool("vrc_leftover_menu", Description = "MenuItem / ObjectToggle / MA param leftovers after Owner hand-delete (POLICY leftover_needles).", Group = "core")]
    public static class VrcLeftoverMenuTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
            [ToolParameter("Menu leftover name needle. Empty = POLICY leftover_needles.", Required = false)]
            public string needle { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            return VrcDccCommon.Run(() => HandleLeftover(p));
        }

        static object HandleLeftover(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var paramNeedle = VrcDccCommon.Param(p, "needle", "name", "");
            var needles = string.IsNullOrEmpty(paramNeedle)
                ? VrcDccPolicy.LeftoverNeedles
                : new[] { paramNeedle };
            var miHits = 0;
            var paramHits = 0;
            var otMiss = 0;
            var names = new List<string>();
            var mis = av.GetComponentsInChildren<ModularAvatarMenuItem>(true);
            for (var i = 0; i < mis.Length; i++)
            {
                var mi = mis[i];
                if (mi == null) continue;
                var pn = mi.Control != null && mi.Control.parameter != null ? mi.Control.parameter.name : "";
                var lab = !string.IsNullOrEmpty(mi.label) ? mi.label : mi.gameObject.name;
                var path = VrcDccCommon.PathOf(mi.transform);
                if (!VrcDccCommon.NeedleHit(pn, needles) &&
                    !VrcDccCommon.NeedleHit(lab, needles) &&
                    !VrcDccCommon.NeedleHit(path, needles))
                    continue;
                miHits++;
                if (names.Count < 24) names.Add(path + " p=" + pn);
            }
            var pars = av.GetComponentsInChildren<ModularAvatarParameters>(true);
            for (var i = 0; i < pars.Length; i++)
            {
                if (pars[i] == null || pars[i].parameters == null) continue;
                for (var j = 0; j < pars[i].parameters.Count; j++)
                {
                    var pn = pars[i].parameters[j].nameOrPrefix ?? "";
                    if (VrcDccCommon.NeedleHit(pn, needles)) paramHits++;
                }
            }
            var ots = av.GetComponentsInChildren<ModularAvatarObjectToggle>(true);
            for (var i = 0; i < ots.Length; i++)
            {
                if (ots[i] == null || ots[i].Objects == null) continue;
                for (var j = 0; j < ots[i].Objects.Count; j++)
                {
                    var ent = ots[i].Objects[j];
                    var rp = ent.Object != null ? ent.Object.referencePath : "";
                    var tgt = ent.Object != null ? ent.Object.Get(ots[i]) : null;
                    if (tgt == null && VrcDccCommon.NeedleHit(rp, needles))
                        otMiss++;
                }
            }
            var ok = miHits == 0 && paramHits == 0 && otMiss == 0;
            var data = new { needles, miHits, paramHits, otMiss, names, ok };
            if (!ok) return new ErrorResponse("LEFTOVER_MENU", data);
            return new SuccessResponse("vrc_leftover_menu", data);
        }
    }
}

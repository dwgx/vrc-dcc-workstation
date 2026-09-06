using System;
using System.Collections.Generic;
using MCPForUnity.Editor.Helpers;
using Newtonsoft.Json.Linq;
using UnityEngine;

namespace VrcDcc.Tools.Editor
{
    internal static class VrcDccCommon
    {
        public const string AvatarParamHelp = "Avatar root GameObject name. Empty = POLICY unity_root_name. Never the first VRCAvatarDescriptor in the scene.";

        public static string AvatarName(JObject p)
        {
            if (p != null)
            {
                var t = p.Value<string>("avatar") ?? p.Value<string>("root");
                if (!string.IsNullOrEmpty(t))
                    return t;
            }
            var fromPolicy = VrcDccPolicy.RootName;
            if (!string.IsNullOrEmpty(fromPolicy))
                return fromPolicy;
            return "";
        }

        public static GameObject FindAvatar(string name)
        {
            if (string.IsNullOrEmpty(name))
                name = VrcDccPolicy.RootName;
            if (string.IsNullOrEmpty(name))
                return null;
            var hits = VrcDccIdentity.FindExactName(name);
            if (hits.Count == 1)
                return hits[0];
            return null;
        }

        public static object NeedAvatar(JObject p, out GameObject av)
        {
            av = null;
            if (VrcDccPolicy.IsInvalid)
                return new ErrorResponse("POLICY_INVALID", new { error = VrcDccPolicy.InvalidReason });
            var name = AvatarName(p);
            if (string.IsNullOrEmpty(name))
                return new ErrorResponse("NO_AVATAR_IDENTITY", new { hint = "Set POLICY unity_root_name or pass avatar=" });
            var hits = VrcDccIdentity.FindExactName(name);
            if (hits.Count == 0)
                return new ErrorResponse("NO_AVATAR", new { avatar = name });
            if (hits.Count > 1)
                return new ErrorResponse("AMBIGUOUS_AVATAR", new
                {
                    avatar = name,
                    n = hits.Count,
                    paths = VrcDccIdentity.Paths(hits, 8)
                });
            av = hits[0];
            return null;
        }

        public static string PathOf(Transform t)
        {
            if (t == null) return "";
            var p = t.name;
            while (t.parent != null)
            {
                t = t.parent;
                p = t.name + "/" + p;
            }
            return p;
        }

        public static string Param(JObject p, string a, string b, string fallback = "")
        {
            if (p == null) return fallback;
            var v = p.Value<string>(a) ?? p.Value<string>(b);
            return string.IsNullOrEmpty(v) ? fallback : v;
        }

        public static float ParamFloat(JObject p, string name, float fallback)
        {
            if (p == null || p[name] == null) return fallback;
            return p.Value<float>(name);
        }

        public static bool TypeNameContains(Component c, string needle)
        {
            return c != null && c.GetType().Name.IndexOf(needle) >= 0;
        }

        public static void CollectParamsByTypeName(GameObject av, string typeNeedle, string field, HashSet<string> into)
        {
            var mbs = av.GetComponentsInChildren<MonoBehaviour>(true);
            for (var i = 0; i < mbs.Length; i++)
            {
                var mb = mbs[i];
                if (mb == null || mb.GetType().Name.IndexOf(typeNeedle) < 0) continue;
                var so = new UnityEditor.SerializedObject(mb);
                var prop = so.FindProperty(field);
                if (prop != null && !string.IsNullOrEmpty(prop.stringValue))
                    into.Add(prop.stringValue);
            }
        }

        public static bool NeedleHit(string hay, string[] needles)
        {
            if (string.IsNullOrEmpty(hay) || needles == null) return false;
            for (var i = 0; i < needles.Length; i++)
            {
                var n = needles[i];
                if (!string.IsNullOrEmpty(n) && hay.IndexOf(n) >= 0)
                    return true;
            }
            return false;
        }

        public static object Run(Func<object> fn)
        {
            try
            {
                return fn();
            }
            catch (Exception ex)
            {
                return new ErrorResponse(ex.GetType().Name, new { error = ex.Message });
            }
        }
    }
}

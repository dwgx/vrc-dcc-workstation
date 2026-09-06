using System;
using System.Collections.Generic;
using MCPForUnity.Editor.Helpers;
using Newtonsoft.Json.Linq;
using UnityEngine;
using VRC.SDK3.Avatars.Components;

namespace VrcDcc.Tools.Editor
{
    internal static class VrcDccCommon
    {
        public const string AvatarParamHelp = "Avatar root GameObject name. Empty = POLICY unity_root_name, else first VRCAvatarDescriptor.";

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
            if (!string.IsNullOrEmpty(name))
            {
                var found = GameObject.Find(name);
                if (found != null) return found;
                var all = UnityEngine.Object.FindObjectsOfType<Transform>(true);
                for (var i = 0; i < all.Length; i++)
                {
                    if (all[i] != null && all[i].name == name && all[i].parent == null)
                        return all[i].gameObject;
                }
                for (var i = 0; i < all.Length; i++)
                {
                    if (all[i] != null && all[i].name == name)
                        return all[i].gameObject;
                }
            }
            var descs = UnityEngine.Object.FindObjectsOfType<VRCAvatarDescriptor>(true);
            if (descs != null && descs.Length > 0 && descs[0] != null)
                return descs[0].gameObject;
            return null;
        }

        public static object NeedAvatar(JObject p, out GameObject av)
        {
            av = FindAvatar(AvatarName(p));
            if (av == null)
                return new ErrorResponse("NO_AVATAR", new { avatar = AvatarName(p) });
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

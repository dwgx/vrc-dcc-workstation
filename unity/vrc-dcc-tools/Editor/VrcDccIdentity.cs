using System.Collections.Generic;
using UnityEngine;

namespace VrcDcc.Tools.Editor
{
    /// <summary>
    /// Fail-closed identity. Zero candidates = not applicable. Two+ = ambiguous.
    /// Never return the first of many.
    /// </summary>
    internal static class VrcDccIdentity
    {
        public const string Ok = "ok";
        public const string NotApplicable = "not_applicable";
        public const string Ambiguous = "ambiguous";
        public const string MissingPath = "missing_policy_path";
        public const string BadPolicy = "bad_policy";

        public struct Pick
        {
            public string status;
            public Transform transform;
            public string path;
            public string[] candidates;
            public string wanted;
        }

        public static List<GameObject> FindExactName(string name)
        {
            var hits = new List<GameObject>();
            if (string.IsNullOrEmpty(name)) return hits;
            var all = Object.FindObjectsOfType<Transform>(true);
            for (var i = 0; i < all.Length; i++)
            {
                var t = all[i];
                if (t == null || t.name != name) continue;
                var go = t.gameObject;
                if (go == null) continue;
                var dup = false;
                for (var j = 0; j < hits.Count; j++)
                {
                    if (hits[j] == go) { dup = true; break; }
                }
                if (!dup) hits.Add(go);
            }
            return hits;
        }

        public static string[] Paths(List<GameObject> gos, int cap)
        {
            var n = gos == null ? 0 : gos.Count;
            if (n > cap) n = cap;
            var rows = new string[n];
            for (var i = 0; i < n; i++)
                rows[i] = VrcDccCommon.PathOf(gos[i] != null ? gos[i].transform : null);
            return rows;
        }

        public static Transform FindRelative(Transform root, string relative)
        {
            if (root == null || string.IsNullOrEmpty(relative)) return null;
            var p = relative.Replace('\\', '/').Trim().Trim('/');
            if (p.Length == 0) return null;
            if (p == root.name) return root;
            var prefix = root.name + "/";
            if (p.StartsWith(prefix))
                p = p.Substring(prefix.Length);
            return root.Find(p);
        }

        public static Pick UniqueTransform(Transform root, string explicitPath, List<Transform> discovered)
        {
            var cand = new List<string>();
            if (discovered != null)
            {
                for (var i = 0; i < discovered.Count; i++)
                {
                    if (discovered[i] == null) continue;
                    cand.Add(VrcDccCommon.PathOf(discovered[i]));
                }
            }
            if (!string.IsNullOrEmpty(explicitPath))
            {
                var wanted = explicitPath.Trim();
                if (wanted.Length == 0)
                    return Result(BadPolicy, null, cand, explicitPath);
                var t = FindRelative(root, wanted);
                if (t == null)
                    return Result(MissingPath, null, cand, wanted);
                return Result(Ok, t, new List<string> { VrcDccCommon.PathOf(t) }, wanted);
            }
            if (discovered == null || discovered.Count == 0)
                return Result(NotApplicable, null, cand, null);
            if (discovered.Count > 1)
                return Result(Ambiguous, null, cand, null);
            return Result(Ok, discovered[0], cand, null);
        }

        static Pick Result(string status, Transform t, List<string> cand, string wanted)
        {
            var cap = cand.Count > 8 ? 8 : cand.Count;
            var rows = new string[cap];
            for (var i = 0; i < cap; i++) rows[i] = cand[i];
            return new Pick
            {
                status = status,
                transform = t,
                path = t != null ? VrcDccCommon.PathOf(t) : "",
                candidates = rows,
                wanted = wanted ?? ""
            };
        }

        public static List<Transform> NippleSmrs(Transform av)
        {
            var hits = new List<Transform>();
            if (av == null) return hits;
            var smrs = av.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            for (var i = 0; i < smrs.Length; i++)
            {
                var smr = smrs[i];
                if (smr == null || smr.sharedMesh == null) continue;
                var mesh = smr.sharedMesh;
                var ok = false;
                for (var si = 0; si < mesh.blendShapeCount; si++)
                {
                    if (mesh.GetBlendShapeName(si).IndexOf("Nipple_") >= 0)
                    {
                        ok = true;
                        break;
                    }
                }
                if (ok) hits.Add(smr.transform);
            }
            return hits;
        }

        public static List<Transform> GogoRoots(Transform av)
        {
            var hits = new List<Transform>();
            if (av == null) return hits;
            var trs = av.GetComponentsInChildren<Transform>(true);
            for (var i = 0; i < trs.Length; i++)
            {
                var tr = trs[i];
                if (tr != null && tr.name.IndexOf("GogoLoco") >= 0)
                    hits.Add(tr);
            }
            return hits;
        }
    }
}

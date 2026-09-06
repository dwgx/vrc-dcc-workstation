using System;
using System.IO;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;

namespace VrcDcc.Tools.Editor
{
    [Serializable]
    internal sealed class VrcDccPolicyData
    {
        public int schema = 1;
        public string avatar = "";
        public string unity_root_name = "";
        public string body_token = "";
        public bool require_prefab_path = true;
        public string[] disable_mcp_tools = { "execute_code" };
        public string[] leftover_needles = Array.Empty<string>();
        public float? expected_hips_y;
        public float hips_slack = 0.05f;
        public int sku_quota = 1;
    }

    [InitializeOnLoad]
    internal static class VrcDccPolicy
    {
        const string PrefPrefix = "MCPForUnity.ToolEnabled.";
        static VrcDccPolicyData _cached;
        static string _cachedPath = "";

        static VrcDccPolicy()
        {
            EditorApplication.delayCall += ApplyDisabledTools;
            AssemblyReloadEvents.afterAssemblyReload += ApplyDisabledTools;
            EditorApplication.playModeStateChanged += OnPlayMode;
        }

        static void OnPlayMode(PlayModeStateChange state)
        {
            if (state == PlayModeStateChange.EnteredEditMode)
                ApplyDisabledTools();
        }

        public static VrcDccPolicyData Current
        {
            get
            {
                Load();
                return _cached;
            }
        }

        public static string RootName
        {
            get
            {
                var n = Current != null ? Current.unity_root_name : "";
                return string.IsNullOrEmpty(n) ? "" : n;
            }
        }

        public static string BodyToken
        {
            get
            {
                var n = Current != null ? Current.body_token : "";
                return n ?? "";
            }
        }

        public static bool RequirePrefabPath
        {
            get { return Current == null || Current.require_prefab_path; }
        }

        public static string[] LeftoverNeedles
        {
            get
            {
                var n = Current != null ? Current.leftover_needles : null;
                if (n == null || n.Length == 0)
                    return Array.Empty<string>();
                return n;
            }
        }

        public static VrcDccPolicyData Load()
        {
            var path = ResolvePath();
            if (_cached != null && path == _cachedPath)
                return _cached;
            _cachedPath = path;
            if (string.IsNullOrEmpty(path) || !File.Exists(path))
            {
                _cached = new VrcDccPolicyData();
                return _cached;
            }
            try
            {
                var raw = File.ReadAllText(path);
                var obj = JObject.Parse(raw);
                _cached = obj.ToObject<VrcDccPolicyData>() ?? new VrcDccPolicyData();
            }
            catch (Exception ex)
            {
                Debug.LogWarning("[vrc-dcc] POLICY.json parse failed: " + ex.Message);
                _cached = new VrcDccPolicyData();
            }
            return _cached;
        }

        public static void ApplyDisabledTools()
        {
            var data = Load();
            var tools = data != null ? data.disable_mcp_tools : null;
            if (tools == null || tools.Length == 0)
                return;
            for (var i = 0; i < tools.Length; i++)
            {
                var name = tools[i];
                if (string.IsNullOrEmpty(name))
                    continue;
                EditorPrefs.SetBool(PrefPrefix + name, false);
            }
        }

        static string ResolvePath()
        {
            var data = Application.dataPath;
            if (string.IsNullOrEmpty(data))
                return "";
            var overlay = Path.Combine(data, "VrcDcc", "POLICY.json");
            if (File.Exists(overlay))
                return overlay;
            var pkg = Path.GetFullPath(Path.Combine(data, "..", "Packages", "com.vrc-dcc.tools", "POLICY.default.json"));
            if (File.Exists(pkg))
                return pkg;
            return "";
        }
    }
}

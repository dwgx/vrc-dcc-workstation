using System.Globalization;
using MCPForUnity.Editor.Helpers;
using MCPForUnity.Editor.Tools;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;
using VRC.SDK3.Avatars.Components;
using VRC.SDK3.Avatars.ScriptableObjects;
using nadena.dev.modular_avatar.core;

namespace VrcDcc.Tools.Editor
{
    [McpForUnityTool("vrc_audit", Description = "Edit-only avatar audit JSON (bits, missOT, nipples, GoGo Base). Do not invent execute_code.", Group = "core")]
    public static class VrcAuditTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var desc = av.GetComponent<VRCAvatarDescriptor>();
            var edit = desc != null ? desc.expressionParameters : null;
            var editBits = edit != null ? edit.CalcTotalCost() : -1;
            var editN = edit != null && edit.parameters != null ? edit.parameters.Length : -1;
            var vfOnSource = 0;
            if (edit != null && edit.parameters != null)
            {
                for (var i = 0; i < edit.parameters.Length; i++)
                {
                    var n = edit.parameters[i] != null ? edit.parameters[i].name : null;
                    if (n != null && n.StartsWith("VF")) vfOnSource++;
                }
            }
            var bakePath = "Packages/com.vrcfury.temp/Builds/" + av.name + "/VRCFury Params.asset";
            var bake = AssetDatabase.LoadAssetAtPath<VRCExpressionParameters>(bakePath);
            var bakeBits = -1;
            var bakeN = -1;
            var bakeInt = 0;
            var bakeBool = 0;
            if (bake != null && bake.parameters != null)
            {
                bakeBits = bake.CalcTotalCost();
                bakeN = bake.parameters.Length;
                for (var i = 0; i < bake.parameters.Length; i++)
                {
                    var bp = bake.parameters[i];
                    if (bp == null || !bp.networkSynced) continue;
                    if (bp.valueType == VRCExpressionParameters.ValueType.Bool) bakeBool++;
                    else bakeInt++;
                }
            }
            var missOT = 0;
            var menuItems = 0;
            var enabledSyncedMI = 0;
            var cutterOnMenu = 0;
            var mis = av.GetComponentsInChildren<ModularAvatarMenuItem>(true);
            for (var i = 0; i < mis.Length; i++)
            {
                if (mis[i] == null) continue;
                menuItems++;
                if (mis[i].isSynced && mis[i].gameObject.activeInHierarchy) enabledSyncedMI++;
                var mbs = mis[i].GetComponents<MonoBehaviour>();
                for (var c = 0; c < mbs.Length; c++)
                {
                    if (VrcDccCommon.TypeNameContains(mbs[c], "MeshCutter") ||
                        VrcDccCommon.TypeNameContains(mbs[c], "VertexFilter"))
                        cutterOnMenu++;
                }
            }
            var ots = av.GetComponentsInChildren<ModularAvatarObjectToggle>(true);
            for (var i = 0; i < ots.Length; i++)
            {
                if (ots[i] == null || ots[i].Objects == null) continue;
                for (var j = 0; j < ots[i].Objects.Count; j++)
                {
                    var ent = ots[i].Objects[j];
                    if (ent.Object == null) { missOT++; continue; }
                    if (ent.Object.Get(ots[i]) == null) missOT++;
                }
            }
            float nipOn = -1f, nipUp = -1f, nipSmall = -1f;
            var bodySmr = FindNippleMesh(av.transform);
            if (bodySmr != null && bodySmr.sharedMesh != null)
            {
                var mesh = bodySmr.sharedMesh;
                for (var si = 0; si < mesh.blendShapeCount; si++)
                {
                    var n = mesh.GetBlendShapeName(si);
                    if (n.IndexOf("Nipple_On") >= 0) nipOn = bodySmr.GetBlendShapeWeight(si);
                    else if (n.IndexOf("Nipple_Up") >= 0) nipUp = bodySmr.GetBlendShapeWeight(si);
                    else if (n.IndexOf("Nipple_Small") >= 0) nipSmall = bodySmr.GetBlendShapeWeight(si);
                }
            }
            var gogo = FindGoGoRoot(av.transform);
            var gogoBaseOn = 0;
            var gogoBaseMode = -1;
            if (gogo != null)
            {
                var mas = gogo.GetComponents<ModularAvatarMergeAnimator>();
                for (var gi = 0; gi < mas.Length; gi++)
                {
                    if (mas[gi] == null) continue;
                    if ((int)mas[gi].layerType != 0) continue;
                    gogoBaseOn = mas[gi].enabled ? 1 : 0;
                    gogoBaseMode = (int)mas[gi].mergeAnimatorMode;
                }
            }
            var inv = CultureInfo.InvariantCulture;
            var motchiri = AssetDatabase.LoadAssetAtPath<UnityEngine.Object>(
                "Assets/\u529F\u80FD/motchiri_shader/Prefab_FX/motchiri_shader.prefab");
            var data = new
            {
                avatar = av.name,
                playing = EditorApplication.isPlaying ? 1 : 0,
                editBits,
                editN,
                vfOnSource,
                bakeBits,
                bakeN,
                bakeInt,
                bakeBool,
                menuItems,
                enabledSyncedMI,
                missOT,
                cutterOnMenu,
                nippleOn = nipOn.ToString(inv),
                nippleUp = nipUp.ToString(inv),
                nippleSmall = nipSmall.ToString(inv),
                audio = av.GetComponentsInChildren<AudioSource>(true).Length,
                physbones = CountType(av, "VRCPhysBone"),
                lights = av.GetComponentsInChildren<Light>(true).Length,
                smr = av.GetComponentsInChildren<SkinnedMeshRenderer>(true).Length,
                motchiriFx = motchiri == null ? 0 : 1,
                gogoPresent = gogo == null ? 0 : 1,
                gogoBaseOn,
                gogoBaseMode,
                abtPresent = av.transform.Find("ABT") == null ? 0 : 1,
                fitted = false,
                note = "Wiring dump. isSynced=0 is not fitted. Owner Edit look still required."
            };
            if (EditorApplication.isPlaying)
                return new ErrorResponse("PLAYING", data);
            if (desc == null)
                return new ErrorResponse("NO_DESC", data);
            if (missOT > 0)
                return new ErrorResponse("MISS_OT", data);
            return new SuccessResponse("vrc_audit", data);
        }

        static SkinnedMeshRenderer FindNippleMesh(Transform av)
        {
            var named = av.Find("Body_b");
            if (named != null)
            {
                var smr = named.GetComponent<SkinnedMeshRenderer>();
                if (smr != null && smr.sharedMesh != null) return smr;
            }
            var smrs = av.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            for (var i = 0; i < smrs.Length; i++)
            {
                var smr = smrs[i];
                if (smr == null || smr.sharedMesh == null) continue;
                var mesh = smr.sharedMesh;
                for (var si = 0; si < mesh.blendShapeCount; si++)
                {
                    if (mesh.GetBlendShapeName(si).IndexOf("Nipple_") >= 0)
                        return smr;
                }
            }
            return null;
        }

        static Transform FindGoGoRoot(Transform av)
        {
            var t = av.Find("功能/GogoLoco All (Modular Avatar)") ?? av.Find("功能/GogoLoco All");
            if (t != null) return t;
            var trs = av.GetComponentsInChildren<Transform>(true);
            for (var i = 0; i < trs.Length; i++)
            {
                var tr = trs[i];
                if (tr != null && tr.name.IndexOf("GogoLoco") >= 0)
                    return tr;
            }
            return null;
        }

        static int CountType(GameObject av, string needle)
        {
            var n = 0;
            var mbs = av.GetComponentsInChildren<MonoBehaviour>(true);
            for (var i = 0; i < mbs.Length; i++)
                if (VrcDccCommon.TypeNameContains(mbs[i], needle)) n++;
            return n;
        }
    }

    [McpForUnityTool("vrc_ma_wiring", Description = "Every MergeAnimator enabled/mode/layer. Disabled Replace still bakes.", Group = "core")]
    public static class VrcMaWiringTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var mas = av.GetComponentsInChildren<ModularAvatarMergeAnimator>(true);
            var rows = new object[mas.Length];
            for (var i = 0; i < mas.Length; i++)
            {
                var ma = mas[i];
                rows[i] = new
                {
                    path = VrcDccCommon.PathOf(ma.transform),
                    en = ma.enabled ? 1 : 0,
                    layer = (int)ma.layerType,
                    mode = (int)ma.mergeAnimatorMode,
                    anim = ma.animator != null ? ma.animator.name : "",
                    goActive = ma.gameObject.activeInHierarchy ? 1 : 0
                };
            }
            var sw = 0;
            var mbs = av.GetComponentsInChildren<MonoBehaviour>(true);
            for (var i = 0; i < mbs.Length; i++)
                if (VrcDccCommon.TypeNameContains(mbs[i], "VrcDccLocoSwitch")) sw = 1;
            return new SuccessResponse("vrc_ma_wiring", new { n = mas.Length, rows, locoSwitch = sw });
        }
    }

    [McpForUnityTool("vrc_ot_inventory", Description = "ObjectToggle miss via AvatarObjectReference.Get; want vs live activeSelf.", Group = "core")]
    public static class VrcOtInventoryTool
    {
        public class Parameters
        {
            [ToolParameter(VrcDccCommon.AvatarParamHelp, Required = false)]
            public string avatar { get; set; }
        }

        public static object HandleCommand(JObject p)
        {
            var err = VrcDccCommon.NeedAvatar(p, out var av);
            if (err != null) return err;
            var ots = av.GetComponentsInChildren<ModularAvatarObjectToggle>(true);
            var miss = 0;
            var nEnt = 0;
            var rows = new System.Collections.Generic.List<object>();
            for (var i = 0; i < ots.Length; i++)
            {
                var ot = ots[i];
                if (ot == null || ot.Objects == null) continue;
                var param = "";
                var mi = ot.GetComponent<ModularAvatarMenuItem>();
                if (mi != null && mi.Control != null && mi.Control.parameter != null)
                    param = mi.Control.parameter.name;
                for (var j = 0; j < ot.Objects.Count; j++)
                {
                    nEnt++;
                    var ent = ot.Objects[j];
                    GameObject go = null;
                    var isMiss = 0;
                    if (ent.Object == null) { isMiss = 1; miss++; }
                    else
                    {
                        go = ent.Object.Get(ot);
                        if (go == null) { isMiss = 1; miss++; }
                    }
                    if (rows.Count >= 36) continue;
                    rows.Add(new
                    {
                        host = VrcDccCommon.PathOf(ot.transform),
                        param,
                        tgt = go == null ? "" : VrcDccCommon.PathOf(go.transform),
                        want = ent.Active ? 1 : 0,
                        now = go != null && go.activeSelf ? 1 : 0,
                        miss = isMiss
                    });
                }
            }
            return new SuccessResponse("vrc_ot_inventory", new { ot = ots.Length, entries = nEnt, miss, shown = rows.Count, rows });
        }
    }
}

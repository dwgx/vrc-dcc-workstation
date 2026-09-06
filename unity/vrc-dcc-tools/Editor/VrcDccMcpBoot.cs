#if VRC_DCC_MCP
using System;
using System.Threading.Tasks;
using MCPForUnity.Editor.Services;
using MCPForUnity.Editor.Services.Transport;
using UnityEditor;
using UnityEngine;

namespace VrcDcc.Tools.Editor
{
    /// <summary>
    /// Start CoplayDev HTTP on 8080 and connect the Editor websocket so named
    /// vrc_* tools register. Quiet: no DisplayDialog. Skip Configure All.
    /// Do not call StartLocalHttpServer when 8080 is already reachable — that
    /// API stops the existing process first.
    /// </summary>
    [InitializeOnLoad]
    internal static class VrcDccMcpBoot
    {
        static VrcDccMcpBoot()
        {
            EditorApplication.delayCall += () => { _ = StartAndConnect(); };
        }

        static async Task StartAndConnect()
        {
            try
            {
                var server = MCPServiceLocator.Server;
                if (!server.IsLocalHttpServerReachable())
                {
                    if (!server.StartLocalHttpServer(quiet: true))
                    {
                        Debug.LogWarning("[vrc-dcc] MCP HTTP start failed");
                        return;
                    }

                    for (var i = 0; i < 40; i++)
                    {
                        if (server.IsLocalHttpServerReachable())
                            break;
                        await Task.Delay(250);
                    }
                }

                if (MCPServiceLocator.TransportManager.IsRunning(TransportMode.Http))
                    return;

                var ok = await MCPServiceLocator.Bridge.StartAsync();
                if (!ok)
                    Debug.LogWarning("[vrc-dcc] MCP bridge connect failed");
            }
            catch (Exception ex)
            {
                Debug.LogWarning("[vrc-dcc] MCP HTTP/bridge: " + ex.Message);
            }
        }
    }
}
#endif

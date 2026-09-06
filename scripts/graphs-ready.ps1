#Requires -Version 5.1
<#
.SYNOPSIS
  Handshake for the three graphs (clothes / USB / C#). ASCII only.
  Does not init an avatar Unity tree. Does not write the product project.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Continue'
$station = Split-Path -Parent $PSScriptRoot
$homeDir = [Environment]::GetFolderPath('UserProfile')
$router = Join-Path $station 'maps\GRAPHS.md'
$unityProject = ''
$loc = Join-Path $station 'local.json'
if (Test-Path -LiteralPath $loc) {
    try {
        $locObj = Get-Content -LiteralPath $loc -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($locObj.unity_project) { $unityProject = [string]$locObj.unity_project }
    } catch { }
}

Write-Output 'graphs-ready 1.1'
Write-Output "router: $router"
$cli = 'missing'
try {
    $v = (codegraph version 2>$null | Select-Object -First 1)
    if ($v) { $cli = $v.ToString().Trim() }
} catch { }
Write-Output "cli: $cli"
Write-Output ('station_index: ' + $(if (Test-Path -LiteralPath (Join-Path $station '.codegraph')) { 'yes' } else { 'no' }))
if ([string]::IsNullOrWhiteSpace($unityProject)) {
    Write-Output 'avatar_index: unset (local.json unity_project empty)'
    Write-Output 'avatar_codegraph_json: unset'
} else {
    Write-Output ('avatar_index: ' + $(if (Test-Path -LiteralPath (Join-Path $unityProject '.codegraph')) { 'yes' } else { 'no' }))
    Write-Output ('avatar_codegraph_json: ' + $(if (Test-Path -LiteralPath (Join-Path $unityProject 'codegraph.json')) { 'yes' } else { 'no' }))
}
$mcpJson = Join-Path $homeDir '.cursor\mcp.json'
$mcpState = 'missing'
if (Test-Path -LiteralPath $mcpJson) {
    $mcpRaw = Get-Content -LiteralPath $mcpJson -Raw -Encoding UTF8
    $wsFolder = '${' + 'workspaceFolder}'
    if ($mcpRaw.Contains($wsFolder)) { $mcpState = 'workspaceFolder' }
    elseif ($mcpRaw.Contains('"codegraph"')) { $mcpState = 'ok' }
    else { $mcpState = 'no-server' }
}
Write-Output "codegraph_mcp: $mcpState"
Write-Output "projectPath_station: $station"
Write-Output "projectPath_avatar: $(if ($unityProject) { $unityProject } else { 'unset' })"
Write-Output 'clothes: python maps/query.py <avatar> <words>'
Write-Output 'usb: python maps/query.py library <words>'
Write-Output 'csharp: codegraph_explore + projectPath (avatar Unity if avatar_index=yes else Read named .cs)'
Write-Output 'home: do not codegraph init / index the avatar Unity tree'
if ($mcpState -eq 'workspaceFolder') {
    Write-Output 'hint: codegraph MCP used --path workspaceFolder; prefer serve --mcp without that flag (owner overlay).'
}
exit 0

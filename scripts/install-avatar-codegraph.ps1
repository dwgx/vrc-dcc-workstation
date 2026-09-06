#Requires -Version 5.1
<#
.SYNOPSIS
  Copy templates/avatar-codegraph.json and init the C# index.
  Refuses home / station cwd. Must run from the avatar Unity project window.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$station = Split-Path -Parent $PSScriptRoot
$cwd = (Get-Location).Path

function Test-Under([string]$child, [string]$parent) {
    $c = $child.TrimEnd('\')
    $p = $parent.TrimEnd('\')
    return ($c.Equals($p, [StringComparison]::OrdinalIgnoreCase)) -or
        $c.StartsWith($p + '\', [StringComparison]::OrdinalIgnoreCase)
}

$homeDir = [Environment]::GetFolderPath('UserProfile')
$agentSystem = Join-Path $homeDir '.agent-system'
if (Test-Under $cwd $homeDir) {
    Write-Output 'install-avatar-codegraph: refuse. Home cwd must not write the Unity tree.'
    Write-Output "open a Cursor window at the avatar Unity project then: powershell -File $PSCommandPath"
    exit 2
}
if (Test-Under $cwd $agentSystem) {
    Write-Output 'install-avatar-codegraph: refuse. agent-system cwd must not write the Unity tree.'
    exit 2
}
if (Test-Under $cwd $station) {
    Write-Output 'install-avatar-codegraph: refuse. Station cwd must not write the Unity tree.'
    Write-Output 'open a Cursor window at the avatar Unity project then rerun this script.'
    exit 2
}
$assets = Join-Path $cwd 'Assets'
$manifest = Join-Path $cwd 'Packages\manifest.json'
if (-not (Test-Path -LiteralPath $assets) -or -not (Test-Path -LiteralPath $manifest)) {
    Write-Output 'install-avatar-codegraph: refuse. cwd is not a Unity project (need Assets/ and Packages/manifest.json).'
    exit 2
}

$src = Join-Path $station 'templates\avatar-codegraph.json'
$dst = Join-Path $cwd 'codegraph.json'
if (-not (Test-Path -LiteralPath $src)) { throw "missing $src" }
Copy-Item -LiteralPath $src -Destination $dst -Force
Write-Output "wrote $dst"
& codegraph init $cwd
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'install-avatar-codegraph: done. MCP codegraph_explore projectPath is this Unity root.'
exit 0

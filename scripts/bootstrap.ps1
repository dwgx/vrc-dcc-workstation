#Requires -Version 5.1
<#
.SYNOPSIS
  Probe the machine and optionally write gitignored local MCP JSON + local.json.
  Default dry-run. Does not edit user-global MCP. Does not write avatar project trees.
#>
[CmdletBinding()]
param(
    [string]$InstallRoot = '',
    [switch]$Apply,
    [switch]$CloneMcp
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($InstallRoot)) {
    $InstallRoot = Split-Path -Parent $PSScriptRoot
}

function Test-Exe([string]$Path) {
    return (-not [string]::IsNullOrWhiteSpace($Path)) -and (Test-Path -LiteralPath $Path)
}

function Find-UnityEditor {
    $hits = @()
    $roots = @(
        (Join-Path ${env:ProgramFiles} 'Unity\Hub\Editor'),
        (Join-Path ${env:ProgramFiles(x86)} 'Unity\Hub\Editor')
    )
    if (-not [string]::IsNullOrWhiteSpace($env:VRC_DCC_UNITY_HUB)) {
        $roots += $env:VRC_DCC_UNITY_HUB
    }
    foreach ($root in $roots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $exe = Join-Path $_.FullName 'Editor\Unity.exe'
            if (Test-Exe $exe) { $hits += $exe }
        }
    }
    return $hits
}

function Find-Blender {
    $hits = @()
    $cands = @(
        (Join-Path ${env:ProgramFiles} 'Blender Foundation\Blender 5.2\blender.exe'),
        (Join-Path ${env:ProgramFiles} 'Blender Foundation\Blender 5.2.1\blender.exe')
    )
    if (-not [string]::IsNullOrWhiteSpace($env:VRC_DCC_BLENDER)) {
        $cands += $env:VRC_DCC_BLENDER
    }
    foreach ($p in $cands) {
        if (Test-Exe $p) { $hits += $p }
    }
    return $hits
}

function Find-Uvx {
    $cmd = Get-Command uvx -ErrorAction SilentlyContinue
    if ($cmd) { return [string]$cmd.Source }
    $cands = @(
        (Join-Path $env:USERPROFILE '.local\bin\uvx.exe')
    )
    if (-not [string]::IsNullOrWhiteSpace($env:VRC_DCC_UVX)) {
        $cands += $env:VRC_DCC_UVX
    }
    foreach ($p in $cands) {
        if (Test-Exe $p) { return $p }
    }
    return ''
}

$template = Join-Path $InstallRoot 'mcp\cursor.mcp.json.template'
$outMcp = Join-Path $InstallRoot 'mcp\local.mcp.json'
$localExample = Join-Path $InstallRoot 'local.json.example'
$localJson = Join-Path $InstallRoot 'local.json'
$vendors = Join-Path $InstallRoot 'vendors\upstream'

$unityHits = @(Find-UnityEditor)
$blenderHits = @(Find-Blender)
$uvx = Find-Uvx

Write-Host "vrc-dcc-workstation bootstrap  root=$InstallRoot  apply=$Apply  clone=$CloneMcp"
Write-Host ("  [{0}] unity    {1}" -f $(if ($unityHits.Count) { 'OK' } else { 'MISSING' }), ($unityHits -join '; '))
Write-Host ("  [{0}] blender  {1}" -f $(if ($blenderHits.Count) { 'OK' } else { 'MISSING' }), ($blenderHits -join '; '))
Write-Host ("  [{0}] uvx      {1}" -f $(if ($uvx) { 'OK' } else { 'MISSING' }), $uvx)

if (-not $Apply) {
    Write-Host 'dry-run only. Re-run with -Apply to write mcp\local.mcp.json and local.json (if missing).'
    exit 0
}

if (-not (Test-Path -LiteralPath $template)) {
    throw "Missing template: $template"
}

$uvxForTpl = if ($uvx) { $uvx.Replace('\', '/') } else { 'uvx' }
$text = [System.IO.File]::ReadAllText($template)
$text = $text.Replace('{{UVX}}', $uvxForTpl)
New-Item -ItemType Directory -Force -Path (Split-Path $outMcp) | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($outMcp, $text, $utf8)
Write-Host "wrote $outMcp"

if (-not (Test-Path -LiteralPath $localJson)) {
    Copy-Item -LiteralPath $localExample -Destination $localJson
    $obj = Get-Content -LiteralPath $localJson -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($unityHits.Count) { $obj.unity_editor = $unityHits[0] }
    if ($blenderHits.Count) { $obj.blender_exe = $blenderHits[0] }
    if ($uvx) { $obj.uvx = $uvx }
    $json = $obj | ConvertTo-Json -Depth 6
    [System.IO.File]::WriteAllText($localJson, $json + [Environment]::NewLine, $utf8)
    Write-Host "wrote $localJson (fill unity_project if needed)"
} else {
    Write-Host "kept existing $localJson"
}

if ($CloneMcp) {
    New-Item -ItemType Directory -Force -Path $vendors | Out-Null
    $repos = @(
        @{ name = 'cats-blender-plugin-5.2'; url = 'https://github.com/Alrauna/Cats-Blender-Plugin.git'; tag = '' },
        @{ name = 'vrchat-agentic-tools'; url = 'https://github.com/gummidot/vrchat-agentic-tools.git'; tag = '' },
        @{ name = 'vrchat-avatar-modding-skill'; url = 'https://github.com/felixchaos/vrchat-avatar-modding-skill.git'; tag = '' }
    )
    foreach ($r in $repos) {
        $dest = Join-Path $vendors $r.name
        if (Test-Path -LiteralPath $dest) {
            Write-Host "skip clone (exists) $dest"
            continue
        }
        if ([string]::IsNullOrWhiteSpace($r.tag)) {
            Write-Host "git clone --depth 1 $($r.url) $dest"
            & git clone --depth 1 $r.url $dest
        } else {
            Write-Host "git clone --branch $($r.tag) --depth 1 $($r.url) $dest"
            & git clone --branch $r.tag --depth 1 $r.url $dest
        }
        if ($LASTEXITCODE -ne 0) { throw "git clone failed: $($r.url)" }
    }
}

Write-Host 'done. Next: docs/ATTACH.md. Do not paste MCP into user-global client config.'

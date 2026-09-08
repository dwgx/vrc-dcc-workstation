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
    [switch]$CloneMcp,
    [string]$UiLanguage = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($InstallRoot)) {
    $InstallRoot = $RepoRoot
}
$InstallRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($InstallRoot)

function Assert-PlainPath([string]$Path) {
    $cursor = $Path
    while ($cursor) {
        $item = Get-Item -LiteralPath $cursor -Force -ErrorAction SilentlyContinue
        if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Inspect linked install paths before writing: $cursor"
        }
        $parent = Split-Path -Parent $cursor
        if (-not $parent -or $parent -eq $cursor) { break }
        $cursor = $parent
    }
}

function Write-NewText([string]$Path, [string]$Text) {
    Assert-PlainPath $Path
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        Write-Host "kept existing $Path"
        return
    }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Path) | Out-Null
    $bytes = (New-Object System.Text.UTF8Encoding $false).GetBytes($Text)
    $stream = [IO.File]::Open($Path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    try { $stream.Write($bytes, 0, $bytes.Length) } finally { $stream.Dispose() }
    Write-Host "wrote $Path"
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

$template = Join-Path $RepoRoot 'mcp\cursor.mcp.json.template'
$outMcp = Join-Path $InstallRoot 'mcp\local.mcp.json'
$localExample = Join-Path $RepoRoot 'local.json.example'
$localJson = Join-Path $InstallRoot 'local.json'
$vendors = Join-Path $InstallRoot 'vendors\upstream'

$unityHits = @(Find-UnityEditor)
$blenderHits = @(Find-Blender)
$uvx = Find-Uvx

. (Join-Path $PSScriptRoot 'resolve-locale.ps1')
$uiLocale = Get-WorkstationLocale -RepoRoot $InstallRoot -Hint $UiLanguage

Write-Host "vrc-dcc-workstation bootstrap  root=$InstallRoot  apply=$Apply  clone=$CloneMcp"
Write-Host ("  [{0}] unity    {1}" -f $(if ($unityHits.Count) { 'OK' } else { 'MISSING' }), ($unityHits -join '; '))
Write-Host ("  [{0}] blender  {1}" -f $(if ($blenderHits.Count) { 'OK' } else { 'MISSING' }), ($blenderHits -join '; '))
Write-Host ("  [{0}] uvx      {1}" -f $(if ($uvx) { 'OK' } else { 'MISSING' }), $uvx)
Write-LocaleBanner -RepoRoot $InstallRoot -Locale $uiLocale

if (-not $Apply) {
    Write-Host 'dry-run only. Re-run with -Apply to create missing MCP/local.json. Existing MCP is kept; a separate InstallRoot must be empty.'
    exit 0
}

Assert-PlainPath $RepoRoot
Assert-PlainPath $InstallRoot
foreach ($path in @($outMcp, (Join-Path $InstallRoot '.mcp.json'), (Join-Path $InstallRoot '.cursor\mcp.json'), $localJson)) {
    Assert-PlainPath $path
    if (Test-Path -LiteralPath $path -PathType Container) { throw "Expected a configuration file: $path" }
}
$envHint = $null
foreach ($cand in @($UiLanguage, $env:WORKSTATION_UI_LANG, $env:VRC_DCC_UI_LANG, $env:DEBUGGER_UI_LANG)) {
    if (-not [string]::IsNullOrWhiteSpace($cand)) { $envHint = $cand; break }
}
$localeUpdate = $null
if ($envHint -and (Test-Path -LiteralPath $localJson -PathType Leaf)) {
    # An explicit locale choice may fill an empty preference, not reset local paths.
    $existing = Get-Content -LiteralPath $localJson -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($existing -isnot [pscustomobject]) { throw 'local.json must be a JSON object to update its locale.' }
    $preference = $existing.PSObject.Properties['ui_language']
    if ($null -eq $preference -or [string]::IsNullOrWhiteSpace([string]$preference.Value)) {
        $existing | Add-Member -NotePropertyName ui_language -NotePropertyValue $uiLocale -Force
        $localeUpdate = ($existing | ConvertTo-Json -Depth 100) + [Environment]::NewLine
    }
}
$sourceFull = [IO.Path]::GetFullPath($RepoRoot).TrimEnd('\', '/')
$targetFull = [IO.Path]::GetFullPath($InstallRoot).TrimEnd('\', '/')
$sameRoot = $sourceFull.Equals($targetFull, [StringComparison]::OrdinalIgnoreCase)

if (-not $sameRoot) {
    if ($targetFull.StartsWith($sourceFull + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or
        $sourceFull.StartsWith($targetFull + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Source and separate InstallRoot must not overlap.'
    }
    if (Test-Path -LiteralPath $InstallRoot) {
        if (-not (Test-Path -LiteralPath $InstallRoot -PathType Container) -or
            @(Get-ChildItem -LiteralPath $InstallRoot -Force).Count) {
            throw 'InstallRoot contains existing files. Use scripts/compare_upstream.py for a reviewed update, or run that installation''s own bootstrap to fill missing configuration. New installations need an empty directory.'
        }
    }
    # Plan all copies first. Existing installations use the update workflow.
    $copies = @()
    foreach ($rel in @('manifests', 'skills', 'docs', 'scripts', 'templates', 'mcp')) {
        $src = Join-Path $RepoRoot $rel
        if (-not (Test-Path -LiteralPath $src)) { continue }
        Assert-PlainPath $src
        foreach ($item in @(Get-ChildItem -LiteralPath $src -Recurse -Force)) {
            $relative = $item.FullName.Substring($sourceFull.Length + 1)
            if ($relative -match '(^|[\\/])(__pycache__|\.venv)([\\/]|$)' -or $item.Name -eq 'local.mcp.json') { continue }
            Assert-PlainPath $item.FullName
            if (-not $item.PSIsContainer) { $copies += $relative }
        }
    }
    foreach ($f in @('AGENTS.md', 'AGENTS.zh-CN.md', 'AGENTS.ja.md', 'AGENTS.ko.md', 'README.md', 'CLAUDE.md', 'GEMINI.md', 'OWNER.example.md', 'locales.json', 'local.json.example')) {
        $src = Join-Path $RepoRoot $f
        Assert-PlainPath $src
        if (Test-Path -LiteralPath $src -PathType Leaf) { $copies += $f }
    }
    Write-Host "copy skeleton $RepoRoot -> $InstallRoot"
    foreach ($relative in $copies) {
        $dest = Join-Path $InstallRoot $relative
        Assert-PlainPath $dest
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
        [IO.File]::Copy((Join-Path $RepoRoot $relative), $dest, $false)
    }
}

if (-not (Test-Path -LiteralPath $template)) {
    throw "Missing template: $template"
}

$uvxForTpl = if ($uvx) { $uvx.Replace('\', '/') } else { 'uvx' }
$text = [System.IO.File]::ReadAllText($template)
$text = $text.Replace('{{UVX}}', $uvxForTpl)
$utf8 = New-Object System.Text.UTF8Encoding $false
$mcpTargets = @(
    $outMcp,
    (Join-Path $InstallRoot '.mcp.json'),
    (Join-Path $InstallRoot '.cursor\mcp.json')
)
foreach ($dest in $mcpTargets) {
    Write-NewText $dest $text
}

if (-not (Test-Path -LiteralPath $localJson)) {
    $obj = Get-Content -LiteralPath $localExample -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($unityHits.Count) { $obj.unity_editor = $unityHits[0] }
    if ($blenderHits.Count) { $obj.blender_exe = $blenderHits[0] }
    if ($uvx) { $obj.uvx = $uvx }
    $obj | Add-Member -NotePropertyName install_root -NotePropertyValue $InstallRoot -Force
    if ($envHint) { $obj | Add-Member -NotePropertyName ui_language -NotePropertyValue $uiLocale -Force }
    $json = $obj | ConvertTo-Json -Depth 6
    Write-NewText $localJson ($json + [Environment]::NewLine)
} else {
    Write-Host "kept existing $localJson"
}

if ($null -ne $localeUpdate) {
    [IO.File]::WriteAllText($localJson, $localeUpdate, $utf8)
    Write-Host "filled empty ui_language in $localJson"
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

Write-Host 'done. Next: docs/ATTACH.md and docs/BOOTSTRAP.md. Do not paste MCP into user-global client config.'

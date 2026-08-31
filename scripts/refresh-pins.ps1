#Requires -Version 5.1
<#
.SYNOPSIS
  Re-fetch live pins for vrc-dcc manifests (network). Writes notes if a pin moved.

  GitHub: prefer `gh api` (authenticated). Unauthenticated REST is 60 req/hr and
  will 403 this PC after a few browser/agent hits. PyPI does not have that cap.
  UnityAgent: take the newest `editor-v*` tag, not `sdk-v*` or a stale VPM catalog.
#>
[CmdletBinding()]
param([switch]$Apply)

$ErrorActionPreference = 'Stop'
$vrc = Split-Path $PSScriptRoot -Parent
$toolsPath = Join-Path $vrc 'manifests\tools.json'
$tools = Get-Content -LiteralPath $toolsPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Get-PyPIVersion([string]$name) {
    $d = Invoke-RestMethod "https://pypi.org/pypi/$name/json"
    return [string]$d.info.version
}

function Get-GitHubLatestTag {
    param(
        [Parameter(Mandatory = $true)][string]$Repo,
        [string]$TagPrefix = ''
    )
    $tag = $null
    $ghCmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($null -ne $ghCmd) {
        if (-not [string]::IsNullOrWhiteSpace($TagPrefix)) {
            $raw = & gh api "repos/$Repo/releases?per_page=20" --jq '.[].tag_name' 2>$null
            if ($LASTEXITCODE -eq 0 -and $null -ne $raw) {
                $tag = @($raw) | Where-Object { $_ -like ($TagPrefix + '*') } | Select-Object -First 1
            }
        }
        if ([string]::IsNullOrWhiteSpace($tag)) {
            $latest = & gh api "repos/$Repo/releases/latest" --jq .tag_name 2>$null
            if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($latest)) {
                $tag = [string]$latest
            }
        }
    }
    if ([string]::IsNullOrWhiteSpace($tag)) {
        try {
            $r = Invoke-RestMethod "https://api.github.com/repos/$Repo/releases/latest"
            $tag = [string]$r.tag_name
        } catch {
            Write-Warning ("GitHub {0}: {1}" -f $Repo, $_.Exception.Message)
            return $null
        }
    }
    return [string]$tag
}

$blender = Get-PyPIVersion 'blender-mcp'
$unityPy = Get-PyPIVersion 'mcpforunityserver'
$coplay = Get-GitHubLatestTag -Repo 'CoplayDev/unity-mcp'
$agent = Get-GitHubLatestTag -Repo 'lighfu/unity-agent' -TagPrefix 'editor-v'
$dcc = Get-GitHubLatestTag -Repo 'dcc-mcp/dcc-mcp-blender'

$report = @(
    "blender-mcp pypi=$blender (pin 1.9.0)",
    "mcpforunityserver pypi=$unityPy (pin 10.1.2)",
    "CoplayDev/unity-mcp latest=$(if ($coplay) { $coplay } else { 'UNAVAILABLE' }) (pin v10.1.2)",
    "lighfu/unity-agent editor=$(if ($agent) { $agent } else { 'UNAVAILABLE' }) (pin editor-v0.15.0)",
    "dcc-mcp-blender latest=$(if ($dcc) { $dcc } else { 'UNAVAILABLE' }) (pin v0.2.3)"
)
$report | ForEach-Object { Write-Host $_ }

if (-not $Apply) {
    Write-Host 'dry-run. Re-run with -Apply to append notes/ if any pin drifted.'
    exit 0
}

$drift = @()
if ($blender -ne '1.9.0') { $drift += "blender-mcp $blender" }
if ($unityPy -ne '10.1.2') { $drift += "mcpforunityserver $unityPy" }
if ($coplay -and $coplay -ne 'v10.1.2') { $drift += "unity-mcp $coplay" }
if ($agent -and $agent -ne 'editor-v0.15.0') { $drift += "unity-agent $agent" }
if ($dcc -and $dcc -ne 'v0.2.3') { $drift += "dcc-mcp-blender $dcc" }

if ($drift.Count -eq 0) {
    Write-Host 'pins still match. no note written.'
    exit 0
}

$day = Get-Date -Format 'yyyy-MM-dd'
$note = Join-Path $vrc "notes\$day-pin-drift.md"
$body = @"
---
tags: [pins]
status: observed
source: scripts/refresh-pins.ps1
---

# Pin drift $day

$($drift -join "`n")

Update manifests/tools.json only after the Owner accepts the new pins.
"@
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($note, $body.TrimEnd() + [Environment]::NewLine, $utf8)
Write-Host "wrote $note"

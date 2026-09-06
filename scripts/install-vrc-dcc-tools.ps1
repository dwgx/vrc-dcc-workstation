#Requires -Version 5.1
<#
.SYNOPSIS
  Add com.vrc-dcc.tools to the open Unity project's Packages/manifest.json,
  copy maps/<avatar>/POLICY.json to Assets/VrcDcc/POLICY.json, and drop a
  Cursor rule so 改模 agents load slice-loop.

  Refuses home / station / agent-system cwd. Run from ANY avatar Unity window
  (folder that has Assets/ + Packages/manifest.json). Not Kaguya-only.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$station = Split-Path -Parent $PSScriptRoot
$pkg = Join-Path $station 'unity\vrc-dcc-tools'
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
    Write-Output 'install-vrc-dcc-tools: refuse. Home cwd must not write a Unity tree.'
    Write-Output "open a Cursor window at the avatar Unity project then: powershell -File $PSCommandPath"
    exit 2
}
if (Test-Under $cwd $agentSystem) {
    Write-Output 'install-vrc-dcc-tools: refuse. agent-system cwd must not write a Unity tree.'
    exit 2
}
if (Test-Under $cwd $station) {
    Write-Output 'install-vrc-dcc-tools: refuse. Station cwd must not write a Unity tree.'
    Write-Output 'open a Cursor window at the avatar Unity project then rerun this script.'
    exit 2
}
$assets = Join-Path $cwd 'Assets'
$manifest = Join-Path $cwd 'Packages\manifest.json'
if (-not (Test-Path -LiteralPath $assets) -or -not (Test-Path -LiteralPath $manifest)) {
    Write-Output 'install-vrc-dcc-tools: refuse. cwd is not a Unity project (need Assets/ and Packages/manifest.json).'
    exit 2
}
if (-not (Test-Path -LiteralPath (Join-Path $pkg 'package.json'))) {
    throw "missing package $pkg"
}

$avatarId = Split-Path -Leaf $cwd
$py = 'python'
$loc = Join-Path $station 'local.json'
if (Test-Path -LiteralPath $loc) {
    try {
        $locObj = Get-Content -LiteralPath $loc -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($locObj.python_exe -and (Test-Path -LiteralPath ([string]$locObj.python_exe))) {
            $py = [string]$locObj.python_exe
        }
    } catch { }
}
$pkgUnix = ($pkg -replace '\\', '/')
$cwdUnix = ($cwd -replace '\\', '/')
$code = @"
import json
from pathlib import Path
root = Path(r'''$cwd''')
man = root / 'Packages' / 'manifest.json'
data = json.loads(man.read_text(encoding='utf-8'))
deps = data.setdefault('dependencies', {})
deps['com.vrc-dcc.tools'] = 'file:$pkgUnix'
man.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('wrote', man)
"@
& $py -c $code
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$policyDestDir = Join-Path $assets 'VrcDcc'
New-Item -ItemType Directory -Force -Path $policyDestDir | Out-Null
$policyDest = Join-Path $policyDestDir 'POLICY.json'
$policySrc = Join-Path $station "maps\$avatarId\POLICY.json"
$policyDefault = Join-Path $pkg 'POLICY.default.json'
if (Test-Path -LiteralPath $policySrc) {
    Copy-Item -LiteralPath $policySrc -Destination $policyDest -Force
    Write-Output "copied $policySrc -> $policyDest"
} elseif (Test-Path -LiteralPath $policyDefault) {
    Copy-Item -LiteralPath $policyDefault -Destination $policyDest -Force
    Write-Output "copied default POLICY -> $policyDest"
    Write-Output "warning: default POLICY has empty unity_root_name; named vrc_* will return NO_AVATAR_IDENTITY until maps/<id>/POLICY.json is copied."
}
if (-not (Test-Path -LiteralPath $policyDest)) {
    Write-Error "POLICY.json missing after copy: $policyDest"
    exit 2
}

$ruleDir = Join-Path $cwd '.cursor\rules'
New-Item -ItemType Directory -Force -Path $ruleDir | Out-Null
$rule = Join-Path $ruleDir 'vrc-dcc-slice-loop.mdc'
$ruleBody = @"
---
description: Avatar DCC uses station slice-loop. Named vrc_* not execute_code.
alwaysApply: true
---

# Avatar DCC (pointer)

Station: ``$station``
Authoritative: station ``AGENTS.md`` / gitignored ``OWNER.md``.
Chat in the owner's language. Tracked files stay English. Public git is optional.

Every 改模 slice: ``templates/JOB.md`` then ``python maps/handshake.py $avatarId`` then ``skills/vrc-dcc/references/slice-loop.md``.
``python maps/gate.py $avatarId begin <review-id>`` then one named ``vrc_*`` on CoplayDev ``8080``.
If ``vrc_audit`` is missing: ``powershell -File $PSCommandPath`` (this Unity cwd), Reload Window.
Do not invent ``execute_code``. Do not SDK Publish.
"@
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($rule, $ruleBody.TrimEnd() + [Environment]::NewLine, $utf8)
Write-Output "wrote $rule"
Write-Output 'install-vrc-dcc-tools: done. Unity compile. VrcDccMcpBoot quiet-starts HTTP then the Editor websocket (Skip Configure All if a wizard appears). Cursor Reload Window on this Unity folder. Expect vrc_audit in GetDynamicTools / HTTP tools/list.'
exit 0

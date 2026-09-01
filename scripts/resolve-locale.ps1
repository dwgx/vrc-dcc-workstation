#Requires -Version 5.1
<#
.SYNOPSIS
  Resolve UI locale for workstation templates (en, zh-CN, ja, ko).
#>

function Get-WorkstationLocale {
    [CmdletBinding()]
    param(
        [string]$RepoRoot = '',
        [string]$Hint = ''
    )
    if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
        $RepoRoot = Split-Path -Parent $PSScriptRoot
    }
    $map = @{
        'zh' = 'zh-CN'; 'zh-cn' = 'zh-CN'; 'zh-hans' = 'zh-CN'; 'zh-sg' = 'zh-CN'
        'zh-tw' = 'zh-CN'; 'zh-hk' = 'zh-CN'; 'zh-hant' = 'zh-CN'; 'chs' = 'zh-CN'; 'cht' = 'zh-CN'
        'ja' = 'ja'; 'ja-jp' = 'ja'; 'jp' = 'ja'
        'ko' = 'ko'; 'ko-kr' = 'ko'; 'kr' = 'ko'
        'en' = 'en'; 'en-us' = 'en'; 'en-gb' = 'en'; 'en-au' = 'en'
    }
    function Normalize([string]$Raw) {
        if ([string]::IsNullOrWhiteSpace($Raw)) { return $null }
        $k = $Raw.Trim().ToLowerInvariant().Replace('_', '-')
        if ($map.ContainsKey($k)) { return [string]$map[$k] }
        $short = ($k -split '-')[0]
        if ($map.ContainsKey($short)) { return [string]$map[$short] }
        return $null
    }
    foreach ($cand in @($Hint)) {
        $n = Normalize $cand
        if ($n) { return $n }
    }
    $localPath = Join-Path $RepoRoot 'local.json'
    if (Test-Path -LiteralPath $localPath) {
        try {
            $obj = Get-Content -LiteralPath $localPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $n = Normalize ([string]$obj.ui_language)
            if ($n) { return $n }
        } catch { }
    }
    foreach ($cand in @($env:WORKSTATION_UI_LANG, $env:VRC_DCC_UI_LANG, $env:DEBUGGER_UI_LANG)) {
        $n = Normalize $cand
        if ($n) { return $n }
    }
    try {
        $n = Normalize ([System.Globalization.CultureInfo]::CurrentUICulture.Name)
        if ($n) { return $n }
    } catch { }
    return 'en'
}

function Get-WorkstationInstallRoot {
    [CmdletBinding()]
    param(
        [string]$RepoRoot = '',
        [string]$Override = ''
    )
    if (-not [string]::IsNullOrWhiteSpace($Override)) {
        return $Override.Trim()
    }
    if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
        $RepoRoot = Split-Path -Parent $PSScriptRoot
    }
    $localPath = Join-Path $RepoRoot 'local.json'
    if (Test-Path -LiteralPath $localPath) {
        try {
            $obj = Get-Content -LiteralPath $localPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $ir = [string]$obj.install_root
            if (-not [string]::IsNullOrWhiteSpace($ir)) {
                return $ir.Trim()
            }
        } catch { }
    }
    return $RepoRoot
}

function Get-LocaleSuffix([string]$Locale) {
    switch ($Locale) {
        'zh-CN' { return '.zh-CN' }
        'ja' { return '.ja' }
        'ko' { return '.ko' }
        default { return '' }
    }
}

function Get-LocaleRootFile {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$Stem,
        [string]$Locale = 'en'
    )
    $suf = Get-LocaleSuffix $Locale
    $named = Join-Path $RepoRoot ($Stem + $suf + '.md')
    if ($suf -and (Test-Path -LiteralPath $named)) { return $named }
    return (Join-Path $RepoRoot ($Stem + '.md'))
}

function Save-WorkstationLocale {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [string]$Locale = '',
        [string]$InstallRoot = '',
        [switch]$WriteLocale
    )
    $path = Join-Path $RepoRoot 'local.json'
    $utf8 = New-Object System.Text.UTF8Encoding $false
    $obj = $null
    if (Test-Path -LiteralPath $path) {
        try { $obj = Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json } catch { }
    }
    $example = Join-Path $RepoRoot 'local.json.example'
    if ($null -eq $obj -and (Test-Path -LiteralPath $example)) {
        $obj = Get-Content -LiteralPath $example -Raw -Encoding UTF8 | ConvertFrom-Json
    }
    if ($null -eq $obj) {
        $obj = [pscustomobject]@{ ui_language = ''; install_root = '' }
    }
    if (-not [string]::IsNullOrWhiteSpace($InstallRoot)) {
        $obj | Add-Member -NotePropertyName install_root -NotePropertyValue $InstallRoot -Force
    }
    if ($WriteLocale -and -not [string]::IsNullOrWhiteSpace($Locale)) {
        $existing = $null
        try { $existing = [string]$obj.ui_language } catch { }
        if ([string]::IsNullOrWhiteSpace($existing)) {
            $obj | Add-Member -NotePropertyName ui_language -NotePropertyValue $Locale -Force
        }
    }
    $json = $obj | ConvertTo-Json -Depth 8
    [System.IO.File]::WriteAllText($path, $json + [Environment]::NewLine, $utf8)
}

function Write-LocaleBanner {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$Locale
    )
    $agents = Get-LocaleRootFile -RepoRoot $RepoRoot -Stem 'AGENTS' -Locale $Locale
    $readme = Get-LocaleRootFile -RepoRoot $RepoRoot -Stem 'README' -Locale $Locale
    $qDir = Join-Path $RepoRoot ('templates\i18n\' + $Locale + '\INIT_QUESTIONNAIRE.md')
    $qEn = Join-Path $RepoRoot 'templates\INIT_QUESTIONNAIRE.md'
    $q = if (Test-Path -LiteralPath $qDir) { $qDir } else { $qEn }
    Write-Host ("UI locale={0}" -f $Locale)
    Write-Host ("  README        {0}" -f $readme)
    Write-Host ("  AGENTS        {0}" -f $agents)
    Write-Host ("  questionnaire {0}" -f $q)
    Write-Host '  Chat in this locale. Git commits stay English. See docs/I18N.md'
}

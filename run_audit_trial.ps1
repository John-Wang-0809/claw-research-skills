param(
    [int]$Limit = 5,
    [int]$Workers = 1,
    [string[]]$Themes = @("01_information_retrieval_evidence_collection"),
    [switch]$AllThemes,
    [switch]$NoResume,
    [switch]$DryRun,
    [int]$ShowTopCorrections = 3,
    [switch]$ApplyCorrections
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  $Title"
    Write-Host "========================================"
}

function Normalize-Themes {
    param([string[]]$InputThemes)

    $items = @()
    foreach ($raw in $InputThemes) {
        if (-not $raw) { continue }
        $parts = $raw -split '[,;]'
        foreach ($part in $parts) {
            $t = $part.Trim()
            if ($t.Length -gt 0) {
                $items += $t
            }
        }
    }

    # Keep stable order while deduping
    $seen = @{}
    $out = @()
    foreach ($t in $items) {
        if (-not $seen.ContainsKey($t)) {
            $seen[$t] = $true
            $out += $t
        }
    }
    return $out
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$auditScript = Join-Path $repoRoot "audit_skill_description_match_responses.py"
$applyScript = Join-Path $repoRoot "apply_audit_corrections_to_theme.py"
$themeDir = Join-Path $repoRoot "Final_Research_Skills_Thematic_Split"

if (-not (Test-Path -LiteralPath $auditScript)) {
    throw "audit script not found: $auditScript"
}

$ThemeList = @()
if ($AllThemes) {
    if (-not (Test-Path -LiteralPath $themeDir)) {
        throw "Theme directory not found: $themeDir"
    }
    $allThemeNames = Get-ChildItem -LiteralPath $themeDir -Filter *.md -File |
        Where-Object { $_.Name -ne "README.md" } |
        Sort-Object Name |
        ForEach-Object { $_.BaseName }
    $ThemeList = @(Normalize-Themes -InputThemes $allThemeNames)
} else {
    $ThemeList = @(Normalize-Themes -InputThemes $Themes)
}

if (-not $ThemeList -or $ThemeList.Count -eq 0) {
    throw "No valid themes parsed from -Themes input."
}

Write-Section "Audit Trial Runner"
Write-Host "Repo Root : $repoRoot"
Write-Host "Script    : $auditScript"
Write-Host "Limit     : $Limit"
Write-Host "Workers   : $Workers"
Write-Host "Themes    : $($ThemeList -join ', ')"
Write-Host "DryRun    : $DryRun"
Write-Host "NoResume  : $NoResume"
Write-Host "Preview   : $ShowTopCorrections correction row(s)"
Write-Host "AllThemes : $AllThemes"
Write-Host "ApplyFix  : $ApplyCorrections"

try {
    $null = & python --version 2>$null
} catch {
    throw "python is not available in PATH."
}

$argsList = @(
    $auditScript,
    "--limit", "$Limit",
    "--workers", "$Workers"
)

foreach ($theme in $ThemeList) {
    if ($theme -and $theme.Trim().Length -gt 0) {
        $argsList += @("--theme", $theme.Trim())
    }
}

if ($NoResume) {
    $argsList += "--no-resume"
}
if ($DryRun) {
    $argsList += "--dry-run"
}

Write-Section "Running Python Audit"
$nativePrefExists = $null -ne (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue)
if ($nativePrefExists) {
    $previousNativePref = $PSNativeCommandUseErrorActionPreference
    $script:PSNativeCommandUseErrorActionPreference = $false
}
$output = @()
try {
    $env:PYTHONUNBUFFERED = "1"
    & python -u @argsList 2>&1 | Tee-Object -Variable output | ForEach-Object { Write-Host $_ }
    $exitCode = $LASTEXITCODE
}
finally {
    Remove-Item Env:\PYTHONUNBUFFERED -ErrorAction SilentlyContinue
    if ($nativePrefExists) {
        $script:PSNativeCommandUseErrorActionPreference = $previousNativePref
    }
}
$output = @($output)

if ($exitCode -ne 0) {
    throw "audit script failed with exit code $exitCode"
}

$runDirLine = $output | Select-String -Pattern "^Run directory:\s*(.+)$" | Select-Object -Last 1
if (-not $runDirLine) {
    if ($DryRun) {
        $runDirLine = $output | Select-String -Pattern "^Dry-run completed\. Output:\s*(.+)$" | Select-Object -Last 1
    }
}

if (-not $runDirLine) {
    Write-Warning "Could not parse run directory from output."
    exit 0
}

$runDir = $runDirLine.Matches[0].Groups[1].Value.Trim()
$summaryPath = Join-Path $runDir "audit_summary.json"
$mismatchPath = Join-Path $runDir "audit_mismatch_only.md"
$resultsPath = Join-Path $runDir "audit_results.jsonl"

Write-Section "Run Output"
Write-Host "Run Dir   : $runDir"
Write-Host "Summary   : $summaryPath"
Write-Host "Mismatch  : $mismatchPath"
Write-Host "Results   : $resultsPath"

if (Test-Path -LiteralPath $summaryPath) {
    Write-Section "Quick Summary"
    $summary = Get-Content -LiteralPath $summaryPath -Raw | ConvertFrom-Json
    Write-Host ("Total Rows       : {0}" -f $summary.total_rows)
    Write-Host ("OK Rows          : {0}" -f $summary.ok_rows)
    if ($summary.PSObject.Properties.Name -contains "aligned_rows") {
        Write-Host ("Aligned Rows     : {0}" -f $summary.aligned_rows)
    }
    if ($summary.PSObject.Properties.Name -contains "unaligned_rows") {
        Write-Host ("Unaligned Rows   : {0}" -f $summary.unaligned_rows)
    }
    Write-Host ("Failed Rows      : {0}" -f $summary.failed_rows)
}

if ((-not $DryRun) -and $ShowTopCorrections -gt 0 -and (Test-Path -LiteralPath $resultsPath)) {
    Write-Section "Correction Preview"
    $rows = @()
    Get-Content -LiteralPath $resultsPath | ForEach-Object {
        if (-not [string]::IsNullOrWhiteSpace($_)) {
            try {
                $rows += ($_ | ConvertFrom-Json)
            } catch {}
        }
    }

    $shown = 0
    foreach ($row in $rows) {
        if ($shown -ge $ShowTopCorrections) { break }
        $checks = $row.parsed_result.field_checks
        if (-not $checks) { continue }

        $hasCorrection = $false
        foreach ($field in @("why_research_related","function_explanation","execution_flow","evidence")) {
            if ($checks.$field -and $checks.$field.correction_applied -eq $true) {
                $hasCorrection = $true
                break
            }
        }
        if (-not $hasCorrection) { continue }

        $shown++
        Write-Host ""
        Write-Host ("[{0}] {1} ({2})" -f $shown, $row.skill, $row.repo)
        foreach ($field in @("why_research_related","function_explanation","execution_flow","evidence")) {
            $item = $checks.$field
            if ($item -and $item.correction_applied -eq $true) {
                $text = [string]$item.corrected_text
                if ($text.Length -gt 180) { $text = $text.Substring(0,180) + "..." }
                Write-Host ("- {0}: {1}" -f $field, $text)
            }
        }
    }

    if ($shown -eq 0) {
        Write-Host "No correction_applied=true rows found in this run."
    } else {
        Write-Host ""
        Write-Host ("Previewed {0} row(s). Full corrected text is in: {1}" -f $shown, $resultsPath)
    }
}

if ($ApplyCorrections) {
    if ($DryRun) {
        Write-Section "Apply Corrections"
        Write-Host "Skipping apply step because -DryRun is enabled."
    } else {
        if (-not (Test-Path -LiteralPath $applyScript)) {
            throw "apply script not found: $applyScript"
        }
        if (-not (Test-Path -LiteralPath $resultsPath)) {
            throw "results jsonl not found: $resultsPath"
        }

        Write-Section "Apply Corrections"
        $applyOk = 0
        $applyFail = 0
        $applySkip = 0

        foreach ($theme in $ThemeList) {
            $themeDoc = Join-Path $themeDir "$theme.md"
            if (-not (Test-Path -LiteralPath $themeDoc)) {
                Write-Warning "Theme markdown not found, skipped: $themeDoc"
                $applySkip++
                continue
            }

            Write-Host ""
            Write-Host "[Apply] $theme"
            $applyArgs = @(
                $applyScript,
                "--theme-doc", $themeDoc,
                "--audit-jsonl", $resultsPath
            )

            $nativePrefExists = $null -ne (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue)
            if ($nativePrefExists) {
                $previousNativePref = $PSNativeCommandUseErrorActionPreference
                $script:PSNativeCommandUseErrorActionPreference = $false
            }
            try {
                $env:PYTHONUNBUFFERED = "1"
                $applyOutput = & python -u @applyArgs 2>&1
                $applyExitCode = $LASTEXITCODE
            }
            finally {
                Remove-Item Env:\PYTHONUNBUFFERED -ErrorAction SilentlyContinue
                if ($nativePrefExists) {
                    $script:PSNativeCommandUseErrorActionPreference = $previousNativePref
                }
            }

            $applyOutput | ForEach-Object { Write-Host $_ }
            if ($applyExitCode -ne 0) {
                $applyFail++
                Write-Warning "Apply failed for theme: $theme"
            } else {
                $applyOk++
            }
        }

        Write-Host ""
        Write-Host "Apply Summary:"
        Write-Host "  Success : $applyOk"
        Write-Host "  Failed  : $applyFail"
        Write-Host "  Skipped : $applySkip"

        if ($applyFail -gt 0) {
            throw "One or more themes failed during correction apply."
        }
    }
}

Write-Host ""
Write-Host "Trial run completed."

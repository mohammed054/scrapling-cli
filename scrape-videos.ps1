<#
.SYNOPSIS
    Scrape YouTube video transcripts from a URL list file using Chrome cookies.

.DESCRIPTION
    This script:
    1. Kills ALL Chrome processes (including background/utility processes)
    2. Waits for cookie database to unlock
    3. Reads video URLs from videos.txt
    4. Runs the Python scraper using Chrome's Default profile cookies
    5. Restarts your main Chrome profile

.PARAMETER UrlsFile
    Path to the URLs file (default: videos.txt)

.PARAMETER OutputDir
    Output directory for markdown files (default: output/videos)

.PARAMETER CookiesProfile
    Chrome profile to use for cookies (default: Default)

.PARAMETER CookiesFile
    Path to Netscape format cookies.txt file (alternative to browser profile)

.PARAMETER VerboseLog
    Enable verbose logging

.PARAMETER NoEnrich
    Skip watch page enrichment (faster, less metadata)

.PARAMETER NoYtDlp
    Disable yt-dlp backend (use only youtube_transcript_api)

.PARAMETER NoRestartChrome
    Don't restart Chrome after completion

.EXAMPLE
    .\scrape-videos.ps1

.EXAMPLE
    .\scrape-videos.ps1 -VerboseLog -NoEnrich

.EXAMPLE
    .\scrape-videos.ps1 -UrlsFile "my_videos.txt" -OutputDir "output/my_videos"

.EXAMPLE
    .\scrape-videos.ps1 -CookiesFile "cookies.txt" -NoYtDlp
#>

[CmdletBinding()]
param(
    [Parameter()]
    [string]$UrlsFile = "videos.txt",

    [Parameter()]
    [string]$OutputDir = "output/videos",

    [Parameter()]
    [string]$CookiesProfile = "Default",

    [Parameter()]
    [string]$CookiesFile = "",

    [Parameter()]
    [switch]$VerboseLog,

    [Parameter()]
    [switch]$NoEnrich,

    [Parameter()]
    [switch]$NoYtDlp,

    [Parameter()]
    [switch]$NoRestartChrome
)

# --- Configuration ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = $ScriptDir

# --- Functions ---
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

function Kill-AllChrome {
    Write-Log "Killing all Chrome processes..."
    $processes = @("chrome", "chromedriver")
    foreach ($procName in $processes) {
        $procs = Get-Process -Name $procName -ErrorAction SilentlyContinue
        if ($procs) {
            foreach ($proc in $procs) {
                try {
                    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
                    Write-Log "  Stopped $procName (PID: $($proc.Id))"
                } catch {
                    Write-Log "  Failed to stop $procName (PID: $($proc.Id)): $_" "WARN"
                }
            }
        }
    }
    # Also kill any remaining Chrome-related processes
    $chromeProcs = Get-Process | Where-Object { $_.ProcessName -like "*chrome*" } -ErrorAction SilentlyContinue
    foreach ($proc in $chromeProcs) {
        try {
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
            Write-Log "  Stopped $($proc.ProcessName) (PID: $($proc.Id))"
        } catch { }
    }
    Write-Log "Waiting for file handles to release..."
    Start-Sleep -Seconds 6
}

function Run-Scraper {
    param(
        [string]$UrlsFile,
        [string]$OutputDir,
        [string]$CookiesProfile,
        [string]$CookiesFile,
        [switch]$VerboseLog,
        [switch]$NoEnrich,
        [switch]$NoYtDlp
    )

    Write-Log "Starting transcript scraper..."
    Write-Log "  URLs file:    $UrlsFile"
    Write-Log "  Output dir:   $OutputDir"
    if ($CookiesFile) {
        Write-Log "  Cookies:      file:$CookiesFile"
    } else {
        Write-Log "  Cookies:      chrome:$CookiesProfile"
    }
    if ($NoYtDlp) {
        Write-Log "  Backend:      youtube_transcript_api only (yt-dlp disabled)"
    }

    $pythonExe = (Get-Command "python" -ErrorAction SilentlyContinue).Source
    if (-not $pythonExe) {
        $pythonExe = "python"
    }

    $argList = @(
        "scrape_videos.py",
        "--urls-file", $UrlsFile,
        "--output-dir", $OutputDir,
        "--transcript-delay", "20",
        "--transcript-retries", "12",
        "--transcript-rate-limit-cooldown", "1200",
        "--allow-missing-transcripts",
        "--workers", "1"
    )

    if ($CookiesFile) {
        $argList += "--cookies-file", $CookiesFile
    } else {
        $argList += "--cookies-from-browser", "chrome:$CookiesProfile"
    }

    if ($VerboseLog) { $argList += "--verbose" }
    if ($NoEnrich) { $argList += "--no-enrich" }
    if ($NoYtDlp) { $argList += "--no-yt-dlp" }

    Write-Log "Running: $pythonExe $($argList -join ' ')"

    Set-Location $ProjectDir
    $process = Start-Process -FilePath $pythonExe -ArgumentList $argList -Wait -NoNewWindow -PassThru
    return $process.ExitCode
}

# --- Main Execution ---
Write-Log "=" * 60
Write-Log "YOUTUBE VIDEO TRANSCRIPT SCRAPER"
Write-Log "=" * 60

try {
    # Step 1: Kill all Chrome processes
    Kill-AllChrome

    # Step 2: Run the scraper
    $exitCode = Run-Scraper `
        -UrlsFile $UrlsFile `
        -OutputDir $OutputDir `
        -CookiesProfile $CookiesProfile `
        -CookiesFile $CookiesFile `
        -VerboseLog:$VerboseLog `
        -NoEnrich:$NoEnrich `
        -NoYtDlp:$NoYtDlp

    # Step 3: Restart main Chrome
    if (-not $NoRestartChrome) {
        Write-Log "Restarting main Chrome..."
        Start-Process "chrome.exe" -ErrorAction SilentlyContinue
    }

    Write-Log "=" * 60
    if ($exitCode -eq 0) {
        Write-Log "SUCCESS: All videos processed!" "INFO"
    } else {
        Write-Log "COMPLETED WITH ERRORS: Exit code $exitCode" "WARN"
    }
    Write-Log "=" * 60

    exit $exitCode
}
catch {
    Write-Log "FATAL ERROR: $_" "ERROR"

    # Try to restart Chrome even on failure
    if (-not $NoRestartChrome) {
        Write-Log "Restarting main Chrome..."
        Start-Process "chrome.exe" -ErrorAction SilentlyContinue
    }
    exit 1
}

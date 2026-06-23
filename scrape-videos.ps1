<# 
.SYNOPSIS
    Scrape YouTube video transcripts from a URL list file using dedicated Chrome profile.

.DESCRIPTION
    This script:
    1. Kills ALL Chrome processes (including background/utility processes)
    2. Creates/uses a dedicated Chrome profile for scraping (avoids cookie locks)
    3. Reads video URLs from videos.txt
    4. Runs the Python scraper for each video
    5. Restarts your main Chrome profile

.PARAMETER UrlsFile
    Path to the URLs file (default: videos.txt)

.PARAMETER OutputDir
    Output directory for markdown files (default: output/videos)

.PARAMETER ProfilePath
    Path to dedicated Chrome profile (default: Z:\chrome-scrape-profile)

.PARAMETER VerboseLog
    Enable verbose logging

.PARAMETER NoEnrich
    Skip watch page enrichment (faster, less metadata)

.PARAMETER NoRestartChrome
    Don't restart Chrome after completion

.EXAMPLE
    .\scrape-videos.ps1

.EXAMPLE
    .\scrape-videos.ps1 -Verbose -NoEnrich

.EXAMPLE
    .\scrape-videos.ps1 -UrlsFile "my_videos.txt" -OutputDir "output/my_videos"
#>

[CmdletBinding()]
param(
    [Parameter()]
    [string]$UrlsFile = "videos.txt",

    [Parameter()]
    [string]$OutputDir = "output/videos",

    [Parameter()]
    [string]$ProfilePath = "Z:\chrome-scrape-profile",

    [Parameter()]
    [switch]$VerboseLog,

    [Parameter()]
    [switch]$NoEnrich,

    [Parameter()]
    [switch]$NoRestartChrome
)

# --- Configuration ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PythonScript = Join-Path $ScriptDir "scrape_videos.py"
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
    Write-Log "Waiting for file handles to release..."
    Start-Sleep -Seconds 4
}

function Ensure-ProfileExists {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        Write-Log "Creating dedicated Chrome profile at: $Path"
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Log "Profile directory created. Launching Chrome for initial setup..."
        Write-Log "Please sign in to YouTube in the opened Chrome window, then close it."
        $chromeExe = (Get-Command "chrome.exe" -ErrorAction SilentlyContinue).Source
        if (-not $chromeExe) {
            $chromeExe = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
            if (-not (Test-Path $chromeExe)) {
                $chromeExe = "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
            }
        }
        if (Test-Path $chromeExe) {
            Start-Process -FilePath $chromeExe -ArgumentList "--user-data-dir=`"$Path`"", "--no-first-run" -Wait
            Write-Log "Chrome setup complete."
        } else {
            Write-Log "Chrome executable not found. Please create profile manually." "ERROR"
            exit 1
        }
    } else {
        Write-Log "Using existing Chrome profile at: $Path"
    }
}

function Run-Scraper {
    param(
        [string]$UrlsFile,
        [string]$OutputDir,
        [string]$ProfilePath,
        [switch]$VerboseLog,
        [switch]$NoEnrich
    )

    Write-Log "Starting transcript scraper..."
    Write-Log "  URLs file:   $UrlsFile"
    Write-Log "  Output dir:  $OutputDir"
    Write-Log "  Profile:     $ProfilePath"

    $pythonExe = (Get-Command "python" -ErrorAction SilentlyContinue).Source
    if (-not $pythonExe) {
        $pythonExe = "python"
    }

    $argList = @(
        "scrape_videos.py",
        "--urls-file", $UrlsFile,
        "--output-dir", $OutputDir,
        "--cookies-from-browser", "chrome:$ProfilePath",
        "--transcript-delay", "12",
        "--transcript-retries", "8",
        "--transcript-rate-limit-cooldown", "600",
        "--allow-missing-transcripts",
        "--workers", "1"
    )

    if ($VerboseLog) { $argList += "--verbose" }
    if ($NoEnrich) { $argList += "--no-enrich" }

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

    # Step 2: Ensure dedicated profile exists
    Ensure-ProfileExists -Path $ProfilePath

    # Step 3: Run the scraper
    $exitCode = Run-Scraper `
        -UrlsFile $UrlsFile `
        -OutputDir $OutputDir `
        -ProfilePath $ProfilePath `
        -VerboseLog:$VerboseLog `
        -NoEnrich:$NoEnrich

    # Step 4: Restart main Chrome
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
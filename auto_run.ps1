param(
    [string]$PythonExe = "python",
    [string]$ChannelsFile = "channels.daily.txt",
    [string]$OutputDir = "output_daily",
    [string]$StateFile = "state.daily.json",
    [string]$LogDir = "logs",
    [int]$Workers = 2,
    [switch]$VerboseLogs
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$channelsPath = Join-Path $repoRoot $ChannelsFile
if (-not (Test-Path $channelsPath)) {
    throw "Channels file not found: $channelsPath"
}

$channels = Get-Content $channelsPath |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith("#") }

if (-not $channels -or $channels.Count -eq 0) {
    throw "No channels were found in $channelsPath"
}

$logPath = Join-Path $repoRoot $LogDir
New-Item -ItemType Directory -Force -Path $logPath | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$runLog = Join-Path $logPath "daily_fetch_$timestamp.log"

$arguments = @(
    "fetch_new.py",
    "--channels"
) + $channels + @(
    "--transcripts",
    "--workers", $Workers.ToString(),
    "--output-dir", $OutputDir,
    "--state-file", $StateFile,
    "--log-file", $runLog
)

if ($VerboseLogs) {
    $arguments += "--verbose"
}

Write-Host "Running daily fetch for $($channels.Count) channels..."
Write-Host "Log file: $runLog"

& $PythonExe @arguments
exit $LASTEXITCODE

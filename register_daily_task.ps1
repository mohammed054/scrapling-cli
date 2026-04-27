param(
    [string]$TaskName = "Scrapling Daily Fetch",
    [string]$Time = "07:00",
    [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"

if ($Time -notmatch "^\d{2}:\d{2}$") {
    throw "Time must be in HH:MM 24-hour format."
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$runnerPath = Join-Path $repoRoot "auto_run.ps1"

if (-not (Test-Path $runnerPath)) {
    throw "Runner script not found: $runnerPath"
}

$taskCommand = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$runnerPath`" -PythonExe `"$PythonExe`""

schtasks /Create /SC DAILY /ST $Time /TN $TaskName /TR $taskCommand /F | Out-Null

Write-Host "Scheduled task created."
Write-Host "Task name: $TaskName"
Write-Host "Time: $Time"

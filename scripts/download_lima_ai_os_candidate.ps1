param(
    [string]$Repository = "armpit-symphony/LIMA-AI-OS",
    [string]$Branch = "docs-v1-post-g60-readiness-and-next-lane-matrix",
    [string]$DestinationRoot = (Join-Path $env:USERPROFILE "lima_build_sources"),
    [switch]$Install,
    [switch]$InstallDependencies,
    [switch]$SkipTests,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[lima-download] $Message"
}

$safeBranch = $Branch -replace "[^A-Za-z0-9._-]", "_"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$downloadDir = Join-Path $DestinationRoot "lima-ai-os-$safeBranch-$stamp"
$zipPath = Join-Path $downloadDir "source.zip"
$archiveUrl = "https://github.com/$Repository/archive/refs/heads/$Branch.zip"

Write-Step "CANDIDATE_ONLY downloader"
Write-Step "Repository: $Repository"
Write-Step "Branch: $Branch"
Write-Step "Destination: $downloadDir"
Write-Step "This does not claim product readiness or production readiness."

if ($DryRun) {
    Write-Step "DryRun selected; no network call or file write will occur."
    Write-Step "Would download: $archiveUrl"
    Write-Step "Would expand under: $downloadDir"
    if ($Install) {
        Write-Step "Would run candidate installer after expansion."
    }
    exit 0
}

New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null
Write-Step "Downloading source archive"
Invoke-WebRequest -Uri $archiveUrl -OutFile $zipPath

Write-Step "Expanding source archive"
Expand-Archive -Path $zipPath -DestinationPath $downloadDir -Force

$sourcePath = Get-ChildItem -Path $downloadDir -Directory |
    Where-Object { Test-Path (Join-Path $_.FullName "pyproject.toml") } |
    Select-Object -First 1

if ($null -eq $sourcePath) {
    throw "Downloaded archive did not contain a pyproject.toml source root."
}

Write-Step "Source ready: $($sourcePath.FullName)"

if ($Install) {
    $installer = Join-Path $sourcePath.FullName "scripts\install_lima_ai_os_candidate.ps1"
    if (-not (Test-Path $installer)) {
        throw "Installer script missing from downloaded source: $installer"
    }
    Write-Step "Running candidate installer"
    $installArgs = @("-ExecutionPolicy", "Bypass", "-File", $installer, "-SourcePath", $sourcePath.FullName)
    if ($InstallDependencies) {
        $installArgs += "-InstallDependencies"
    }
    if ($SkipTests) {
        $installArgs += "-SkipTests"
    }
    powershell @installArgs
}

Write-Step "Download complete"

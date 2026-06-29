param(
    [string]$SourcePath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$InstallRoot = (Join-Path $env:USERPROFILE ".lima-ai-os\candidate"),
    [switch]$InstallDependencies,
    [switch]$RunTests,
    [switch]$SkipTests,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[lima-install] $Message"
}

function Invoke-Checked {
    param(
        [string]$Executable,
        [string[]]$Arguments
    )
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Executable $($Arguments -join ' ')"
    }
}

$resolvedSource = (Resolve-Path $SourcePath).Path
$pyproject = Join-Path $resolvedSource "pyproject.toml"
if (-not (Test-Path $pyproject)) {
    throw "pyproject.toml not found under SourcePath: $resolvedSource"
}

$venvPath = Join-Path $InstallRoot ".venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"
$pipArgs = @("-m", "pip", "install", "-e", $resolvedSource)
if (-not $InstallDependencies) {
    $pipArgs += "--no-deps"
}

Write-Step "CANDIDATE_ONLY local install"
Write-Step "Source: $resolvedSource"
Write-Step "InstallRoot: $InstallRoot"
Write-Step "Dependencies: $([bool]$InstallDependencies)"
Write-Step "This does not claim product readiness or production readiness."

if ($DryRun) {
    Write-Step "DryRun selected; no files will be created."
    Write-Step "Would create venv: $venvPath"
    Write-Step "Would install package with: $pythonExe $($pipArgs -join ' ')"
    exit 0
}

New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
if (-not (Test-Path $pythonExe)) {
    Write-Step "Creating virtual environment"
    Invoke-Checked "python" @("-m", "venv", $venvPath)
}

Write-Step "Installing LIMA candidate package"
Invoke-Checked $pythonExe $pipArgs

Write-Step "Running import smoke"
Invoke-Checked $pythonExe @("-c", "import lima; import lima.harness.v1_local_document_harness; print('lima candidate import smoke: ok')")

if ($RunTests -and -not $SkipTests) {
    Write-Step "Running focused local document harness tests with workspace Python"
    Push-Location $resolvedSource
    try {
        Invoke-Checked "python" @("-m", "pytest", "-q", "tests\test_v1_local_document_harness.py", "-p", "no:cacheprovider")
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Step "Focused tests not run by installer. Run: python -m pytest -q tests\test_v1_local_document_harness.py -p no:cacheprovider"
}

Write-Step "Install complete"
Write-Step "Try: $pythonExe -m lima.harness.v1_local_document_harness --path C:\path\to\sample.txt"

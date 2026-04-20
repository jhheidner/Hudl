# Run pytest using the project virtual environment (avoids wrong Python on PATH).
# Usage: .\run_tests.ps1 -m smoke
#        .\run_tests.ps1 tests\smoke -v

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$py = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $py)) {
    Write-Host "No .venv found. Create it and install deps:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor Cyan
    Write-Host "  .\.venv\Scripts\python.exe -m pip install -r requirements.txt" -ForegroundColor Cyan
    exit 1
}

& $py -m pytest @args
exit $LASTEXITCODE

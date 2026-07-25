Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Creating virtual environment..."
python -m venv .venv
& .venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing packages in editable mode..."
python -m pip install `
  -e packages\domain-models `
  -e packages\shared-core `
  -e apps\api `
  -e services\market-data `
  -e services\strategy `
  -e services\portfolio `
  -e services\execution `
  -e services\risk

Write-Host "Installing development dependencies..."
python -m pip install ruff pyright pytest pytest-asyncio hypothesis

Write-Host "Setup complete. Activate with: .venv\Scripts\Activate.ps1"

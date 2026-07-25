Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Stopping local infrastructure..."
docker compose -f infrastructure\docker\docker-compose.yml down

Write-Host "Infrastructure stopped."

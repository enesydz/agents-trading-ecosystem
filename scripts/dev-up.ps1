Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Starting local infrastructure..."
docker compose -f infrastructure\docker\docker-compose.yml up -d

Write-Host "Waiting for services to be healthy..."
Start-Sleep -Seconds 5

Write-Host "Infrastructure ready:"
Write-Host "  Redis:      localhost:6379"
Write-Host "  PostgreSQL: localhost:5432"
Write-Host "  Prometheus: localhost:9090"
Write-Host "  Grafana:    localhost:3000"
Write-Host "  Loki:       localhost:3100"

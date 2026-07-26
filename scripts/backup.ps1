param([string]$OutputDirectory = ".\backups")
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
docker compose -f infrastructure/docker/docker-compose.yml exec -T postgres pg_dump -U agents agents | Out-File "$OutputDirectory\agents-$stamp.sql" -Encoding utf8
Write-Host "Backup written to $OutputDirectory\agents-$stamp.sql"

#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Starting local infrastructure..."
docker compose -f infrastructure/docker/docker-compose.yml up -d

echo "Waiting for services to be healthy..."
sleep 5

echo "Infrastructure ready:"
echo "  Redis:      localhost:6379"
echo "  PostgreSQL: localhost:5432"
echo "  Prometheus: localhost:9090"
echo "  Grafana:    localhost:3000"
echo "  Loki:       localhost:3100"

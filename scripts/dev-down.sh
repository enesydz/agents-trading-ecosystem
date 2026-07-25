#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Stopping local infrastructure..."
docker compose -f infrastructure/docker/docker-compose.yml down

echo "Infrastructure stopped."

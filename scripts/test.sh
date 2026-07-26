#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

echo "Running tests..."
pytest tests/ -q
pytest services/*/tests/ -q
pytest apps/*/tests/ -q
pytest services/backtest/tests/ -q
pytest agents/*/tests/ -q

echo "Tests complete."

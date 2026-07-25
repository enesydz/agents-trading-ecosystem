#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

echo "Running Ruff format check..."
ruff format --check apps services agents packages tests

echo "Running Ruff lint..."
ruff check apps services agents packages tests

echo "Running Pyright..."
pyright

echo "Linting complete."

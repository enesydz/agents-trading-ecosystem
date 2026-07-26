#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Creating virtual environment..."
python3.12 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing packages in editable mode..."
pip install \
  -e packages/domain-models \
  -e packages/shared-core \
  -e apps/api \
  -e services/market-data \
  -e services/strategy \
  -e services/portfolio \
  -e services/execution \
  -e services/risk \
  -e services/backtest \
  -e agents/trading-assistant \
  -e services/routing \
  -e services/optimization

echo "Installing development dependencies..."
pip install ruff pyright pytest pytest-asyncio hypothesis

echo "Setup complete. Activate with: source .venv/bin/activate"

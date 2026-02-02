#!/bin/bash
set -e

PYTHON=python3.12

echo "[1/3] Go to MarketSimulator/src"
cd MarketSimulator/src

echo "[2/3] Create venv (MarketSimulator/src/venv)"
$PYTHON -m venv venv

echo "[3/3] Activate venv + install requirements"
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "✅ Done. To run later:"
echo "source MarketSimulator/src/venv/bin/activate"

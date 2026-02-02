#!/bin/bash
set -e

PORT=5670
DEVICE=${1:-en0}

# Activer le venv MarketSimulator
source MarketSimulator/src/venv/bin/activate

echo "Using PORT=$PORT DEVICE=$DEVICE"
echo "Launching agents..."

python ScenarioGenerator/src/main.py --port $PORT --device $DEVICE &
PID_SCEN=$!

python MarketSimulator/src/main.py --port $PORT --device $DEVICE &
PID_MARK=$!

echo "Agents started:"
echo " ScenarioGenerator PID=$PID_SCEN"
echo " MarketSimulator   PID=$PID_MARK"
echo ""
echo "Press Ctrl+C to stop."

# Attendre Ctrl+C
trap "echo 'Stopping...'; kill $PID_SCEN $PID_MARK 2>/dev/null || true; exit 0" INT
while true; do sleep 1; done

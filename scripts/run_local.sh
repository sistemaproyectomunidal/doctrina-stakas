#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "Starting services from $ROOT_DIR, logs -> $LOG_DIR"

# Start e2b-monitor
nohup uvicorn services.e2b-monitor.main:app --host 0.0.0.0 --port 8101 > "$LOG_DIR/e2b-monitor.log" 2>&1 &
E2B_MONITOR_PID=$!
echo "e2b-monitor PID=$E2B_MONITOR_PID"

# Start ml-engine
nohup uvicorn services.ml-engine.main:app --host 0.0.0.0 --port 8102 > "$LOG_DIR/ml-engine.log" 2>&1 &
ML_ENGINE_PID=$!
echo "ml-engine PID=$ML_ENGINE_PID"

# Start social-automation
nohup uvicorn services.social-automation.main:app --host 0.0.0.0 --port 8103 > "$LOG_DIR/social-automation.log" 2>&1 &
SOCIAL_PID=$!
echo "social-automation PID=$SOCIAL_PID"

# Start music-production
nohup uvicorn services.music-production.main:app --host 0.0.0.0 --port 8104 > "$LOG_DIR/music-production.log" 2>&1 &
MUSIC_PID=$!
echo "music-production PID=$MUSIC_PID"

# Start orchestrator
nohup uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8100 > "$LOG_DIR/orchestrator.log" 2>&1 &
ORCH_PID=$!
echo "orchestrator PID=$ORCH_PID"

# Start command-interpreter
nohup uvicorn services.command-interpreter.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/command-interpreter.log" 2>&1 &
CMD_PID=$!
echo "command-interpreter PID=$CMD_PID"

# Start dashboard (streamlit)
nohup streamlit run dashboard/app.py --server.headless true --server.port 8501 > "$LOG_DIR/dashboard.log" 2>&1 &
DASH_PID=$!
echo "dashboard PID=$DASH_PID"

# Give services time to start
sleep 2

# Quick health check: call command-interpreter with a sample payload
echo "\nHealth check: calling Command Interpreter POST /api/command with {\"input\": \"status\"}"
HEALTH=$(curl -s -X POST -H "Content-Type: application/json" -d '{"input":"status"}' http://localhost:8000/api/command || true)

if [ -z "$HEALTH" ]; then
  echo "Command Interpreter did not respond yet. Check logs in $LOG_DIR"
else
  echo "Response from Command Interpreter:"
  echo "$HEALTH"
fi

echo "\nServices started. Logs: $LOG_DIR/*.log"

echo "$E2B_MONITOR_PID $ML_ENGINE_PID $SOCIAL_PID $MUSIC_PID $ORCH_PID $CMD_PID $DASH_PID" > "$ROOT_DIR/scripts/pids.txt"

exit 0

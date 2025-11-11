#!/usr/bin/env bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$ROOT/target/release/secure_resume"
PATTERN="target/release/secure_resume"

if [[ ! -x "$BIN" ]]; then
  echo "secure-resume binary not found at $BIN"
  exit 1
fi

pids="$(pgrep -f "$PATTERN")"

if [[ -z "$pids" ]]; then
  echo "secure-resume not running"
  exit 0
fi

echo "Stopping secure-resume (pid(s): $pids)..."
kill $pids 2>/dev/null || true
sleep 1

if pgrep -f "$PATTERN" >/dev/null; then
  echo "Forcing termination..."
  pkill -9 -f "$PATTERN" || true
fi

if pgrep -f "$PATTERN" >/dev/null; then
  echo "secure-resume still running; manual intervention needed."
  exit 1
else
  echo "secure-resume stopped"
fi


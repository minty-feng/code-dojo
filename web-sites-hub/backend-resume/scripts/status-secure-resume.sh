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
  exit 1
fi

echo "secure-resume running (pid(s): $pids)"

if command -v lsof >/dev/null 2>&1; then
  echo "Listening sockets:"
  lsof -Pan -p $pids -i
elif command -v netstat >/dev/null 2>&1; then
  echo "Listening sockets:"
  netstat -anp | grep "$pids"
else
  echo "Install lsof or netstat to see bound ports."
fi


#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8300}"
VENV_ACTIVATE="$ROOT/.venv/bin/activate"
PYTHON_BIN="${PYTHON_BIN:-python}"

if [ ! -f "app/main.py" ] || [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到 backend-platform-py 项目根目录"
    exit 1
fi

if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "错误: 未找到虚拟环境激活脚本: $VENV_ACTIVATE"
    exit 1
fi

# shellcheck disable=SC1090
source "$VENV_ACTIVATE"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "错误: 未找到 Python: $PYTHON_BIN"
    exit 1
fi

exec "$PYTHON_BIN" -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
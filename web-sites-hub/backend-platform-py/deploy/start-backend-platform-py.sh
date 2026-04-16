#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ACTION="${1:-start}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8300}"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"
ENV_FILE="${ENV_FILE:-$ROOT/deploy/config/backend-platform-py.env}"
LOG_FILE="${LOG_FILE:-$ROOT/backend-platform-py.log}"
PID_FILE="${PID_FILE:-$ROOT/backend-platform-py.pid}"

if [ ! -f "app/main.py" ] || [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到 backend-platform-py 项目根目录"
    exit 1
fi
echo "项目目录校验通过✅"

if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
    echo "环境变量文件加载通过✅ ($ENV_FILE)"
else
    echo "环境变量文件不存在，跳过加载✅ ($ENV_FILE)"
fi

get_running_pid() {
    if [ -f "$PID_FILE" ]; then
        local pid
        pid="$(cat "$PID_FILE" 2>/dev/null || true)"
        if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
            echo "$pid"
            return 0
        fi
    fi
    return 1
}

check_python() {
    if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
        echo "错误: 未找到 Python: $PYTHON_BIN"
        echo "安装提示: Ubuntu 可执行 sudo apt install -y python3.12 python3.12-venv"
        exit 1
    fi
    echo "Python 可执行文件校验通过✅ ($PYTHON_BIN)"

    if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)'; then
        echo "错误: 当前 Python 版本不是 3.12"
        echo "安装提示: 请安装 Python 3.12，并通过 PYTHON_BIN=python3.12 指定解释器"
        exit 1
    fi
    echo "Python 3.12 版本校验通过✅"
}

check_fastapi() {
    if ! "$PYTHON_BIN" -c "import fastapi" >/dev/null 2>&1; then
        echo "错误: 当前 Python 环境缺少 fastapi"
        echo "安装提示: $PYTHON_BIN -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
        exit 1
    fi
    echo "FastAPI 依赖校验通过✅"
}

stop_server() {
    local pid
    if pid="$(get_running_pid)"; then
        kill "$pid" 2>/dev/null || true
        sleep 1
        if kill -0 "$pid" 2>/dev/null; then
            echo "进程未退出，发送 SIGKILL: $pid"
            kill -9 "$pid" 2>/dev/null || true
        fi
        rm -f "$PID_FILE"
        echo "backend-platform-py 已停止 (pid $pid)"
    else
        rm -f "$PID_FILE"
        echo "backend-platform-py 未运行"
    fi
}

start_server() {
    local pid
    if pid="$(get_running_pid)"; then
        echo "backend-platform-py 已在运行 (pid $pid)"
        echo "日志文件: $LOG_FILE"
        exit 0
    fi

    rm -f "$PID_FILE"
    check_python
    check_fastapi

    echo "Starting backend-platform-py on http://$HOST:$PORT"
    nohup "$PYTHON_BIN" -m uvicorn app.main:app --host "$HOST" --port "$PORT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "backend-platform-py started (pid $(cat "$PID_FILE")), logging to $LOG_FILE"
    echo "服务启动完成✅"
}

case "$ACTION" in
    start)
        start_server
        ;;
    stop|kill)
        stop_server
        ;;
    restart)
        stop_server
        start_server
        ;;
    *)
        echo "用法: $0 [start|stop|kill|restart]"
        exit 1
        ;;
esac

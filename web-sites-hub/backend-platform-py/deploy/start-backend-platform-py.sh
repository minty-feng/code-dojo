#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ACTION="${1:-start}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8300}"
VENV_DIR="${VENV_DIR:-$ROOT/.venv}"
VENV_ACTIVATE="$VENV_DIR/bin/activate"
VENV_PYTHON="$VENV_DIR/bin/python"
ENV_FILE="${ENV_FILE:-$ROOT/deploy/backend-platform-py.env}"
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

get_pid_file_pid() {
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

get_port_pids() {
    local pids=""

    if command -v lsof >/dev/null 2>&1; then
        pids="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || true)"
    elif command -v ss >/dev/null 2>&1; then
        pids="$(ss -ltnp "sport = :$PORT" 2>/dev/null | grep -oE 'pid=[0-9]+' | cut -d= -f2 || true)"
    elif command -v fuser >/dev/null 2>&1; then
        pids="$(fuser -n tcp "$PORT" 2>/dev/null | tr -s ' ' '\n' | grep -E '^[0-9]+$' || true)"
    fi

    if [ -n "$pids" ]; then
        printf '%s\n' $pids
        return 0
    fi

    # 兜底：不依赖 lsof/ss，匹配本项目的 uvicorn 进程
    pgrep -f "uvicorn app\.main:app.*--port ${PORT}" 2>/dev/null || true
}

ensure_data_writable() {
    local data_dir="$ROOT/data"
    local db_file="$data_dir/app.db"
    mkdir -p "$data_dir"
    if [ ! -w "$data_dir" ]; then
        echo "错误: data/ 目录不可写: $data_dir"
        echo "请执行: sudo chown -R \$(whoami):\$(whoami) $data_dir && chmod 755 $data_dir"
        exit 1
    fi
    if [ -f "$db_file" ] && [ ! -w "$db_file" ]; then
        echo "错误: SQLite 数据库不可写: $db_file"
        echo "请执行: sudo chown \$(whoami):\$(whoami) $db_file && chmod 664 $db_file"
        exit 1
    fi
    echo "data/ 目录可写✅ ($data_dir)"
}

check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "错误: 未找到虚拟环境目录: $VENV_DIR"
        echo "请先执行: python3.12 -m venv .venv"
        exit 1
    fi

    if [ ! -f "$VENV_ACTIVATE" ] || [ ! -x "$VENV_PYTHON" ]; then
        echo "错误: .venv 不完整，缺少 activate 或 python 可执行文件"
        echo "请重建虚拟环境: rm -rf .venv && python3.12 -m venv .venv"
        exit 1
    fi
    echo ".venv 目录校验通过✅ ($VENV_DIR)"
}

activate_venv() {
    # shellcheck disable=SC1090
    source "$VENV_ACTIVATE"
    PYTHON_BIN="${PYTHON_BIN:-$VENV_PYTHON}"
    export PYTHON_BIN
    echo "虚拟环境激活通过✅ ($VENV_DIR)"
}

check_python() {
    if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
        echo "错误: 虚拟环境内未找到 Python: $PYTHON_BIN"
        exit 1
    fi
    echo "Python 可执行文件校验通过✅ ($PYTHON_BIN)"

    if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)'; then
        echo "错误: 当前 Python 版本不是 3.12"
        echo "请使用 Python 3.12 重建 .venv：rm -rf .venv && python3.12 -m venv .venv"
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
    local pid stopped=0
    while IFS= read -r pid; do
        [ -n "$pid" ] || continue
        kill "$pid" 2>/dev/null || true
        stopped=1
    done < <(get_port_pids | sort -u)

    if pid="$(get_pid_file_pid)"; then
        kill "$pid" 2>/dev/null || true
        stopped=1
    fi

    sleep 1

    while IFS= read -r pid; do
        [ -n "$pid" ] || continue
        if kill -0 "$pid" 2>/dev/null; then
            echo "端口 $PORT 仍被占用，发送 SIGKILL: $pid"
            kill -9 "$pid" 2>/dev/null || true
            stopped=1
        fi
    done < <(get_port_pids | sort -u)

    rm -f "$PID_FILE"
    if [ "$stopped" -eq 1 ]; then
        echo "backend-platform-py 已停止"
    elif [ -n "$(get_port_pids | head -1)" ]; then
        echo "警告: 仍有进程占用端口 $PORT，请手动检查: ps -ef | grep uvicorn"
    else
        echo "backend-platform-py 未运行"
    fi
}

start_server() {
    local pid
    if pid="$(get_pid_file_pid)"; then
        echo "backend-platform-py 已在运行 (pid $pid)"
        echo "日志文件: $LOG_FILE"
        exit 0
    fi
    if [ -n "$(get_port_pids | head -1)" ]; then
        echo "警告: 端口 $PORT 已被其他进程占用，请先执行: $0 stop"
        exit 1
    fi

    rm -f "$PID_FILE"
    ensure_data_writable
    check_venv
    activate_venv
    check_python
    check_fastapi

    echo "Starting backend-platform-py on http://$HOST:$PORT"
    nohup "$PYTHON_BIN" -m uvicorn app.main:app --host "$HOST" --port "$PORT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 1
    if ! kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "错误: 服务启动失败，最近日志:"
        tail -20 "$LOG_FILE" 2>/dev/null || true
        rm -f "$PID_FILE"
        exit 1
    fi
    if [ -n "$(get_port_pids | head -1)" ]; then
        echo "backend-platform-py started (pid $(cat "$PID_FILE")), logging to $LOG_FILE"
        echo "服务启动完成✅"
    else
        echo "错误: 进程已退出或未能监听 $PORT，最近日志:"
        tail -20 "$LOG_FILE" 2>/dev/null || true
        rm -f "$PID_FILE"
        exit 1
    fi
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

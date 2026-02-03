#!/bin/bash
# Rust 工具链安装脚本
# 使用方法：
#   1. 本地：scp scripts/install-rustup.sh user@server:/tmp/
#   2. 服务器：chmod +x /tmp/install-rustup.sh && /tmp/install-rustup.sh

set -e

echo "=========================================="
echo "  Rust 工具链安装脚本"
echo "=========================================="
echo ""

# 检查是否已安装 rustup
if command -v rustup &> /dev/null; then
    echo "✅ rustup 已安装"
    rustup --version
    echo ""
    echo "当前工具链："
    rustup show
    exit 0
fi

# 检查现有 Rust 安装
if command -v rustc &> /dev/null; then
    echo "⚠️  检测到系统已安装 Rust："
    rustc --version
    cargo --version 2>/dev/null || echo "  (cargo 未找到)"
    echo ""
    read -p "是否卸载系统 Rust 并安装 rustup？(y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 卸载系统 Rust..."
        if command -v apt-get &> /dev/null; then
            sudo apt remove -y rustc cargo 2>/dev/null || true
        elif command -v yum &> /dev/null; then
            sudo yum remove -y rust cargo 2>/dev/null || true
        fi
    else
        echo "❌ 取消安装"
        exit 1
    fi
fi

# 设置镜像源（解决网络问题）
echo "🌐 配置 Rust 镜像源..."
export RUSTUP_DIST_SERVER="${RUSTUP_DIST_SERVER:-https://mirrors.ustc.edu.cn/rust-static}"
export RUSTUP_UPDATE_ROOT="${RUSTUP_UPDATE_ROOT:-https://mirrors.ustc.edu.cn/rust-static/rustup}"

# 如果镜像源不可用，回退到官方源
if ! curl -s --connect-timeout 5 "${RUSTUP_DIST_SERVER}" > /dev/null 2>&1; then
    echo "⚠️  镜像源不可用，使用官方源"
    unset RUSTUP_DIST_SERVER
    unset RUSTUP_UPDATE_ROOT
fi

# 跳过路径检查（如果系统已有 Rust）
export RUSTUP_INIT_SKIP_PATH_CHECK=yes

echo "📥 下载并安装 rustup..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable

# 添加到 PATH
if [ -f "$HOME/.cargo/env" ]; then
    echo "📝 配置环境变量..."
    source "$HOME/.cargo/env"
    
    # 添加到 ~/.bashrc（如果不存在）
    if ! grep -q ".cargo/env" "$HOME/.bashrc" 2>/dev/null; then
        echo "" >> "$HOME/.bashrc"
        echo "# Rust environment" >> "$HOME/.bashrc"
        echo 'source "$HOME/.cargo/env"' >> "$HOME/.bashrc"
    fi
fi

echo ""
echo "=========================================="
echo "  ✅ 安装完成！"
echo "=========================================="
echo ""
echo "当前版本："
rustc --version
cargo --version
rustup --version
echo ""
echo "💡 提示："
echo "   - 如果当前 shell 未加载环境，运行: source \$HOME/.cargo/env"
echo "   - 查看工具链: rustup show"
echo "   - 更新工具链: rustup update"
echo ""


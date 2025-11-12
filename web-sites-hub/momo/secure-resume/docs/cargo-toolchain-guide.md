# Cargo 与 Rust 工具链指南

本文档介绍如何安装 Cargo、切换不同版本的 Cargo/Rust 工具链，以及查看当前的编译环境信息。内容适用于 macOS 与 Linux 系统，Windows 用户可参考 rustup 官方文档获取等效命令。**rustup 的许多命令既支持显式 `toolchain` 子命令，也支持省略 `toolchain` 的速记形式，本文会同时展示两种写法。**

## 1. 安装 Cargo（Rustup）

Rust 官方推荐使用 **rustup** 管理工具链。安装完成后会同时获取最新稳定版的 `cargo`、`rustc` 和相关组件。

### 1.1 在线安装

```bash
# 交互式安装脚本
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

- 安装过程会提示选择默认配置（按 `1`）。
- 安装完成后按提示执行 `source $HOME/.cargo/env` 使环境变量生效。
- 终端重新打开后，`cargo`、`rustc`、`rustup` 即可使用。

### 1.2 手动配置环境变量

如果终端尚未识别 `cargo`，手动添加以下内容至 `~/.bashrc` 或 `~/.zshrc`：

```bash
export CARGO_HOME="$HOME/.cargo"
export PATH="$CARGO_HOME/bin:$PATH"
```

保存后执行 `source ~/.zshrc`（或对应 shell）即可。

## 2. 切换 Cargo/Rust 版本

Rustup 通过“工具链（toolchain）”管理不同版本。常见工具链名称：

- `stable`：稳定版（默认安装）
- `beta`：测试版
- `nightly`：每日构建
- `1.77.0`：指定版本号

### 2.1 安装其他工具链

```bash
# 等价写法一（显式）
rustup toolchain install beta
rustup toolchain install nightly
rustup toolchain install 1.75.0

# 等价写法二（速记）
rustup install beta
rustup install nightly
rustup install 1.75.0
```

### 2.2 全局切换默认工具链

```bash
rustup default nightly   # 设置默认工具链为 nightly
rustup default stable    # 恢复为 stable
```

> 说明：`rustup default` 本身已是最简写法（内部等同于 `rustup toolchain default`）。

执行 `rustup default` 可查看当前默认工具链。

### 2.3 针对项目使用特定版本

在项目根目录创建或编辑 `rust-toolchain.toml`：

```toml
[toolchain]
channel = "1.75.0"
components = ["rustfmt", "clippy"]
```

Rustup 会在进入该目录时自动切换到指定工具链。

若希望临时切换，可使用覆盖（override）：

```bash
rustup override set 1.75.0
rustup override unset       # 移除覆盖
```

### 2.4 临时使用其他版本

```bash
# 使用 nightly 构建（不改变默认）
rustup run nightly cargo build

# 使用指定版本执行测试
rustup run 1.75.0 cargo test
```

## 3. 查看 Rust 编译环境

### 3.1 基本版本信息

```bash
rustc --version        # Rust 编译器版本
cargo --version        # Cargo 版本
rustup --version       # rustup 版本
```

### 3.2 查看当前工具链状态

```bash
rustup show
```

输出内容包含：
- `Default host`：当前平台三元组（如 `x86_64-apple-darwin`）。
- `active toolchain`：当前激活的工具链及其路径。
- `installed toolchains`：已安装的所有工具链列表。
- `installed targets`：每个工具链可用的目标平台。

### 3.3 列出已安装组件

```bash
rustup component list --installed
```

可用于确认 `rustfmt`、`clippy` 等工具是否已安装。

### 3.4 检查可用目标列表

```bash
# 查看当前工具链支持的编译目标
rustup target list --installed

# 查看 nightly 工具链支持的目标
rustup target list --toolchain nightly
```

对应速记：

```bash
rustup target list --installed               # 等同 rustup toolchain target list --installed
rustup target list --toolchain nightly       # 等同 rustup toolchain target list nightly
```

### 3.5 查看 Cargo 配置与项目元数据

```bash
cargo locate-project     # 当前项目的 Cargo.toml 位置
cargo metadata --format-version=1 --no-deps
```

`cargo metadata` 可输出项目依赖关系、构建目标等信息，便于调试 CI 或构建脚本。

## 4. 常用维护命令

```bash
# 更新 rustup 自身及所有默认组件
rustup self update
rustup update             # 等同于 rustup toolchain update

# 升级特定工具链
rustup update stable
rustup update nightly

# 卸载工具链（两种写法）
rustup toolchain uninstall 1.70.0
rustup uninstall 1.70.0

# 清理缓存
cargo clean               # 清理 target 目录
rustup cache prune        # 清理 rustup 下载缓存
```

## 5. 参考链接

- Rustup 官方文档: <https://rust-lang.github.io/rustup/>
- Rust 安装指南: <https://www.rust-lang.org/zh-CN/tools/install>
- Cargo 手册: <https://doc.rust-lang.org/cargo/>

> 提示：本文档位于 `docs/cargo-toolchain-guide.md`，如需在团队内部分享可将其纳入知识库或 CI 初始化脚本。
# OpenClaw 本地安装与使用（macOS）

## 1. 文档说明

- **OpenClaw** 指 [openclaw.ai](https://openclaw.ai) 的 **自托管 AI Gateway**：把 Telegram、Slack、WhatsApp 等渠道接到你的模型与智能体，并带 Web 控制台（Control UI）。
- **本文范围**：在 **macOS** 上完成 CLI 安装、Onboarding、守护进程与 Dashboard 验证。
- **非本文范围**：与同名游戏重制项目（Captain Claw 的 OpenClaw）无关。
- **官方文档**：[Getting Started](https://docs.openclaw.ai/start/getting-started)、[中文首页](https://docs.openclaw.ai/zh-CN)、[文档索引](https://docs.openclaw.ai/llms.txt)。

---

## 2. 环境与前置条件

| 项目 | 要求 |
|------|------|
| 操作系统 | macOS（建议较新版本） |
| Shell | zsh（系统默认） |
| Node.js | **22.14+**；官方推荐 **Node 24** |
| 网络 | 能访问 npm、GitHub、OpenClaw 安装源；国内环境建议配置 HTTP(S) 代理 |
| 模型 | 至少一个提供商的 **API Key**（Onboarding 时会提示） |

检查命令：

```bash
node --version
npm --version
curl --version
git --version
```

---

## 3. 安装 Node.js（版本不足时）

若 `node -v` 低于 22.14，请先升级。推荐使用 **nvm**：

```bash
brew install nvm
mkdir -p ~/.nvm

echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$(brew --prefix nvm)/nvm.sh" ] && . "$(brew --prefix nvm)/nvm.sh"' >> ~/.zshrc

source ~/.zshrc
nvm install 24
nvm use 24
nvm alias default 24

node -v
npm -v
```

---

## 4. 安装 OpenClaw

### 4.1 官方一键安装（推荐）

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 4.2 备选：npm 全局安装

```bash
npm install -g openclaw@latest
```

### 4.3 验证

```bash
openclaw --version
```

---

## 5. 命令找不到：PATH 修复

若出现 `openclaw: command not found`，将常见安装路径加入 `PATH`：

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

which openclaw
openclaw --version
```

---

## 6. 初始化（Onboarding）与守护进程

完成向导并安装后台服务：

```bash
openclaw onboard --install-daemon
```

向导通常包括：选择模型提供商、填写 API Key、写入配置、安装并启动 Gateway 守护进程。

---

## 7. 验证 Gateway

```bash
openclaw gateway status
```

正常情况下服务在运行；控制台默认多为 **`http://127.0.0.1:18789`**（以实际输出为准）。

---

## 8. 打开控制台（Dashboard）

```bash
openclaw dashboard
```

在浏览器中发一条消息，确认能收到模型回复。

---

## 9. 常用运维命令

```bash
openclaw gateway status    # 状态
openclaw gateway restart   # 重启
openclaw gateway stop      # 停止
openclaw gateway start     # 启动
openclaw logs --follow     # 实时日志
```

若当前 CLI 版本提供诊断命令，可执行：

```bash
openclaw doctor
```

（以本机 `openclaw --help` 为准。）

---

## 10. 配置与数据路径

| 说明 | 路径 |
|------|------|
| 主配置（JSON/JSON5） | `~/.openclaw/openclaw.json` |

高级用法（如自定义 Control UI 静态资源）见官方 [Getting Started](https://docs.openclaw.ai/start/getting-started) 中的 `gateway.controlUi.root` 说明。

### 环境变量（服务账号或自定义目录）

| 变量 | 含义 |
|------|------|
| `OPENCLAW_HOME` | 内部路径解析用的主目录 |
| `OPENCLAW_STATE_DIR` | 状态目录覆盖 |
| `OPENCLAW_CONFIG_PATH` | 配置文件路径覆盖 |

完整说明：[Environment variables](https://docs.openclaw.ai/help/environment)。

---

## 11. 国内网络与代理

安装或拉依赖超时，可先设置代理再执行安装（端口按本机代理修改）：

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
curl -fsSL https://openclaw.ai/install.sh | bash
```

持久化示例：

```bash
echo 'export http_proxy=http://127.0.0.1:7890' >> ~/.zshrc
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.zshrc
source ~/.zshrc
```

---

## 12. 常见问题排查

### 12.1 `command not found`

按 **第 5 节** 修复 PATH，重开终端或 `source ~/.zshrc`。

### 12.2 Node 版本不满足

按 **第 3 节** 升级到 Node 24（或至少 22.14+）。

### 12.3 Dashboard 打不开

1. `openclaw gateway status`
2. `openclaw gateway restart`
3. `openclaw logs --follow`
4. 检查端口占用：`lsof -i :18789`

### 12.4 有 API Key 仍无回复

- 核对提供商与 Key 是否匹配、额度与权限。
- 从日志中查看认证错误、限流或网络错误。

### 12.5 一键脚本失败

- 确认 `curl`、`node`、`npm` 可用。
- 开启代理后重试，或改用 **第 4.2 节** npm 安装。

---

## 13. 最短「从零到可用」命令序列

```bash
node -v
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw --version
openclaw onboard --install-daemon
openclaw gateway status
openclaw dashboard
```

---

## 14. 延伸阅读

- [Getting Started（英文）](https://docs.openclaw.ai/start/getting-started)
- [Install 汇总](https://docs.openclaw.ai/install)
- [Node 安装说明](https://docs.openclaw.ai/install/node)
- [Channels（各渠道配置）](https://docs.openclaw.ai/channels)
- [Troubleshooting](https://docs.openclaw.ai/help/faq)

# 🧭 Clash Meta 专业安装与配置指南（Ubuntu）

## 📘 一、前言

Clash Meta（全称 *Clash.Meta*）是 Clash 的高级分支版本，支持更多协议（如 Hysteria、TUIC、Reality、ShadowTLS 等），常用于科学上网、内网穿透或流量分流控制。

---

## ⚙️ 二、环境要求

* 操作系统：Ubuntu 20.04 / 22.04 / 24.04

* 权限：`sudo`

* 必要工具：

  ```bash
  sudo apt update
  sudo apt install -y curl wget vim unzip
  ```
---

## 📦 三、客户端安装 Clash Verge

```
https://github.com/clash-verge-rev/clash-verge-rev
```


---

## 📦 四、命令行安装 Clash Meta

### 1. 下载最新版本（自动识别架构）

```bash
#https://github.com/WindSpiritSR/clash/releases
wget -O clash-meta.gz https://github.com/WindSpiritSR/clash/releases/download/v1.18.0/clash-linux-amd64-v3-v1.18.0.gz #https://github.com/WindSpiritSR/clash

wget -O mihomo.gz https://github.com/MetaCubeX/mihomo/releases/download/v1.19.16/mihomo-darwin-amd64-v1.19.16.gz #貌似也可以 https://github.com/MetaCubeX/mihomo/wiki/FAQ

gunzip clash-meta.gz
chmod +x clash-meta
```

### 2. 验证安装

```bash
./clash-meta -v
```

可以看到类似输出：

```
Clash.Meta v1.x.x linux amd64 ...
```

---

## 📁 五、配置文件结构

在 `~/.config/clash/` 下创建配置目录：

```bash
mkdir -p ~/.config/clash
cd ~/.config/clash
```

### 1. 使用订阅链接自动配置（推荐）

如果你有订阅链接，可以直接下载配置：

```bash
# 创建配置目录
mkdir -p ~/.config/clash
cd ~/.config/clash

# 下载订阅配置（直接保存为 config.yaml）
curl -L -o config.yaml "https://example.com/sub?target=clash"

# 或使用 wget
wget -O config.yaml "https://example.com/sub?target=clash"
```

**注意事项：**

- 订阅配置通常已包含完整的代理节点、规则和代理组
- 如果订阅配置缺少某些设置（如 `external-ui`、`allow-lan`），可以手动编辑 `config.yaml` 添加
- 建议在下载前备份现有配置（如果有）：
  ```bash
  cp ~/.config/clash/config.yaml ~/.config/clash/config.yaml.bak
  ```

### 2. 手动创建主配置文件：`config.yaml`

```yaml
mixed-port: 7890
allow-lan: true
bind-address: "*"
external-controller: 0.0.0.0:9090
external-ui: /root/clash-meta/ui
secret: ""    # 如果想要免密登录 Web UI，保持为空
log-level: info

dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  nameserver:
    - 1.1.1.1
    - 8.8.8.8
  fallback:
    - https://1.1.1.1/dns-query
    - https://8.8.8.8/dns-query

# 代理节点 (示例)
proxies:
  - { name: "🇸🇬 SG", type: ss, server: 1.2.3.4, port: 443, cipher: aes-128-gcm, password: "xxx" }

proxy-groups:
  - name: "AUTO"
    type: select
    proxies:
      - 🇸🇬 SG
      - DIRECT

rules:
  - GEOIP,CN,DIRECT
  - MATCH,AUTO
```

---

## 🧩 六、配置 Web 控制台（Clash Dashboard）

### 1. 下载 UI 前端（Yacd 或  ）

```bash
cd ~/clash-meta
wget https://github.com/MetaCubeX/Yacd-meta/archive/refs/heads/gh-pages.zip -O ui.zip
unzip ui.zip
mv Yacd-meta-gh-pages ~/.config/clash/ui
```

### 2. 启动 Clash Meta

```bash
cd ~/clash-meta
./clash-meta -d ~/.config/clash/
```

若想后台运行：

```bash
nohup ./clash-meta -d ~/.config/clash/ > clash.log 2>&1 &
```

---

## 🌐 七、访问 Web 控制面板

在浏览器中打开：

```
http://129.28.85.223:9090/ui/#/proxies
```

若显示 "需要输入 Secret"：

👉 确认 `config.yaml` 中：

```yaml
secret: ""
```

并重启 Clash Meta。

若仍提示密码，可清理浏览器缓存后再试。

---

## 🧰 七、系统代理设置（可选）

### Linux 临时代理

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

### 永久生效（添加到 `~/.bashrc`）

```bash
echo 'export http_proxy=http://127.0.0.1:7890' >> ~/.bashrc
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.bashrc
source ~/.bashrc
```

---

## 🌍 八、其他机器使用代理服务

### 服务器端配置（129.28.85.223）

#### 1. 确保 Clash Meta 允许局域网访问

检查 `config.yaml` 配置：

```yaml
allow-lan: true          # 必须为 true
bind-address: "*"        # 监听所有网卡
mixed-port: 7890         # 代理端口
external-controller: 0.0.0.0:9090  # Web UI 端口
```

#### 2. 配置防火墙（Ubuntu/Debian）

```bash
# 开放代理端口 7890（HTTP/HTTPS 代理）
sudo ufw allow 7890/tcp

# 开放 Web UI 端口 9090（可选，仅管理需要）
sudo ufw allow 9090/tcp

# 开放 DNS 端口 53（如果使用 Clash DNS）
sudo ufw allow 53/udp

# 查看防火墙状态
sudo ufw status
```

#### 3. 如果使用云服务器，还需在云控制台配置安全组

- **阿里云/腾讯云/AWS**：在安全组规则中开放端口 `7890`、`9090`、`53`
- **协议类型**：TCP（7890, 9090）、UDP（53）

---

### 客户端配置（其他机器）

#### Windows 系统

**方法 1：系统代理设置**

1. 打开「设置」→「网络和 Internet」→「代理」
2. 手动设置代理：
   - 地址：`129.28.85.223`
   - 端口：`7890`
   - 勾选「对所有协议使用相同的代理服务器」

**方法 2：使用 Clash for Windows**

1. 下载 [Clash for Windows](https://github.com/Fndroid/clash_for_windows_pkg/releases)
2. 在「Profiles」中添加远程配置：
   ```
   http://129.28.85.223:9090/ui/yacd
   ```
   或直接使用 API：
   ```
   http://129.28.85.223:9090
   ```

**方法 3：环境变量（命令行）**

```cmd
# CMD
set http_proxy=http://129.28.85.223:7890
set https_proxy=http://129.28.85.223:7890

# PowerShell
$env:http_proxy="http://129.28.85.223:7890"
$env:https_proxy="http://129.28.85.223:7890"
```

---

#### macOS 系统

**方法 1：系统代理设置**

1. 打开「系统设置」→「网络」→ 选择当前网络 →「详细信息」→「代理」
2. 勾选「网页代理(HTTP)」和「安全网页代理(HTTPS)」
3. 服务器：`129.28.85.223`，端口：`7890`

**方法 2：使用 ClashX 或 ClashX Pro**

1. 下载 [ClashX](https://github.com/yichengchen/clashX/releases)
2. 配置远程 API：
   - API 地址：`http://129.28.85.223:9090`
   - Secret：留空（如果服务器未设置密码）

**方法 3：环境变量（终端）**

```bash
export http_proxy=http://129.28.85.223:7890
export https_proxy=http://129.28.85.223:7890
```

---

#### Linux 系统

**方法 1：环境变量**

```bash
# 临时设置
export http_proxy=http://129.28.85.223:7890
export https_proxy=http://129.28.85.223:7890

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export http_proxy=http://129.28.85.223:7890' >> ~/.bashrc
echo 'export https_proxy=http://129.28.85.223:7890' >> ~/.bashrc
source ~/.bashrc
```

**方法 2：使用 Clash for Linux**

```bash
# 下载 Clash
wget https://github.com/Dreamacro/clash/releases/latest/download/clash-linux-amd64 -O clash
chmod +x clash

# 配置 config.yaml，设置外部控制器
external-controller: http://129.28.85.223:9090
```

**方法 3：系统代理（GNOME/KDE）**

- GNOME：设置 → 网络 → 网络代理 → 手动 → 填入 `129.28.85.223:7890`
- KDE：系统设置 → 网络 → 代理 → 手动配置

---

#### 移动设备（iOS/Android）

**iOS（iPhone/iPad）**

1. 设置 → Wi-Fi → 点击当前网络右侧的「i」
2. 滚动到底部 →「配置代理」→「手动」
3. 服务器：`129.28.85.223`，端口：`7890`

**Android**

1. 设置 → Wi-Fi → 长按当前网络 →「修改网络」
2. 高级选项 → 代理 →「手动」
3. 主机名：`129.28.85.223`，端口：`7890`

**或使用 Clash 客户端：**

- iOS：[Shadowrocket](https://apps.apple.com/app/shadowrocket/id932747118) / [Stash](https://apps.apple.com/app/stash/id1596063349)
- Android：[Clash for Android](https://github.com/Kr328/ClashForAndroid/releases)

在客户端中添加远程配置：
```
http://129.28.85.223:9090
```

---

### 访问 Web 控制面板（其他机器）

在浏览器中打开：

```
http://129.28.85.223:9090/ui/#/proxies
```

可以：
- 查看代理节点状态
- 切换代理节点
- 查看流量统计
- 修改规则

---

### 验证代理是否生效

在客户端机器上执行：

```bash
# 查看当前 IP
curl ipinfo.io

# 或使用其他服务
curl ifconfig.me
curl ip.sb
```

如果返回的 IP 地址与服务器 IP（129.28.85.223）不同，说明代理成功。

---

## 🔄 八、验证是否代理成功

```bash
curl ipinfo.io
```

如果返回的 IP 显示为香港、日本等地，说明代理生效。

---

## 🧱 九、可选进阶：Systemd 自启动服务

创建 systemd 服务：

```bash
sudo vim /etc/systemd/system/clash-meta.service
```

写入：

```ini
[Unit]
Description=Clash Meta Service
After=network.target

[Service]
Type=simple
ExecStart=/home/ubuntu/clash-meta/clash-meta -d /home/ubuntu/.config/clash/
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动并设置开机自启：

```bash
sudo systemctl daemon-reload
sudo systemctl enable clash-meta
sudo systemctl start clash-meta
```

---

## 🔒 十、安全建议

1. 若服务器公网开放端口 `9090`，建议配置密码：

   ```yaml
   secret: "YourStrongPassword"
   ```

2. 或在防火墙中仅允许特定 IP 访问：

   ```bash
   sudo ufw allow from <your-ip> to any port 9090
   ```

---

## 🧠 十一、常见问题

| 问题           | 原因                             | 解决                          |
| ------------ | ------------------------------ | --------------------------- |
| `/ui` 返回 404 | UI 路径未配置正确                     | 检查 `external-ui` 指向的文件夹存在   |
| 提示需要密码       | `config.yaml` 中 `secret` 未设置为空 | 设置 `secret: ""`             |
| curl 无法代理    | 环境变量未导出                        | `export http_proxy=...` 后重试 |
| Web UI 空白    | 前端文件未完整下载                      | 重新下载 Yacd-meta gh-pages     |

---

## ✅ 十二、总结

你现在已拥有：

* ✅ Clash Meta 核心程序
* ✅ 可视化控制台（Yacd-meta）
* ✅ 全局代理功能
* ✅ 可选的 systemd 自启动

---

## 🔗 相关资源

* [Clash Meta GitHub](https://github.com/MetaCubeX/Clash.Meta)
* [Yacd-meta Dashboard](https://github.com/MetaCubeX/Yacd-meta)
* [Clash 配置文档](https://clash-meta.gitbook.io/meta/)


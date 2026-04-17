# Clash Meta（Mihomo）安装与配置指南（Ubuntu）


## 1. 前言

**Clash Meta / Mihomo** 是 Clash 的增强分支，支持更多协议（如 Hysteria、TUIC、Reality 等），常用于规则分流、透明代理或局域网共享代理。桌面端也可直接使用 **[Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev)** 等 GUI，本指南侧重 **无图形界面的 Ubuntu 服务端**。

## 2. 环境要求

- 系统：Ubuntu 20.04 / 22.04 / 24.04（其它 Debian 系类似）
- 权限：`sudo`
- 基础工具：

```bash
sudo apt update
sudo apt install -y curl wget vim unzip
```

## 3. 获取二进制（推荐官方 Mihomo）

在 [MetaCubeX/mihomo Releases](https://github.com/MetaCubeX/mihomo/releases) 下载对应 **OS + 架构** 的包（文件名通常含 `linux-amd64`、`linux-arm64` 等），勿把 **darwin**（macOS）包放到 Linux 上运行。

示例（**URL 与文件名以 [Releases](https://github.com/MetaCubeX/mihomo/releases) 页面为准**，勿照抄过期版本号）：

```bash
mkdir -p ~/clash-meta && cd ~/clash-meta
# 从 Release 页复制 linux-amd64（或 arm64）对应的 .gz 直链，例如：
# wget -O mihomo.gz 'https://github.com/MetaCubeX/mihomo/releases/download/vX.Y.Z/mihomo-linux-amd64-vX.Y.Z.gz'
gunzip -f mihomo.gz && chmod +x mihomo
mv mihomo clash-meta   # 可选：沿用习惯命令名
./clash-meta -v
```

若需其它 fork 的构建，请自行核对仓库说明与校验和。

**备选：sing-box**（通用代理平台，**配置为 JSON**，与 Clash `config.yaml` 不通用；版本与架构以 [SagerNet/sing-box Releases](https://github.com/SagerNet/sing-box/releases) 为准）：

```bash
mkdir -p ~/sing-box && cd ~/sing-box
wget -O singbox.tar.gz https://github.com/SagerNet/sing-box/releases/download/v1.13.7/sing-box-1.13.7-linux-amd64.tar.gz
tar xzf singbox.tar.gz
# 解压后进入带版本号的目录，可执行文件一般为 ./sing-box
./sing-box-1.13.7-linux-amd64/sing-box version
```

## 4. 配置目录与订阅

数据目录一般为 `~/.config/clash/`：

```bash
mkdir -p ~/.config/clash
cd ~/.config/clash
```

**有订阅时**：将订阅生成的 Clash 配置保存为 `config.yaml`（下载前建议备份）：

```bash
cp -n config.yaml config.yaml.bak 2>/dev/null || true
curl -fsSL -o config.yaml "https://example.com/sub?target=clash"
# 或 wget -O config.yaml "https://..."
```

**最小示例**（无订阅时仅作结构参考，节点需替换为真实信息）：

```yaml
mixed-port: 7890
allow-lan: true
bind-address: "*"
external-controller: 0.0.0.0:9090
external-ui: /home/YOUR_USER/.config/clash/ui
secret: ""          # 公网暴露控制台时务必改为强密码，见下文「安全」
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

proxies:
  - { name: "SG", type: ss, server: 1.2.3.4, port: 443, cipher: aes-128-gcm, password: "xxx" }

proxy-groups:
  - name: "AUTO"
    type: select
    proxies: [SG, DIRECT]

rules:
  - GEOIP,CN,DIRECT
  - MATCH,AUTO
```

注意：`external-ui` 必须指向 **已解压的 Web UI 静态文件目录**（见下一节），且路径与运行用户一致。

## 5. Web 控制台（Yacd-meta）

```bash
cd ~/.config/clash
wget -O ui.zip https://github.com/MetaCubeX/Yacd-meta/archive/refs/heads/gh-pages.zip
unzip -q ui.zip && mv Yacd-meta-gh-pages ui && rm ui.zip
```

启动（`-d` 指定配置目录）：

```bash
cd ~/clash-meta   # 二进制所在目录
./clash-meta -d ~/.config/clash/
```

后台运行示例：

```bash
nohup ./clash-meta -d ~/.config/clash/ > ~/.config/clash/clash.log 2>&1 &
```

浏览器访问（将 `YOUR_SERVER_IP` 换成公网或内网 IP）：

```text
http://YOUR_SERVER_IP:9090/ui/#/proxies
```

若提示需要 Secret：在 `config.yaml` 中设置 `secret: ""` 后重启；若仍异常可清理浏览器缓存。**公网开放 9090 时不建议使用空密码。**

## 6. 本机环境变量代理（Linux）

临时：

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

写入 `~/.bashrc` 或 `~/.zshrc` 可长期生效（按需修改 shell 配置文件）。

## 7. 局域网或其它机器使用同一台服务器代理

以下用占位符 **`YOUR_SERVER_IP`** 表示运行 Clash 的机器地址（内网或公网）。

### 7.1 服务端检查清单

`config.yaml` 中建议：

```yaml
allow-lan: true
bind-address: "*"
mixed-port: 7890
external-controller: 0.0.0.0:9090
```

**防火墙（UFW 示例）**：

```bash
sudo ufw allow 7890/tcp
sudo ufw allow 9090/tcp    # 仅管理需要时开放；可限制来源 IP
sudo ufw allow 53/udp      # 若使用 Clash 在 53 提供 DNS
sudo ufw status
```

云主机还需在 **安全组** 中放行相同端口（TCP/UDP 与上文一致）。

### 7.2 客户端怎么连

| 场景 | 做法 |
|------|------|
| Windows / macOS GUI | 系统代理或 Clash 系客户端中，HTTP/HTTPS 代理填 `YOUR_SERVER_IP`，端口 `7890` |
| 终端 | `export http_proxy=http://YOUR_SERVER_IP:7890` 与 `https_proxy` 同上 |
| 手机 Wi‑Fi 代理 | 手动代理：主机 `YOUR_SERVER_IP`，端口 `7890` |

管理面板 URL：`http://YOUR_SERVER_IP:9090/ui/#/proxies`（勿将 9090 暴露给不可信网络且无密码）。

### 7.3 验证

在 **客户端** 执行：

```bash
curl -sS https://ipinfo.io
# 或 curl -sS https://ifconfig.me
```

若出口 IP 与预期代理线路一致（且与直连不同），说明流量已走代理。

## 8. systemd 自启动（可选）

将路径改成你的实际用户与二进制位置：

```bash
sudo vim /etc/systemd/system/clash-meta.service
```

```ini
[Unit]
Description=Clash Meta (Mihomo)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_LINUX_USER
ExecStart=/home/YOUR_LINUX_USER/clash-meta/clash-meta -d /home/YOUR_LINUX_USER/.config/clash/
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now clash-meta
sudo systemctl status clash-meta
```

## 9. 安全建议

1. **公网** 开放 `9090` 时：设置强 `secret`，并优先用防火墙限制来源 IP，例如：  
   `sudo ufw allow from YOUR_ADMIN_IP to any port 9090`
2. 仅内网使用时也应避免弱口令与不必要的端口暴露。
3. 订阅链接、节点与日志可能含敏感信息，注意文件权限与备份位置。

## 10. 常见问题

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| `/ui` 404 | `external-ui` 路径错误或未解压 | 确认目录存在且与配置一致 |
| 一直要密码 | `secret` 非空或与面板不一致 | 修改 `config.yaml` 并重启 |
| curl 不走代理 | 未设置 `http_proxy`/`https_proxy` | 导出变量或使用支持代理的客户端 |
| Web UI 空白 | UI 文件不完整 | 重新下载解压 Yacd-meta gh-pages 分支 |

## 11. 相关链接

- [Mihomo（Clash Meta）](https://github.com/MetaCubeX/mihomo)
- [Yacd-meta](https://github.com/MetaCubeX/Yacd-meta)
- [Meta 文档](https://wiki.metacubex.one/)

# TCP/IP协议详解

## 💡 核心结论

1. **TCP三次握手建立连接，四次挥手断开连接**
2. **TCP通过序列号、确认号、重传实现可靠传输**
3. **滑动窗口控制流量，慢启动和拥塞避免控制拥塞**
4. **TIME_WAIT状态防止旧连接数据包干扰新连接**
5. **UDP无连接、不可靠，但延迟低，适合实时应用**

---

## 1. TCP/IP模型

### 1.1 四层模型

```
应用层    HTTP, FTP, DNS, SMTP
    ↓
传输层    TCP, UDP
    ↓
网络层    IP, ICMP, ARP
    ↓
链路层    Ethernet, WiFi
```

### 1.2 数据封装

```
应用数据
    ↓
[TCP头部 | 应用数据]          TCP段（Segment）
    ↓
[IP头部 | TCP头部 | 应用数据]   IP数据包（Packet）
    ↓
[以太网头部 | IP数据包 | 尾部]   以太网帧（Frame）
```

---

## 2. TCP协议

### 2.1 TCP头部格式

```c
struct tcp_header {
    uint16_t source_port;      // 源端口
    uint16_t dest_port;        // 目标端口
    uint32_t seq_num;          // 序列号
    uint32_t ack_num;          // 确认号
    uint8_t  data_offset : 4;  // 头部长度
    uint8_t  reserved : 4;     // 保留
    uint8_t  flags;            // 标志位
    // URG, ACK, PSH, RST, SYN, FIN
    uint16_t window;           // 窗口大小
    uint16_t checksum;         // 校验和
    uint16_t urgent_ptr;       // 紧急指针
    // 可选项...
};
```

**关键字段**：
- **seq_num**：本次发送数据的第一个字节的序列号
- **ack_num**：期望接收的下一个字节的序列号
- **flags**：控制标志（SYN, ACK, FIN, RST等）
- **window**：接收窗口大小

### 2.2 三次握手

```
客户端                                  服务器
  │                                       │
  │── SYN seq=x ───────────────────────→ │  LISTEN
  │                                       │  SYN_RCVD
  │←─ SYN+ACK seq=y, ack=x+1 ────────── │
  │                                       │
  │── ACK seq=x+1, ack=y+1 ────────────→ │  ESTABLISHED
  │                                       │
ESTABLISHED                           ESTABLISHED
```

**为什么是三次？**
1. **第一次**：客户端告诉服务器"我要连接你"
2. **第二次**：服务器回复"我收到了，我也要连接你"
3. **第三次**：客户端确认"好的，连接建立"

**防止历史连接**：
```
如果只有两次握手：
1. 客户端发送SYN（但网络延迟）
2. 客户端超时重发SYN
3. 服务器收到第二个SYN，回复SYN+ACK
4. 连接建立，正常通信
5. 第一个延迟的SYN到达服务器
6. 服务器又建立一个连接（错误！）

三次握手可以让客户端拒绝旧的SYN+ACK
```

**代码示例**：
```c
// 客户端
int sockfd = socket(AF_INET, SOCK_STREAM, 0);

struct sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

// 发起三次握手
connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
```

### 2.3 四次挥手

```
客户端                                  服务器
  │                                       │
  │── FIN seq=u ───────────────────────→ │  CLOSE_WAIT
FIN_WAIT_1                                │
  │                                       │
  │←─ ACK ack=u+1 ──────────────────── │
FIN_WAIT_2                                │
  │                                       │
  │←─ FIN seq=v ───────────────────── │  LAST_ACK
TIME_WAIT                                 │
  │                                       │
  │── ACK ack=v+1 ────────────────────→ │  CLOSED
  │                                       │
  │ (等待2MSL)                           │
CLOSED                                    │
```

**为什么是四次？**
- TCP是全双工，双方都需要关闭
- **第一次**：客户端说"我发完了"（FIN）
- **第二次**：服务器说"我知道了"（ACK）
- **第三次**：服务器说"我也发完了"（FIN）
- **第四次**：客户端说"我知道了"（ACK）

**TIME_WAIT状态**：
- 持续时间：2MSL（Maximum Segment Lifetime，通常60秒）
- 目的：
  1. 确保最后的ACK到达对方
  2. 让旧连接的数据包在网络中消失

**代码示例**：
```c
// 关闭连接
close(sockfd);  // 触发四次挥手

// 避免TIME_WAIT的socket复用
int reuse = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
```

### 2.4 可靠传输

**序列号和确认号**：
```
发送方: seq=100, 发送100字节
接收方: ack=200 (期望接收第200字节)

发送方: seq=200, 发送50字节
接收方: ack=250

序列号标识数据位置，确认号确认收到
```

**超时重传**：
```c
// 简化的重传机制
struct retransmit {
    uint32_t seq;
    uint8_t* data;
    int len;
    struct timeval send_time;
    int retries;
};

void check_timeout() {
    struct timeval now;
    gettimeofday(&now, NULL);
    
    for (packet in sent_queue) {
        if (now - packet.send_time > RTO) {
            // 超时，重传
            send_packet(packet);
            packet.retries++;
            packet.send_time = now;
        }
    }
}
```

**快速重传**：
```
接收方收到乱序包时，立即发送重复ACK

发送方收到3个重复ACK，立即重传
（不等超时）

seq=100 ───→ ✓ ack=200
seq=200 ───→ ✗ 丢失
seq=300 ───→ ✓ ack=200 (重复1)
seq=400 ───→ ✓ ack=200 (重复2)
seq=500 ───→ ✓ ack=200 (重复3)
seq=200 ───→ ✓ 快速重传！
```

### 2.5 流量控制（滑动窗口）

**原理**：接收方告诉发送方自己的缓冲区大小

```c
接收方:
recv_window = BUFFER_SIZE - (next_seq - acked_seq)
在TCP头部的window字段通知发送方

发送方:
send_window = min(recv_window, cwnd)  // cwnd是拥塞窗口
只能发送send_window大小的数据

示例:
接收方缓冲区: 4KB
已接收未处理: 2KB
→ 通告窗口: 2KB

发送方最多再发2KB数据
```

**零窗口探测**：
```c
// 接收方窗口为0
while (recv_window == 0) {
    // 发送方定期发送1字节探测包
    send_probe();
    sleep(probe_interval);
}
```

### 2.6 拥塞控制

**四个算法**：

**1. 慢启动（Slow Start）**
```
初始cwnd = 1 MSS
每收到一个ACK，cwnd += 1
指数增长: 1 → 2 → 4 → 8 → 16 ...

到达ssthresh（慢启动阈值）后，进入拥塞避免
```

**2. 拥塞避免（Congestion Avoidance）**
```
线性增长: cwnd += 1/cwnd (每RTT增加1)
16 → 17 → 18 → 19 ...

如果发生超时:
  ssthresh = cwnd / 2
  cwnd = 1
  重新慢启动
```

**3. 快速重传（Fast Retransmit）**
```
收到3个重复ACK:
  立即重传丢失的包
  进入快速恢复
```

**4. 快速恢复（Fast Recovery）**
```
收到3个重复ACK后:
  ssthresh = cwnd / 2
  cwnd = ssthresh + 3
  线性增长

收到新ACK:
  cwnd = ssthresh
  进入拥塞避免
```

**拥塞控制图示**：
```
cwnd
 │     慢启动    │  拥塞避免  │快速恢复│拥塞避免
 │    /          │  /         │/       │ /
 │   /           │ /          │        │/
 │  /            │/           │        │
 │ /             ↓ 3个重复ACK │        │
 │/              │            ↓        │
 └───────────────────────────────────→ 时间
```

---

## 3. UDP协议

### 3.1 UDP头部格式

```c
struct udp_header {
    uint16_t source_port;   // 源端口 (2字节)
    uint16_t dest_port;     // 目标端口 (2字节)
    uint16_t length;        // UDP长度 (2字节)
    uint16_t checksum;      // 校验和 (2字节)
    // 数据部分...
};
// 总共只有8字节！
```

### 3.2 UDP特点

**优点**：
- ✅ 无连接，无握手开销
- ✅ 低延迟（无重传等待）
- ✅ 头部简单（只有8字节）
- ✅ 支持广播和多播

**缺点**：
- ❌ 不可靠（可能丢包、乱序、重复）
- ❌ 无流量控制
- ❌ 无拥塞控制

### 3.3 UDP vs TCP

| 特性 | TCP | UDP |
|------|-----|-----|
| 连接 | 面向连接 | 无连接 |
| 可靠性 | 可靠 | 不可靠 |
| 顺序 | 有序 | 可能乱序 |
| 速度 | 慢（头部20-60字节） | 快（头部8字节） |
| 应用 | HTTP, FTP, SSH | DNS, 视频, 游戏 |

### 3.4 UDP应用场景

```
✅ DNS查询：单个数据包，丢包重查即可
✅ 视频直播：实时性优先，丢几帧无所谓
✅ 在线游戏：低延迟优先，丢包插值
✅ VoIP：实时语音，延迟>可靠性
✅ DHCP：简单请求-响应

❌ 文件传输：需要可靠性
❌ 网页浏览：需要完整数据
❌ 邮件：需要可靠性
```

### 3.5 UDP编程示例

```c
// UDP服务器
int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

struct sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);
server_addr.sin_addr.s_addr = INADDR_ANY;

bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));

char buffer[1024];
struct sockaddr_in client_addr;
socklen_t addr_len = sizeof(client_addr);

while (1) {
    int n = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                    (struct sockaddr*)&client_addr, &addr_len);
    
    printf("Received: %s\n", buffer);
    
    sendto(sockfd, buffer, n, 0,
           (struct sockaddr*)&client_addr, addr_len);
}

// UDP客户端
int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

struct sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

const char* message = "Hello UDP";
sendto(sockfd, message, strlen(message), 0,
       (struct sockaddr*)&server_addr, sizeof(server_addr));

char buffer[1024];
int n = recvfrom(sockfd, buffer, sizeof(buffer), 0, NULL, NULL);
printf("Response: %s\n", buffer);
```

---

## 4. IP协议

### 4.1 IP地址

**IPv4**：
```
32位，4个字节
点分十进制：192.168.1.1

网络部分 + 主机部分
A类：0.0.0.0 - 127.255.255.255
B类：128.0.0.0 - 191.255.255.255
C类：192.0.0.0 - 223.255.255.255

子网掩码：255.255.255.0 (/24)
网络地址：192.168.1.0
广播地址：192.168.1.255
可用主机：192.168.1.1 - 192.168.1.254
```

**IPv6**：
```
128位，16个字节
冒号十六进制：2001:0db8:85a3:0000:0000:8a2e:0370:7334

简化：
2001:db8:85a3::8a2e:370:7334
（连续的0可省略）
```

### 4.2 IP数据包格式

```c
struct ip_header {
    uint8_t  version : 4;       // 版本号 (4)
    uint8_t  ihl : 4;           // 头部长度
    uint8_t  tos;               // 服务类型
    uint16_t total_length;      // 总长度
    uint16_t identification;    // 标识
    uint16_t flags : 3;         // 标志
    uint16_t fragment_offset : 13; // 片偏移
    uint8_t  ttl;               // 生存时间
    uint8_t  protocol;          // 协议 (TCP=6, UDP=17)
    uint16_t checksum;          // 校验和
    uint32_t source_ip;         // 源IP
    uint32_t dest_ip;           // 目标IP
    // 可选项...
};
```

### 4.3 IP路由

**路由表**：
```bash
# 查看路由表
$ route -n
Destination     Gateway         Genmask         Flags Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     eth0

# 路由选择：最长前缀匹配
目标: 192.168.1.100
匹配: 192.168.1.0/24（更具体）→ 直接投递
不匹配: 0.0.0.0/0 → 默认网关
```

### 4.4 NAT（网络地址转换）

```
内网 → 外网
源IP: 192.168.1.100:5000
NAT转换: 203.0.113.5:60000
目标IP: 8.8.8.8:53

外网 → 内网
源IP: 8.8.8.8:53
目标IP: 203.0.113.5:60000
NAT转换: 192.168.1.100:5000

NAT表:
内部地址:端口         外部地址:端口
192.168.1.100:5000 ↔ 203.0.113.5:60000
192.168.1.101:6000 ↔ 203.0.113.5:60001
```

---

## 5. 常见问题

### Q1: 为什么TIME_WAIT要等2MSL？
**A**:
1. 确保最后的ACK到达（如果丢失，对方会重发FIN，需要能接收并回复）
2. 让旧连接的数据包在网络中消失

### Q2: 如何减少TIME_WAIT？
**A**:
- 调整`tcp_tw_reuse`和`tcp_tw_recycle`（需谨慎）
- 使用SO_REUSEADDR
- 客户端使用短连接，由客户端主动关闭

### Q3: TCP为什么需要Nagle算法？
**A**:
- 合并小包，减少网络拥塞
- 但增加延迟，交互式应用需禁用（TCP_NODELAY）

### Q4: 为什么UDP不可靠但还要用？
**A**:
- 低延迟优先级高于可靠性（实时应用）
- 可以在应用层实现可靠性（如QUIC）

---

## 6. 性能优化

### 6.1 TCP优化

```bash
# 增大缓冲区
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216

# TCP窗口缩放
sysctl -w net.ipv4.tcp_window_scaling=1

# 快速回收TIME_WAIT
sysctl -w net.ipv4.tcp_tw_reuse=1

# SYN队列大小
sysctl -w net.ipv4.tcp_max_syn_backlog=8192

# 连接队列大小
sysctl -w net.core.somaxconn=1024
```

### 6.2 应用层优化

```c
// TCP_NODELAY: 禁用Nagle算法
int flag = 1;
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));

// SO_KEEPALIVE: 保活机制
int keepalive = 1;
setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE, &keepalive, sizeof(keepalive));

// SO_RCVBUF: 接收缓冲区
int bufsize = 8192;
setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize));
```

---

## 参考资源

- 《TCP/IP详解 卷1：协议》
- RFC 793 (TCP)
- RFC 768 (UDP)
- Linux源码：`net/ipv4/tcp.c`
- Wireshark实战教程


# 网络工具大全

## 💡 核心结论

1. **ping检测连通性，traceroute追踪路由路径**
2. **netstat/ss查看网络连接状态，lsof查看端口占用**
3. **tcpdump/Wireshark抓包分析，是网络调试的利器**
4. **curl/wget测试HTTP，nmap扫描端口和服务**
5. **iperf测试带宽，mtr综合诊断网络问题**

---

## 1. 连通性测试工具

### 1.1 ping

**功能**：测试主机可达性和网络延迟

```bash
# 基本用法
$ ping www.baidu.com
PING www.a.shifen.com (14.215.177.38): 56 data bytes
64 bytes from 14.215.177.38: icmp_seq=0 ttl=54 time=8.123 ms
64 bytes from 14.215.177.38: icmp_seq=1 ttl=54 time=7.892 ms

# 发送指定数量的包
$ ping -c 4 8.8.8.8

# 设置包大小
$ ping -s 1024 8.8.8.8

# 设置时间间隔
$ ping -i 0.2 8.8.8.8

# flood ping（压力测试）
$ sudo ping -f 8.8.8.8

# 设置TTL
$ ping -t 10 8.8.8.8
```

**原理**：发送ICMP Echo Request，接收Echo Reply

**常见结果**：
```
time < 10ms   : 极好
time < 50ms   : 良好
time < 100ms  : 一般
time > 200ms  : 较差
Request timeout: 网络不通或防火墙阻止
```

### 1.2 traceroute/tracert

**功能**：追踪数据包到目标的路由路径

```bash
# Linux/Mac
$ traceroute www.baidu.com
traceroute to www.a.shifen.com (14.215.177.38), 30 hops max
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.123 ms  1.089 ms
 2  10.0.0.1 (10.0.0.1)  2.345 ms  2.234 ms  2.123 ms
 3  * * *
 4  14.215.177.38 (14.215.177.38)  8.123 ms  7.890 ms  7.765 ms

# Windows
$ tracert www.baidu.com

# 使用ICMP而不是UDP
$ traceroute -I www.baidu.com

# 指定最大跳数
$ traceroute -m 15 www.baidu.com

# 不解析主机名（更快）
$ traceroute -n 8.8.8.8
```

**原理**：
1. 发送TTL=1的包，第一跳路由器返回ICMP Time Exceeded
2. 发送TTL=2的包，第二跳路由器返回
3. 依次递增TTL，直到到达目标

### 1.3 mtr

**功能**：结合ping和traceroute，持续监控

```bash
# 交互式界面
$ mtr www.baidu.com

# 报告模式（发送10个包）
$ mtr -r -c 10 www.baidu.com

# CSV格式输出
$ mtr --csv www.baidu.com

# 只显示IP不解析域名
$ mtr -n 8.8.8.8
```

**输出解释**：
```
                          Loss%   Snt   Last   Avg  Best  Wrst StDev
1. 192.168.1.1             0.0%    10    1.2   1.3   1.1   1.5   0.1
2. 10.0.0.1                0.0%    10    2.3   2.4   2.2   2.6   0.1
3. ???                   100.0%    10    0.0   0.0   0.0   0.0   0.0
4. 14.215.177.38           0.0%    10    8.1   8.2   7.9   8.5   0.2

Loss%: 丢包率
Snt:   发送的包数
Avg:   平均延迟
Best:  最小延迟
Wrst:  最大延迟
StDev: 标准差（抖动）
```

---

## 2. 连接和端口查看工具

### 2.1 netstat

**功能**：显示网络连接、路由表、接口统计

```bash
# 显示所有TCP连接
$ netstat -t

# 显示所有UDP连接
$ netstat -u

# 显示监听端口
$ netstat -l

# 显示所有连接和监听端口
$ netstat -a

# 不解析主机名和端口名（更快）
$ netstat -n

# 显示进程信息
$ netstat -p

# 组合使用（最常用）
$ netstat -tulnp

# 显示路由表
$ netstat -r

# 显示网络接口统计
$ netstat -i
```

**输出示例**：
```
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      5678/mysqld
tcp        0    396 192.168.1.100:22        192.168.1.200:54321     ESTABLISHED 9012/sshd
```

### 2.2 ss

**功能**：netstat的现代替代品，更快

```bash
# 显示所有TCP连接
$ ss -t

# 显示监听端口
$ ss -l

# 组合使用
$ ss -tulnp

# 显示TCP连接的详细信息
$ ss -tin

# 按状态过滤
$ ss state established

# 按地址过滤
$ ss dst 8.8.8.8

# 按端口过滤
$ ss sport = :80
$ ss dport = :443

# 显示进程信息
$ ss -p

# 显示TCP内存使用
$ ss -tm
```

**输出示例**：
```
State    Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN   0      128    *:22                *:*
ESTAB    0      0      192.168.1.100:22    192.168.1.200:54321
```

### 2.3 lsof

**功能**：列出打开的文件（包括网络连接）

```bash
# 查看指定端口被哪个进程占用
$ lsof -i:8080
$ lsof -i:80-443  # 范围

# 查看指定进程的网络连接
$ lsof -p 1234

# 查看指定用户的网络连接
$ lsof -u username

# 查看所有TCP连接
$ lsof -i tcp

# 查看所有UDP连接
$ lsof -i udp

# 查看IPv4连接
$ lsof -i 4

# 组合使用
$ lsof -i tcp -s tcp:established
```

**输出示例**：
```
COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx    1234     root    6u  IPv4  12345      0t0  TCP *:80 (LISTEN)
chrome   5678     user   42u  IPv4  67890      0t0  TCP 192.168.1.100:54321->93.184.216.34:443 (ESTABLISHED)
```

---

## 3. 抓包和分析工具

### 3.1 tcpdump

**功能**：命令行抓包工具

```bash
# 抓取所有网卡的包
$ sudo tcpdump

# 抓取指定网卡
$ sudo tcpdump -i eth0

# 抓取指定主机的包
$ sudo tcpdump host 192.168.1.100

# 抓取指定端口的包
$ sudo tcpdump port 80

# 抓取TCP包
$ sudo tcpdump tcp

# 抓取UDP包
$ sudo tcpdump udp

# 组合过滤
$ sudo tcpdump 'tcp port 80 and host 192.168.1.100'

# 抓取指定数量的包
$ sudo tcpdump -c 100

# 保存到文件
$ sudo tcpdump -w capture.pcap

# 读取文件
$ tcpdump -r capture.pcap

# 显示ASCII内容
$ sudo tcpdump -A

# 显示十六进制内容
$ sudo tcpdump -X

# 不解析主机名
$ sudo tcpdump -n

# 不解析端口名
$ sudo tcpdump -nn

# 显示详细信息
$ sudo tcpdump -v
$ sudo tcpdump -vv
$ sudo tcpdump -vvv
```

**常用过滤表达式**：
```bash
# 源/目标IP
tcpdump src 192.168.1.100
tcpdump dst 8.8.8.8

# 网段
tcpdump net 192.168.1.0/24

# 端口范围
tcpdump portrange 8000-9000

# HTTP流量
tcpdump 'tcp port 80'

# HTTPS流量
tcpdump 'tcp port 443'

# SYN包
tcpdump 'tcp[tcpflags] & tcp-syn != 0'

# RST包
tcpdump 'tcp[tcpflags] & tcp-rst != 0'

# 抓取HTTP GET请求
tcpdump -s 0 -A 'tcp dst port 80 and tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'
```

### 3.2 Wireshark

**功能**：图形化抓包和分析工具

**过滤语法**：
```
# 按协议过滤
http
tcp
udp
dns
icmp

# 按IP过滤
ip.addr == 192.168.1.100
ip.src == 192.168.1.100
ip.dst == 8.8.8.8

# 按端口过滤
tcp.port == 80
tcp.srcport == 1234
tcp.dstport == 443

# 按HTTP过滤
http.request.method == "GET"
http.response.code == 200
http.host contains "google.com"

# 按TCP标志过滤
tcp.flags.syn == 1
tcp.flags.reset == 1

# 组合过滤
ip.addr == 192.168.1.100 && tcp.port == 80
(http || https) && ip.src == 192.168.1.100

# 按字符串过滤
tcp contains "password"
http.request.uri contains "login"
```

**常用功能**：
1. **Follow TCP Stream**：查看完整的TCP会话
2. **Statistics → Conversations**：查看连接统计
3. **Statistics → IO Graphs**：查看流量图表
4. **Expert Info**：查看问题和警告

---

## 4. HTTP测试工具

### 4.1 curl

**功能**：强大的HTTP客户端

```bash
# 基本GET请求
$ curl https://api.github.com

# 显示响应头
$ curl -i https://api.github.com

# 只显示响应头
$ curl -I https://api.github.com

# POST请求
$ curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","age":25}'

# PUT请求
$ curl -X PUT https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name":"李四"}'

# DELETE请求
$ curl -X DELETE https://api.example.com/users/123

# 发送表单数据
$ curl -X POST https://api.example.com/login \
  -d "username=admin&password=secret"

# 上传文件
$ curl -X POST https://api.example.com/upload \
  -F "file=@/path/to/file.txt"

# 自定义头部
$ curl -H "Authorization: Bearer token123" \
  -H "User-Agent: My-App/1.0" \
  https://api.example.com/profile

# 使用Cookie
$ curl -b "session=abc123" https://api.example.com
$ curl -c cookies.txt https://api.example.com  # 保存Cookie

# 跟随重定向
$ curl -L https://bit.ly/short-url

# 设置超时
$ curl --connect-timeout 10 --max-time 30 https://slow-server.com

# 显示详细信息
$ curl -v https://api.github.com

# 静默模式（不显示进度）
$ curl -s https://api.github.com

# 下载文件
$ curl -O https://example.com/file.zip
$ curl -o filename.zip https://example.com/file.zip

# 断点续传
$ curl -C - -O https://example.com/large-file.iso

# 限速
$ curl --limit-rate 100K https://example.com/file.zip

# 代理
$ curl -x http://proxy:8080 https://api.example.com

# 测试响应时间
$ curl -w "@curl-format.txt" -o /dev/null -s https://api.github.com

# curl-format.txt内容：
     time_namelookup:  %{time_namelookup}s\n
        time_connect:  %{time_connect}s\n
     time_appconnect:  %{time_appconnect}s\n
    time_pretransfer:  %{time_pretransfer}s\n
       time_redirect:  %{time_redirect}s\n
  time_starttransfer:  %{time_starttransfer}s\n
                     ----------\n
          time_total:  %{time_total}s\n
```

### 4.2 wget

**功能**：下载工具

```bash
# 下载文件
$ wget https://example.com/file.zip

# 后台下载
$ wget -b https://example.com/large-file.iso

# 断点续传
$ wget -c https://example.com/large-file.iso

# 限速
$ wget --limit-rate=100k https://example.com/file.zip

# 下载整个网站
$ wget -r -np -k https://example.com

# 设置User-Agent
$ wget --user-agent="Mozilla/5.0" https://example.com

# HTTP认证
$ wget --http-user=username --http-password=password https://example.com

# 使用代理
$ wget -e use_proxy=yes -e http_proxy=proxy:8080 https://example.com

# 重试次数
$ wget --tries=5 https://unstable-server.com
```

### 4.3 httpie

**功能**：现代化的HTTP客户端（比curl更友好）

```bash
# 安装
$ pip install httpie

# GET请求
$ http GET https://api.github.com

# POST请求（JSON）
$ http POST https://api.example.com/users name=张三 age:=25

# 自定义头部
$ http GET https://api.example.com \
  Authorization:"Bearer token123" \
  User-Agent:My-App/1.0

# 上传文件
$ http --form POST https://api.example.com/upload file@/path/to/file.txt

# 下载文件
$ http --download https://example.com/file.zip

# 显示详细信息
$ http -v GET https://api.github.com

# 只显示响应体
$ http -b GET https://api.github.com

# 只显示响应头
$ http -h GET https://api.github.com
```

---

## 5. 网络扫描工具

### 5.1 nmap

**功能**：网络扫描和安全审计

```bash
# 扫描主机是否在线
$ nmap 192.168.1.1

# 扫描网段
$ nmap 192.168.1.0/24

# 扫描指定端口
$ nmap -p 80,443 192.168.1.1

# 扫描端口范围
$ nmap -p 1-1000 192.168.1.1

# 扫描所有端口
$ nmap -p- 192.168.1.1

# 快速扫描
$ nmap -F 192.168.1.1

# TCP SYN扫描（隐蔽扫描）
$ sudo nmap -sS 192.168.1.1

# TCP连接扫描
$ nmap -sT 192.168.1.1

# UDP扫描
$ sudo nmap -sU 192.168.1.1

# 服务版本检测
$ nmap -sV 192.168.1.1

# 操作系统检测
$ sudo nmap -O 192.168.1.1

# 脚本扫描
$ nmap -sC 192.168.1.1

# 全面扫描
$ sudo nmap -A 192.168.1.1

# 输出到文件
$ nmap -oN scan.txt 192.168.1.1
$ nmap -oX scan.xml 192.168.1.1
```

### 5.2 nc (netcat)

**功能**：网络瑞士军刀

```bash
# 端口扫描
$ nc -zv 192.168.1.1 80
$ nc -zv 192.168.1.1 1-1000  # 扫描范围

# 创建TCP服务器
$ nc -l 8080

# 连接到服务器
$ nc 192.168.1.1 8080

# UDP模式
$ nc -u 192.168.1.1 53

# 文件传输
# 接收方：
$ nc -l 8080 > received_file.txt
# 发送方：
$ nc 192.168.1.100 8080 < file.txt

# 端口转发
$ nc -l 8080 | nc target_host 80

# 聊天
# 服务器：
$ nc -l 8080
# 客户端：
$ nc 192.168.1.100 8080

# Banner抓取
$ echo "" | nc 192.168.1.1 80

# 反向Shell（安全测试用）
# 监听方：
$ nc -l 4444
# 目标机：
$ nc 192.168.1.100 4444 -e /bin/bash
```

---

## 6. 性能测试工具

### 6.1 iperf

**功能**：网络带宽测试

```bash
# 服务器端
$ iperf -s

# 客户端（TCP测试）
$ iperf -c 192.168.1.100

# UDP测试
$ iperf -c 192.168.1.100 -u -b 100M

# 双向测试
$ iperf -c 192.168.1.100 -d

# 设置测试时间
$ iperf -c 192.168.1.100 -t 60

# 并行连接
$ iperf -c 192.168.1.100 -P 4

# 反向测试
$ iperf -c 192.168.1.100 -R
```

### 6.2 ab (Apache Bench)

**功能**：HTTP压力测试

```bash
# 基本测试（100个请求，10并发）
$ ab -n 100 -c 10 http://localhost/

# POST请求
$ ab -n 100 -c 10 -p data.json -T application/json http://localhost/api/users

# 自定义头部
$ ab -n 100 -c 10 -H "Authorization: Bearer token" http://localhost/

# Keep-Alive
$ ab -n 1000 -c 100 -k http://localhost/

# 输出详细信息
$ ab -v 4 -n 100 -c 10 http://localhost/
```

---

## 7. DNS工具

### 7.1 nslookup

```bash
# 查询域名
$ nslookup www.baidu.com

# 指定DNS服务器
$ nslookup www.baidu.com 8.8.8.8

# 查询特定记录类型
$ nslookup -type=MX gmail.com
$ nslookup -type=NS google.com
```

### 7.2 dig

```bash
# 查询域名
$ dig www.baidu.com

# 简洁输出
$ dig +short www.baidu.com

# 查询特定记录
$ dig MX gmail.com
$ dig NS google.com
$ dig TXT _dmarc.google.com

# 反向查询
$ dig -x 8.8.8.8

# 追踪DNS解析过程
$ dig +trace www.baidu.com

# 指定DNS服务器
$ dig @8.8.8.8 www.baidu.com
```

---

## 8. 综合诊断

```bash
# 快速诊断网络问题
1. ping 8.8.8.8           # 测试外网连通性
2. ping 192.168.1.1       # 测试网关
3. traceroute 8.8.8.8     # 追踪路由
4. nslookup www.baidu.com # 测试DNS
5. netstat -tulnp         # 查看端口占用
6. ss -s                  # 查看连接统计
```

---

## 参考资源

- man pages: tcpdump(8), netstat(8), ss(8)
- Wireshark用户手册
- nmap官方文档
- 《TCP/IP详解》


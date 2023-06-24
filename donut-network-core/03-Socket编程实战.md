# Socket编程实战

## 💡 核心结论

1. **Socket是应用层和传输层之间的接口**
2. **TCP Socket需要bind, listen, accept建立服务器**
3. **UDP Socket无需连接，使用sendto/recvfrom通信**
4. **select/poll/epoll实现I/O多路复用，提高并发性能**
5. **非阻塞I/O配合事件驱动模型可处理大量并发连接**

---

## 1. Socket基础

### 1.1 Socket概念

**Socket = IP地址 + 端口号 + 协议**

```
应用层
  ↓
Socket API ← 这里是Socket
  ↓
传输层(TCP/UDP)
```

### 1.2 Socket类型

```c
// 流式Socket (TCP)
int sockfd = socket(AF_INET, SOCK_STREAM, 0);

// 数据报Socket (UDP)
int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

// 原始Socket
int sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
```

### 1.3 地址结构

```c
// IPv4地址结构
struct sockaddr_in {
    sa_family_t sin_family;     // AF_INET
    in_port_t sin_port;         // 端口号（网络字节序）
    struct in_addr sin_addr;    // IP地址
    unsigned char sin_zero[8];  // 填充
};

// 通用地址结构
struct sockaddr {
    sa_family_t sa_family;
    char sa_data[14];
};

// 使用示例
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(8080);  // 主机字节序→网络字节序
inet_pton(AF_INET, "192.168.1.1", &addr.sin_addr);
```

---

## 2. TCP Socket编程

### 2.1 服务器端流程

```
socket() → bind() → listen() → accept() → recv/send() → close()
```

**完整示例**：
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080
#define BACKLOG 10

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[1024];
    
    // 1. 创建Socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        exit(1);
    }
    
    // 2. 设置地址复用
    int reuse = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
    
    // 3. 绑定地址
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;  // 监听所有接口
    server_addr.sin_port = htons(PORT);
    
    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        exit(1);
    }
    
    // 4. 监听
    if (listen(server_fd, BACKLOG) < 0) {
        perror("listen");
        exit(1);
    }
    
    printf("Server listening on port %d\n", PORT);
    
    // 5. 接受连接并处理
    while (1) {
        client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }
        
        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));
        printf("Client connected: %s:%d\n", client_ip, ntohs(client_addr.sin_port));
        
        // 接收数据
        int n = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (n > 0) {
            buffer[n] = '\0';
            printf("Received: %s\n", buffer);
            
            // 发送响应
            const char* response = "HTTP/1.1 200 OK\r\n\r\nHello World!";
            send(client_fd, response, strlen(response), 0);
        }
        
        close(client_fd);
    }
    
    close(server_fd);
    return 0;
}
```

### 2.2 客户端流程

```
socket() → connect() → send/recv() → close()
```

**完整示例**：
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[1024];
    
    // 1. 创建Socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(1);
    }
    
    // 2. 设置服务器地址
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);
    
    // 3. 连接服务器
    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        exit(1);
    }
    
    printf("Connected to server\n");
    
    // 4. 发送请求
    const char* request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n";
    send(sockfd, request, strlen(request), 0);
    
    // 5. 接收响应
    int n = recv(sockfd, buffer, sizeof(buffer) - 1, 0);
    if (n > 0) {
        buffer[n] = '\0';
        printf("Response:\n%s\n", buffer);
    }
    
    // 6. 关闭连接
    close(sockfd);
    return 0;
}
```

### 2.3 多客户端处理

**方案1：多进程**
```c
while (1) {
    client_fd = accept(server_fd, NULL, NULL);
    
    pid_t pid = fork();
    if (pid == 0) {
        // 子进程处理客户端
        close(server_fd);
        handle_client(client_fd);
        close(client_fd);
        exit(0);
    } else {
        // 父进程继续接受连接
        close(client_fd);
    }
}
```

**方案2：多线程**
```c
void* handle_client(void* arg) {
    int client_fd = *(int*)arg;
    free(arg);
    
    // 处理客户端请求
    char buffer[1024];
    int n = recv(client_fd, buffer, sizeof(buffer), 0);
    // ...
    
    close(client_fd);
    return NULL;
}

while (1) {
    client_fd = accept(server_fd, NULL, NULL);
    
    int *fd_ptr = malloc(sizeof(int));
    *fd_ptr = client_fd;
    
    pthread_t thread;
    pthread_create(&thread, NULL, handle_client, fd_ptr);
    pthread_detach(thread);
}
```

---

## 3. UDP Socket编程

### 3.1 服务器端

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[1024];
    
    // 1. 创建Socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    
    // 2. 绑定地址
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(8080);
    
    bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    
    printf("UDP Server listening on port 8080\n");
    
    // 3. 接收和发送数据
    while (1) {
        int n = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0,
                        (struct sockaddr*)&client_addr, &client_len);
        
        if (n > 0) {
            buffer[n] = '\0';
            printf("Received: %s\n", buffer);
            
            // 回送数据
            sendto(sockfd, buffer, n, 0,
                   (struct sockaddr*)&client_addr, client_len);
        }
    }
    
    close(sockfd);
    return 0;
}
```

### 3.2 客户端

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[1024];
    
    // 1. 创建Socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    
    // 2. 设置服务器地址
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);
    
    // 3. 发送数据
    const char* message = "Hello UDP";
    sendto(sockfd, message, strlen(message), 0,
           (struct sockaddr*)&server_addr, sizeof(server_addr));
    
    // 4. 接收响应
    int n = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0, NULL, NULL);
    if (n > 0) {
        buffer[n] = '\0';
        printf("Response: %s\n", buffer);
    }
    
    close(sockfd);
    return 0;
}
```

---

## 4. I/O多路复用

### 4.1 select

```c
#include <sys/select.h>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    // bind, listen...
    
    fd_set read_fds;
    int max_fd = server_fd;
    int client_fds[FD_SETSIZE];
    int num_clients = 0;
    
    while (1) {
        // 清空集合
        FD_ZERO(&read_fds);
        
        // 添加服务器socket
        FD_SET(server_fd, &read_fds);
        
        // 添加所有客户端socket
        for (int i = 0; i < num_clients; i++) {
            FD_SET(client_fds[i], &read_fds);
            if (client_fds[i] > max_fd) {
                max_fd = client_fds[i];
            }
        }
        
        // 等待事件
        struct timeval timeout = {5, 0};  // 5秒超时
        int ready = select(max_fd + 1, &read_fds, NULL, NULL, &timeout);
        
        if (ready < 0) {
            perror("select");
            break;
        }
        
        if (ready == 0) {
            // 超时
            continue;
        }
        
        // 检查服务器socket
        if (FD_ISSET(server_fd, &read_fds)) {
            int client_fd = accept(server_fd, NULL, NULL);
            client_fds[num_clients++] = client_fd;
            printf("New client connected\n");
        }
        
        // 检查客户端socket
        for (int i = 0; i < num_clients; i++) {
            if (FD_ISSET(client_fds[i], &read_fds)) {
                char buffer[1024];
                int n = recv(client_fds[i], buffer, sizeof(buffer), 0);
                
                if (n <= 0) {
                    // 客户端断开
                    close(client_fds[i]);
                    client_fds[i] = client_fds[--num_clients];
                    i--;
                } else {
                    // 处理数据
                    buffer[n] = '\0';
                    printf("Received: %s\n", buffer);
                    send(client_fds[i], buffer, n, 0);
                }
            }
        }
    }
    
    return 0;
}
```

**select缺点**：
- 有fd数量限制（FD_SETSIZE，通常1024）
- 每次调用需要复制fd_set
- 需要遍历所有fd查找就绪的

### 4.2 poll

```c
#include <poll.h>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    // bind, listen...
    
    struct pollfd fds[1000];
    int nfds = 1;
    
    // 添加服务器socket
    fds[0].fd = server_fd;
    fds[0].events = POLLIN;
    
    while (1) {
        int ready = poll(fds, nfds, 5000);  // 5秒超时
        
        if (ready < 0) {
            perror("poll");
            break;
        }
        
        if (ready == 0) {
            continue;
        }
        
        // 检查服务器socket
        if (fds[0].revents & POLLIN) {
            int client_fd = accept(server_fd, NULL, NULL);
            fds[nfds].fd = client_fd;
            fds[nfds].events = POLLIN;
            nfds++;
        }
        
        // 检查客户端socket
        for (int i = 1; i < nfds; i++) {
            if (fds[i].revents & POLLIN) {
                char buffer[1024];
                int n = recv(fds[i].fd, buffer, sizeof(buffer), 0);
                
                if (n <= 0) {
                    close(fds[i].fd);
                    fds[i] = fds[--nfds];
                    i--;
                } else {
                    send(fds[i].fd, buffer, n, 0);
                }
            }
        }
    }
    
    return 0;
}
```

### 4.3 epoll（Linux）

```c
#include <sys/epoll.h>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    // bind, listen...
    
    // 创建epoll实例
    int epollfd = epoll_create1(0);
    
    // 添加服务器socket
    struct epoll_event ev, events[MAX_EVENTS];
    ev.events = EPOLLIN;
    ev.data.fd = server_fd;
    epoll_ctl(epollfd, EPOLL_CTL_ADD, server_fd, &ev);
    
    while (1) {
        int nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1);
        
        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == server_fd) {
                // 新连接
                int client_fd = accept(server_fd, NULL, NULL);
                
                // 设置非阻塞
                int flags = fcntl(client_fd, F_GETFL, 0);
                fcntl(client_fd, F_SETFL, flags | O_NONBLOCK);
                
                // 添加到epoll
                ev.events = EPOLLIN | EPOLLET;  // 边缘触发
                ev.data.fd = client_fd;
                epoll_ctl(epollfd, EPOLL_CTL_ADD, client_fd, &ev);
            } else {
                // 客户端数据
                int fd = events[i].data.fd;
                char buffer[1024];
                int n = recv(fd, buffer, sizeof(buffer), 0);
                
                if (n <= 0) {
                    epoll_ctl(epollfd, EPOLL_CTL_DEL, fd, NULL);
                    close(fd);
                } else {
                    send(fd, buffer, n, 0);
                }
            }
        }
    }
    
    return 0;
}
```

**epoll优点**：
- 无fd数量限制
- 不需要遍历所有fd
- 支持边缘触发（ET）和水平触发（LT）

---

## 5. Python Socket编程

### 5.1 TCP服务器

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)

print("Server listening on port 8080")

while True:
    client, addr = server.accept()
    print(f"Client connected: {addr}")
    
    data = client.recv(1024)
    print(f"Received: {data.decode()}")
    
    response = b"HTTP/1.1 200 OK\r\n\r\nHello World!"
    client.send(response)
    client.close()
```

### 5.2 异步Socket（asyncio）

```python
import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Client connected: {addr}")
    
    data = await reader.read(1024)
    message = data.decode()
    print(f"Received: {message}")
    
    response = "Echo: " + message
    writer.write(response.encode())
    await writer.drain()
    
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client, '0.0.0.0', 8080)
    
    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr}")
    
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

---

## 6. 常见问题

### Q1: close和shutdown的区别？
**A**:
```c
// close: 关闭socket，引用计数-1
close(sockfd);

// shutdown: 关闭读/写，不减引用计数
shutdown(sockfd, SHUT_RD);    // 关闭读
shutdown(sockfd, SHUT_WR);    // 关闭写
shutdown(sockfd, SHUT_RDWR);  // 全关闭
```

### Q2: SO_REUSEADDR的作用？
**A**: 允许立即重用处于TIME_WAIT状态的端口

### Q3: 阻塞vs非阻塞？
**A**:
```c
// 阻塞：没有数据就等待
int n = recv(sockfd, buffer, size, 0);

// 非阻塞：没有数据立即返回-1，errno=EAGAIN
int flags = fcntl(sockfd, F_GETFL, 0);
fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);
```

### Q4: 粘包问题如何解决？
**A**:
1. 固定长度
2. 分隔符（如\r\n）
3. 长度前缀（TLV格式）

---

## 参考资源

- 《Unix网络编程》(UNP)
- Linux man pages: socket(7), tcp(7)
- Beej's Guide to Network Programming
- Python socket文档


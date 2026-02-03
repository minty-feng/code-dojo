# 09-网络编程基础

网络编程实现进程间跨主机通信。Socket是网络通信的基础API，TCP提供可靠连接，UDP提供快速无连接传输。

## Socket编程

Socket是网络通信端点的抽象。通过 socket()、bind()、listen()、accept()、connect() 等系统调用实现网络通信。

### 基本Socket操作

Socket编程遵循创建-绑定-监听-接受/连接的流程。RAII封装确保资源正确释放，避免文件描述符泄漏。


```cpp
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

class Socket {
private:
    int sockfd;
    
public:
    Socket(int domain, int type, int protocol) {
        sockfd = socket(domain, type, protocol);
        if (sockfd < 0) {
            throw std::runtime_error("Socket creation failed");
        }
    }
    
    ~Socket() {
        if (sockfd >= 0) {
            close(sockfd);
        }
    }
    
    int getFd() const { return sockfd; }
    
    void bind(const sockaddr* addr, socklen_t addrlen) {
        if (::bind(sockfd, addr, addrlen) < 0) {
            throw std::runtime_error("Bind failed");
        }
    }
    
    void listen(int backlog) {
        if (::listen(sockfd, backlog) < 0) {
            throw std::runtime_error("Listen failed");
        }
    }
    
    int accept(sockaddr* addr, socklen_t* addrlen) {
        int clientfd = ::accept(sockfd, addr, addrlen);
        if (clientfd < 0) {
            throw std::runtime_error("Accept failed");
        }
        return clientfd;
    }
    
    void connect(const sockaddr* addr, socklen_t addrlen) {
        if (::connect(sockfd, addr, addrlen) < 0) {
            throw std::runtime_error("Connect failed");
        }
    }
};
```

### TCP服务器

TCP服务器使用 `SOCK_STREAM` 创建面向连接的Socket。`listen()` 设置连接队列，`accept()` 阻塞等待客户端连接。

```cpp
#include <iostream>
#include <string>
#include <cstring>

class TCPServer {
private:
    Socket socket;
    int port;
    
public:
    TCPServer(int p) : socket(AF_INET, SOCK_STREAM, 0), port(p) {
        setupServer();
    }
    
    void setupServer() {
        // 设置地址重用
        int opt = 1;
        setsockopt(socket.getFd(), SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
        
        // 绑定地址
        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        
        socket.bind(reinterpret_cast<sockaddr*>(&addr), sizeof(addr));
        socket.listen(5);
        
        std::cout << "Server listening on port " << port << std::endl;
    }
    
    void run() {
        while (true) {
            sockaddr_in clientAddr{};
            socklen_t clientLen = sizeof(clientAddr);
            
            int clientfd = socket.accept(
                reinterpret_cast<sockaddr*>(&clientAddr), 
                &clientLen
            );
            
            std::cout << "Client connected: " 
                      << inet_ntoa(clientAddr.sin_addr) << std::endl;
            
            handleClient(clientfd);
            close(clientfd);
        }
    }
    
private:
    void handleClient(int clientfd) {
        char buffer[1024];
        while (true) {
            ssize_t bytesRead = recv(clientfd, buffer, sizeof(buffer) - 1, 0);
            if (bytesRead <= 0) {
                break;
            }
            
            buffer[bytesRead] = '\0';
            std::cout << "Received: " << buffer << std::endl;
            
            // 回显消息
            std::string response = "Echo: " + std::string(buffer);
            send(clientfd, response.c_str(), response.length(), 0);
        }
    }
};
```

### TCP客户端

TCP客户端主动发起连接。`connect()` 连接到服务器，`send()`/`recv()` 发送/接收数据。网络字节序用 `htons()` 转换。

```cpp
class TCPClient {
private:
    Socket socket;
    std::string host;
    int port;
    
public:
    TCPClient(const std::string& h, int p) 
        : socket(AF_INET, SOCK_STREAM, 0), host(h), port(p) {
        connectToServer();
    }
    
    void connectToServer() {
        sockaddr_in serverAddr{};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(port);
        
        if (inet_pton(AF_INET, host.c_str(), &serverAddr.sin_addr) <= 0) {
            throw std::runtime_error("Invalid address");
        }
        
        socket.connect(
            reinterpret_cast<sockaddr*>(&serverAddr), 
            sizeof(serverAddr)
        );
        
        std::cout << "Connected to " << host << ":" << port << std::endl;
    }
    
    void sendMessage(const std::string& message) {
        send(socket.getFd(), message.c_str(), message.length(), 0);
    }
    
    std::string receiveMessage() {
        char buffer[1024];
        ssize_t bytesRead = recv(socket.getFd(), buffer, sizeof(buffer) - 1, 0);
        if (bytesRead > 0) {
            buffer[bytesRead] = '\0';
            return std::string(buffer);
        }
        return "";
    }
};
```

## UDP编程

### UDP服务器
```cpp
class UDPServer {
private:
    Socket socket;
    int port;
    
public:
    UDPServer(int p) : socket(AF_INET, SOCK_DGRAM, 0), port(p) {
        setupServer();
    }
    
    void setupServer() {
        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        
        socket.bind(reinterpret_cast<sockaddr*>(&addr), sizeof(addr));
        std::cout << "UDP Server listening on port " << port << std::endl;
    }
    
    void run() {
        char buffer[1024];
        sockaddr_in clientAddr{};
        socklen_t clientLen = sizeof(clientAddr);
        
        while (true) {
            ssize_t bytesRead = recvfrom(
                socket.getFd(), buffer, sizeof(buffer) - 1, 0,
                reinterpret_cast<sockaddr*>(&clientAddr), &clientLen
            );
            
            if (bytesRead > 0) {
                buffer[bytesRead] = '\0';
                std::cout << "Received from " 
                          << inet_ntoa(clientAddr.sin_addr) 
                          << ": " << buffer << std::endl;
                
                // 回显消息
                std::string response = "Echo: " + std::string(buffer);
                sendto(
                    socket.getFd(), response.c_str(), response.length(), 0,
                    reinterpret_cast<sockaddr*>(&clientAddr), clientLen
                );
            }
        }
    }
};
```

### UDP客户端
```cpp
class UDPClient {
private:
    Socket socket;
    std::string host;
    int port;
    sockaddr_in serverAddr;
    
public:
    UDPClient(const std::string& h, int p) 
        : socket(AF_INET, SOCK_DGRAM, 0), host(h), port(p) {
        setupServerAddr();
    }
    
    void setupServerAddr() {
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(port);
        
        if (inet_pton(AF_INET, host.c_str(), &serverAddr.sin_addr) <= 0) {
            throw std::runtime_error("Invalid address");
        }
    }
    
    void sendMessage(const std::string& message) {
        sendto(
            socket.getFd(), message.c_str(), message.length(), 0,
            reinterpret_cast<sockaddr*>(&serverAddr), sizeof(serverAddr)
        );
    }
    
    std::string receiveMessage() {
        char buffer[1024];
        sockaddr_in fromAddr{};
        socklen_t fromLen = sizeof(fromAddr);
        
        ssize_t bytesRead = recvfrom(
            socket.getFd(), buffer, sizeof(buffer) - 1, 0,
            reinterpret_cast<sockaddr*>(&fromAddr), &fromLen
        );
        
        if (bytesRead > 0) {
            buffer[bytesRead] = '\0';
            return std::string(buffer);
        }
        return "";
    }
};
```

## 非阻塞IO

### 非阻塞Socket
```cpp
#include <fcntl.h>
#include <sys/select.h>

class NonBlockingSocket {
private:
    int sockfd;
    
public:
    NonBlockingSocket(int domain, int type, int protocol) {
        sockfd = socket(domain, type, protocol);
        if (sockfd < 0) {
            throw std::runtime_error("Socket creation failed");
        }
        
        // 设置为非阻塞
        int flags = fcntl(sockfd, F_GETFL, 0);
        fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);
    }
    
    ~NonBlockingSocket() {
        if (sockfd >= 0) {
            close(sockfd);
        }
    }
    
    int getFd() const { return sockfd; }
    
    bool connect(const sockaddr* addr, socklen_t addrlen) {
        int result = ::connect(sockfd, addr, addrlen);
        if (result == 0) {
            return true;  // 立即连接成功
        }
        
        if (errno == EINPROGRESS) {
            return false;  // 连接进行中
        }
        
        throw std::runtime_error("Connect failed");
    }
    
    bool isConnected() {
        int error = 0;
        socklen_t len = sizeof(error);
        int result = getsockopt(sockfd, SOL_SOCKET, SO_ERROR, &error, &len);
        
        if (result == 0 && error == 0) {
            return true;
        }
        return false;
    }
};
```

### select模型
```cpp
#include <sys/select.h>

class SelectServer {
private:
    int serverFd;
    fd_set readfds;
    int maxFd;
    std::vector<int> clientFds;
    
public:
    SelectServer(int port) {
        setupServer(port);
        FD_ZERO(&readfds);
        FD_SET(serverFd, &readfds);
        maxFd = serverFd;
    }
    
    void run() {
        while (true) {
            fd_set tempfds = readfds;
            
            int activity = select(maxFd + 1, &tempfds, nullptr, nullptr, nullptr);
            
            if (activity < 0) {
                throw std::runtime_error("Select failed");
            }
            
            // 检查新连接
            if (FD_ISSET(serverFd, &tempfds)) {
                acceptNewConnection();
            }
            
            // 检查客户端数据
            for (auto it = clientFds.begin(); it != clientFds.end();) {
                if (FD_ISSET(*it, &tempfds)) {
                    if (handleClientData(*it)) {
                        ++it;
                    } else {
                        close(*it);
                        FD_CLR(*it, &readfds);
                        it = clientFds.erase(it);
                    }
                } else {
                    ++it;
                }
            }
        }
    }
    
private:
    void setupServer(int port) {
        serverFd = socket(AF_INET, SOCK_STREAM, 0);
        
        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        
        bind(serverFd, reinterpret_cast<sockaddr*>(&addr), sizeof(addr));
        listen(serverFd, 5);
    }
    
    void acceptNewConnection() {
        sockaddr_in clientAddr{};
        socklen_t clientLen = sizeof(clientAddr);
        
        int clientFd = accept(serverFd, 
                             reinterpret_cast<sockaddr*>(&clientAddr), 
                             &clientLen);
        
        if (clientFd >= 0) {
            clientFds.push_back(clientFd);
            FD_SET(clientFd, &readfds);
            maxFd = std::max(maxFd, clientFd);
            
            std::cout << "New client connected" << std::endl;
        }
    }
    
    bool handleClientData(int clientFd) {
        char buffer[1024];
        ssize_t bytesRead = recv(clientFd, buffer, sizeof(buffer) - 1, 0);
        
        if (bytesRead > 0) {
            buffer[bytesRead] = '\0';
            std::cout << "Received: " << buffer << std::endl;
            
            std::string response = "Echo: " + std::string(buffer);
            send(clientFd, response.c_str(), response.length(), 0);
            return true;
        }
        
        return false;  // 客户端断开连接
    }
};
```

## HTTP客户端

### 简单HTTP客户端
```cpp
#include <sstream>
#include <regex>

class HTTPClient {
private:
    std::string host;
    int port;
    
public:
    HTTPClient(const std::string& h, int p = 80) : host(h), port(p) {}
    
    std::string get(const std::string& path) {
        TCPClient client(host, port);
        
        // 构建HTTP请求
        std::stringstream request;
        request << "GET " << path << " HTTP/1.1\r\n";
        request << "Host: " << host << "\r\n";
        request << "Connection: close\r\n";
        request << "\r\n";
        
        client.sendMessage(request.str());
        
        // 接收响应
        std::string response = client.receiveMessage();
        return parseResponse(response);
    }
    
    std::string post(const std::string& path, const std::string& data) {
        TCPClient client(host, port);
        
        // 构建HTTP请求
        std::stringstream request;
        request << "POST " << path << " HTTP/1.1\r\n";
        request << "Host: " << host << "\r\n";
        request << "Content-Type: application/json\r\n";
        request << "Content-Length: " << data.length() << "\r\n";
        request << "Connection: close\r\n";
        request << "\r\n";
        request << data;
        
        client.sendMessage(request.str());
        
        // 接收响应
        std::string response = client.receiveMessage();
        return parseResponse(response);
    }
    
private:
    std::string parseResponse(const std::string& response) {
        // 简单的响应解析
        std::regex headerRegex(R"(HTTP/\d\.\d (\d+) (.+))");
        std::smatch match;
        
        if (std::regex_search(response, match, headerRegex)) {
            int statusCode = std::stoi(match[1]);
            std::string statusText = match[2];
            
            std::cout << "Status: " << statusCode << " " << statusText << std::endl;
        }
        
        // 查找响应体
        size_t bodyStart = response.find("\r\n\r\n");
        if (bodyStart != std::string::npos) {
            return response.substr(bodyStart + 4);
        }
        
        return response;
    }
};
```

## 网络工具类

### 地址转换
```cpp
#include <arpa/inet.h>

class NetworkUtils {
public:
    static std::string ipToString(uint32_t ip) {
        struct in_addr addr;
        addr.s_addr = ip;
        return std::string(inet_ntoa(addr));
    }
    
    static uint32_t stringToIp(const std::string& ipStr) {
        return inet_addr(ipStr.c_str());
    }
    
    static uint16_t hostToNetwork(uint16_t host) {
        return htons(host);
    }
    
    static uint16_t networkToHost(uint16_t network) {
        return ntohs(network);
    }
    
    static uint32_t hostToNetwork(uint32_t host) {
        return htonl(host);
    }
    
    static uint32_t networkToHost(uint32_t network) {
        return ntohl(network);
    }
};
```

### 超时处理
```cpp
#include <sys/time.h>

class TimeoutSocket {
private:
    int sockfd;
    
public:
    TimeoutSocket(int domain, int type, int protocol) {
        sockfd = socket(domain, type, protocol);
    }
    
    void setReceiveTimeout(int seconds) {
        struct timeval timeout;
        timeout.tv_sec = seconds;
        timeout.tv_usec = 0;
        
        setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, 
                  &timeout, sizeof(timeout));
    }
    
    void setSendTimeout(int seconds) {
        struct timeval timeout;
        timeout.tv_sec = seconds;
        timeout.tv_usec = 0;
        
        setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, 
                  &timeout, sizeof(timeout));
    }
    
    ssize_t recvWithTimeout(void* buffer, size_t length, int flags) {
        return recv(sockfd, buffer, length, flags);
    }
    
    ssize_t sendWithTimeout(const void* buffer, size_t length, int flags) {
        return send(sockfd, buffer, length, flags);
    }
};
```

## IO多路复用

### select vs epoll 对比

| 特性 | select | epoll |
|------|--------|-------|
| 最大连接数 | 1024（FD_SETSIZE） | 无限制 |
| 时间复杂度 | O(n) | O(1) |
| 适用场景 | 少量连接 | 大量连接 |
| 跨平台 | 是 | Linux专有 |
| 性能 | 连接数少时可接受 | 高性能服务器 |

### select 示例

```cpp
#include <sys/select.h>
#include <vector>

class SelectServer {
private:
    int serverFd;
    std::vector<int> clients;
    
public:
    void run() {
        fd_set readfds;
        int maxFd = serverFd;
        
        while (true) {
            FD_ZERO(&readfds);
            FD_SET(serverFd, &readfds);  // 监听服务器socket
            
            // 监听所有客户端
            for (int clientFd : clients) {
                FD_SET(clientFd, &readfds);
                maxFd = std::max(maxFd, clientFd);
            }
            
            // 等待事件（阻塞）
            int ret = select(maxFd + 1, &readfds, nullptr, nullptr, nullptr);
            if (ret < 0) {
                perror("select");
                break;
            }
            
            // 检查服务器socket（新连接）
            if (FD_ISSET(serverFd, &readfds)) {
                int clientFd = accept(serverFd, nullptr, nullptr);
                clients.push_back(clientFd);
            }
            
            // 检查客户端socket（数据到达）
            for (auto it = clients.begin(); it != clients.end();) {
                if (FD_ISSET(*it, &readfds)) {
                    char buffer[1024];
                    ssize_t n = recv(*it, buffer, sizeof(buffer), 0);
                    if (n <= 0) {
                        close(*it);
                        it = clients.erase(it);
                        continue;
                    }
                    // 处理数据
                }
                ++it;
            }
        }
    }
};
```

### epoll 示例（Linux高性能）

```cpp
#include <sys/epoll.h>

class EpollServer {
private:
    int serverFd;
    int epollFd;
    
public:
    EpollServer(int port) {
        // 创建server socket
        serverFd = socket(AF_INET, SOCK_STREAM, 0);
        // bind, listen...
        
        // 创建epoll
        epollFd = epoll_create1(0);
        
        // 添加服务器socket到epoll
        epoll_event ev;
        ev.events = EPOLLIN;  // 监听可读事件
        ev.data.fd = serverFd;
        epoll_ctl(epollFd, EPOLL_CTL_ADD, serverFd, &ev);
    }
    
    void run() {
        const int MAX_EVENTS = 10;
        epoll_event events[MAX_EVENTS];
        
        while (true) {
            // 等待事件
            int nfds = epoll_wait(epollFd, events, MAX_EVENTS, -1);
            
            for (int i = 0; i < nfds; ++i) {
                if (events[i].data.fd == serverFd) {
                    // 新连接
                    int clientFd = accept(serverFd, nullptr, nullptr);
                    
                    // 添加客户端到epoll
                    epoll_event ev;
                    ev.events = EPOLLIN | EPOLLET;  // 边缘触发
                    ev.data.fd = clientFd;
                    epoll_ctl(epollFd, EPOLL_CTL_ADD, clientFd, &ev);
                } else {
                    // 客户端数据
                    int clientFd = events[i].data.fd;
                    char buffer[1024];
                    ssize_t n = recv(clientFd, buffer, sizeof(buffer), 0);
                    
                    if (n <= 0) {
                        // 连接关闭或错误
                        epoll_ctl(epollFd, EPOLL_CTL_DEL, clientFd, nullptr);
                        close(clientFd);
                    } else {
                        // 处理数据
                        send(clientFd, buffer, n, 0);
                    }
                }
            }
        }
    }
    
    ~EpollServer() {
        close(epollFd);
        close(serverFd);
    }
};
```

### epoll 触发模式

**水平触发（Level Triggered，默认）：**
- 只要fd可读/可写，epoll_wait就返回
- 适合：简单场景，不易遗漏事件
- 缺点：可能重复触发

**边缘触发（Edge Triggered）：**
- 只在状态变化时触发一次
- 必须一次性读完所有数据
- 适合：高性能服务器
- 需配合非阻塞IO

```cpp
// 边缘触发 + 非阻塞IO示例
void handleEdgeTriggered(int fd) {
    while (true) {
        char buffer[1024];
        ssize_t n = recv(fd, buffer, sizeof(buffer), MSG_DONTWAIT);
        
        if (n > 0) {
            // 处理数据
        } else if (n == 0) {
            // 连接关闭
            break;
        } else {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // 数据读完了
                break;
            } else {
                // 真正的错误
                perror("recv");
                break;
            }
        }
    }
}
```

**选择建议：**
- 少量连接（<100）：select（跨平台）
- 大量连接：epoll（Linux）/ kqueue（BSD）/ IOCP（Windows）
- 高性能要求：边缘触发 + 非阻塞IO
- 简单应用：水平触发

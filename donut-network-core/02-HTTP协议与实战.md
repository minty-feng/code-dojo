# HTTP协议与实战

## 💡 核心结论

1. **HTTP是无状态协议，通过Cookie/Session实现状态管理**
2. **HTTP/1.1支持持久连接，减少TCP握手开销**
3. **HTTPS = HTTP + TLS，通过非对称加密交换对称密钥**
4. **HTTP/2多路复用解决队头阻塞，HTTP/3基于QUIC进一步优化**
5. **RESTful API设计应遵循资源导向和统一接口原则**

---

## 1. HTTP基础

### 1.1 HTTP请求格式

```http
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
Accept-Language: zh-CN,zh;q=0.9
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: session_id=abc123

```

**请求行**：
```
方法 路径 版本
GET /api/users HTTP/1.1
```

**请求头**：
- `Host`: 目标主机（HTTP/1.1必需）
- `User-Agent`: 客户端信息
- `Accept`: 可接受的内容类型
- `Cookie`: 状态信息

**请求体**（POST/PUT）：
```http
POST /api/users HTTP/1.1
Content-Type: application/json
Content-Length: 45

{"name":"张三","age":25,"email":"test@qq.com"}
```

### 1.2 HTTP响应格式

```http
HTTP/1.1 200 OK
Date: Mon, 23 Oct 2023 12:00:00 GMT
Server: nginx/1.18.0
Content-Type: text/html; charset=UTF-8
Content-Length: 1234
Connection: keep-alive
Set-Cookie: session_id=xyz789; HttpOnly
Cache-Control: max-age=3600

<!DOCTYPE html>
<html>
...
</html>
```

**状态行**：
```
版本 状态码 原因短语
HTTP/1.1 200 OK
```

**响应头**：
- `Server`: 服务器信息
- `Content-Type`: 内容类型
- `Content-Length`: 内容长度
- `Set-Cookie`: 设置Cookie

---

## 2. HTTP方法

### 2.1 常用方法

| 方法 | 说明 | 幂等性 | 安全性 |
|------|------|--------|--------|
| GET | 获取资源 | ✅ | ✅ |
| POST | 创建资源 | ❌ | ❌ |
| PUT | 更新资源（完整） | ✅ | ❌ |
| PATCH | 更新资源（部分） | ❌ | ❌ |
| DELETE | 删除资源 | ✅ | ❌ |
| HEAD | 获取头部 | ✅ | ✅ |
| OPTIONS | 获取支持的方法 | ✅ | ✅ |

**幂等性**：多次执行结果相同
**安全性**：不修改服务器状态

### 2.2 GET vs POST

| 特性 | GET | POST |
|------|-----|------|
| 参数位置 | URL query string | 请求体 |
| 参数长度 | 有限制（~2KB） | 无限制 |
| 缓存 | 可缓存 | 不可缓存 |
| 历史记录 | 保留在浏览器历史 | 不保留 |
| 书签 | 可收藏 | 不可收藏 |
| 安全性 | 参数暴露在URL | 相对安全 |
| 用途 | 获取数据 | 提交数据 |

### 2.3 RESTful API设计

```http
# 获取所有用户
GET /api/users

# 获取单个用户
GET /api/users/123

# 创建用户
POST /api/users
Body: {"name":"张三","age":25}

# 更新用户（完整）
PUT /api/users/123
Body: {"name":"李四","age":26,"email":"li@qq.com"}

# 更新用户（部分）
PATCH /api/users/123
Body: {"age":27}

# 删除用户
DELETE /api/users/123

# 获取用户的订单
GET /api/users/123/orders

# 分页和过滤
GET /api/users?page=2&size=20&role=admin
```

---

## 3. HTTP状态码

### 3.1 状态码分类

**1xx 信息**：
- `100 Continue`: 继续请求
- `101 Switching Protocols`: 切换协议（WebSocket）

**2xx 成功**：
- `200 OK`: 成功
- `201 Created`: 已创建
- `204 No Content`: 无内容

**3xx 重定向**：
- `301 Moved Permanently`: 永久重定向
- `302 Found`: 临时重定向
- `304 Not Modified`: 未修改（缓存）

**4xx 客户端错误**：
- `400 Bad Request`: 请求错误
- `401 Unauthorized`: 未认证
- `403 Forbidden`: 禁止访问
- `404 Not Found`: 未找到
- `429 Too Many Requests`: 请求过多

**5xx 服务器错误**：
- `500 Internal Server Error`: 服务器错误
- `502 Bad Gateway`: 网关错误
- `503 Service Unavailable`: 服务不可用
- `504 Gateway Timeout`: 网关超时

### 3.2 常见场景

```python
# 成功创建资源
HTTP/1.1 201 Created
Location: /api/users/123

# 无权限访问
HTTP/1.1 403 Forbidden
{"error":"Permission denied"}

# 资源不存在
HTTP/1.1 404 Not Found
{"error":"User not found"}

# 参数验证失败
HTTP/1.1 400 Bad Request
{"error":"Invalid email format"}

# 服务器内部错误
HTTP/1.1 500 Internal Server Error
{"error":"Database connection failed"}
```

---

## 4. HTTP头部详解

### 4.1 请求头

```http
# 缓存控制
Cache-Control: no-cache, no-store, must-revalidate
If-None-Match: "abc123"  # ETag
If-Modified-Since: Mon, 23 Oct 2023 12:00:00 GMT

# 内容协商
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,en;q=0.9
Accept-Encoding: gzip, deflate, br

# 认证
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# 跨域
Origin: https://example.com
Referer: https://example.com/page

# 连接控制
Connection: keep-alive
Keep-Alive: timeout=5, max=1000

# 代理
X-Forwarded-For: 192.168.1.100
X-Real-IP: 203.0.113.5
```

### 4.2 响应头

```http
# 缓存控制
Cache-Control: public, max-age=31536000
ETag: "abc123"
Last-Modified: Mon, 23 Oct 2023 12:00:00 GMT
Expires: Tue, 24 Oct 2023 12:00:00 GMT

# 安全
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'

# CORS
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400

# 内容
Content-Type: application/json; charset=utf-8
Content-Length: 1234
Content-Encoding: gzip
Transfer-Encoding: chunked
```

---

## 5. Cookie和Session

### 5.1 Cookie

**设置Cookie**：
```http
HTTP/1.1 200 OK
Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=3600
Set-Cookie: user_pref=dark_mode; Path=/; Max-Age=2592000
```

**Cookie属性**：
- `Path`: Cookie的作用路径
- `Domain`: Cookie的作用域
- `Max-Age`: 有效期（秒）
- `Expires`: 过期时间
- `HttpOnly`: 禁止JavaScript访问（防XSS）
- `Secure`: 只通过HTTPS传输
- `SameSite`: 防止CSRF攻击
  - `Strict`: 完全禁止跨站
  - `Lax`: GET跨站允许
  - `None`: 允许跨站（需Secure）

**发送Cookie**：
```http
GET /api/profile HTTP/1.1
Host: api.example.com
Cookie: session_id=abc123; user_pref=dark_mode
```

### 5.2 Session

**工作流程**：
```
1. 用户登录 → 服务器创建Session
2. 服务器返回Session ID（通过Cookie）
3. 后续请求携带Session ID
4. 服务器通过Session ID识别用户

客户端: Cookie: session_id=abc123
服务器: sessions[abc123] = {user_id: 123, login_time: ...}
```

**Session实现**（Python Flask）：
```python
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    # 验证用户
    if verify_user(username, password):
        session['user_id'] = get_user_id(username)
        session['username'] = username
        return {'message': 'Login successful'}
    
    return {'error': 'Invalid credentials'}, 401

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401
    
    user_id = session['user_id']
    return {'user_id': user_id, 'username': session['username']}

@app.route('/logout')
def logout():
    session.clear()
    return {'message': 'Logged out'}
```

---

## 6. HTTPS

### 6.1 HTTPS握手过程

```
1. ClientHello
   客户端 → 服务器
   - 支持的TLS版本
   - 支持的加密套件
   - 随机数（Client Random）

2. ServerHello
   服务器 → 客户端
   - 选择的TLS版本
   - 选择的加密套件
   - 随机数（Server Random）
   - 服务器证书（含公钥）

3. 客户端验证证书
   - 检查证书有效期
   - 检查证书链
   - 检查域名是否匹配

4. 客户端生成Pre-Master Secret
   - 用服务器公钥加密
   - 发送给服务器

5. 双方生成会话密钥
   - Master Secret = f(Client Random, Server Random, Pre-Master Secret)
   - 用于后续对称加密

6. 握手完成
   - 双方发送Finished消息
   - 开始加密通信
```

### 6.2 对称加密 vs 非对称加密

| 特性 | 对称加密 | 非对称加密 |
|------|----------|------------|
| 密钥 | 同一个 | 公钥+私钥 |
| 速度 | 快 | 慢 |
| 安全性 | 密钥交换困难 | 安全 |
| 算法 | AES, DES | RSA, ECC |
| 用途 | 数据加密 | 密钥交换、签名 |

**HTTPS结合方案**：
```
非对称加密（慢）→ 交换对称密钥
对称加密（快）→ 加密实际数据
```

### 6.3 证书验证

```bash
# 查看证书信息
openssl s_client -connect www.baidu.com:443 -showcerts

# 证书链
Root CA (根证书)
  ↓
Intermediate CA (中间证书)
  ↓
Server Certificate (服务器证书)

# 验证证书
openssl verify -CAfile ca.crt server.crt
```

---

## 7. HTTP版本演进

### 7.1 HTTP/1.0

```
每个请求一个TCP连接
请求 → 响应 → 关闭连接 → 新请求 → 新连接
```

### 7.2 HTTP/1.1

```
持久连接（Keep-Alive）
一个TCP连接上多个请求
请求1 → 响应1 → 请求2 → 响应2 ...

问题：队头阻塞
请求1（慢） → 请求2（快，但必须等待）
```

### 7.3 HTTP/2

**特性**：
1. **多路复用**：一个连接上并行传输多个请求
2. **头部压缩**：HPACK算法压缩头部
3. **服务器推送**：主动推送资源
4. **二进制帧**：不再是文本协议

```
HTTP/1.1:
请求1 ━━━━━━━━━━━━━━━━━━━━ 响应1
请求2 ━━━━━━━━━━━━━━━━━━━━ 响应2

HTTP/2:
请求1 ━━━━━━━━ 响应1
请求2  ━━━━ 响应2
请求3   ━━━━━━ 响应3
（交错传输）
```

### 7.4 HTTP/3

**基于QUIC（UDP）**：
- 0-RTT连接建立
- 改进的拥塞控制
- 连接迁移（IP变化不断连接）
- 无队头阻塞

---

## 8. 实战示例

### 8.1 Python HTTP客户端

```python
import requests

# GET请求
response = requests.get('https://api.github.com/users/octocat')
print(response.status_code)  # 200
print(response.json())

# POST请求
data = {'name': '张三', 'age': 25}
response = requests.post('https://api.example.com/users', json=data)

# 自定义头部
headers = {
    'Authorization': 'Bearer token123',
    'User-Agent': 'My App/1.0'
}
response = requests.get('https://api.example.com/profile', headers=headers)

# 超时和重试
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

response = session.get('https://api.example.com/data', timeout=5)
```

### 8.2 Python HTTP服务器

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
next_id = 1

# GET /api/users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

# GET /api/users/<id>
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(users[user_id])

# POST /api/users
@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    user = {'id': next_id, 'name': data['name'], 'age': data.get('age', 0)}
    users[next_id] = user
    next_id += 1
    
    return jsonify(user), 201

# PUT /api/users/<id>
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    users[user_id].update(data)
    return jsonify(users[user_id])

# DELETE /api/users/<id>
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    del users[user_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 8.3 Node.js HTTP服务器

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    // 解析URL
    const url = new URL(req.url, `http://${req.headers.host}`);
    
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    
    // 路由
    if (url.pathname === '/api/users' && req.method === 'GET') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify([{id: 1, name: '张三'}]));
    } 
    else if (url.pathname === '/api/users' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            const user = JSON.parse(body);
            res.writeHead(201, {'Content-Type': 'application/json'});
            res.end(JSON.stringify({id: 2, ...user}));
        });
    }
    else {
        res.writeHead(404, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({error: 'Not found'}));
    }
});

server.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
```

---

## 9. 常见问题

### Q1: 为什么要用HTTPS？
**A**:
- 数据加密（防窃听）
- 数据完整性（防篡改）
- 身份验证（防冒充）

### Q2: Cookie和Token的区别？
**A**:
- **Cookie**: 自动发送，有大小限制，易受CSRF攻击
- **Token**: 手动携带，无大小限制，需防XSS

### Q3: HTTP缓存如何工作？
**A**:
```
强缓存：Cache-Control, Expires
  浏览器直接使用缓存，不请求服务器

协商缓存：ETag, Last-Modified
  浏览器询问服务器，服务器返回304或新内容
```

### Q4: RESTful和RPC的区别？
**A**:
- **RESTful**: 资源导向，HTTP方法，无状态
- **RPC**: 函数调用，自定义协议，可能有状态

---

## 参考资源

- 《HTTP权威指南》
- RFC 2616 (HTTP/1.1)
- RFC 7540 (HTTP/2)
- MDN Web Docs - HTTP
- OWASP - Web Security


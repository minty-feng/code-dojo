# 06-Python Web开发

Python在Web开发领域生态丰富。Flask轻量灵活，Django功能全面，FastAPI性能卓越。

## Flask基础

### 最小应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/user/<name>')
def greet(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 路由和视图

```python
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# GET请求
@app.route('/api/users', methods=['GET'])
def get_users():
    users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    return jsonify(users)

# POST请求
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    # 保存到数据库...
    return jsonify({'id': 123, 'name': name}), 201

# 路径参数
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    # 查询数据库...
    return jsonify({'id': user_id, 'name': 'Alice'})

# 查询参数
@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    return f'Search: {query}, Page: {page}'

# 表单数据
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    return 'Submitted'

# 模板渲染
@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html', name=name)
```

### Jinja2模板

```html
<!-- templates/profile.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Profile</title>
</head>
<body>
    <h1>Welcome, {{ name }}!</h1>
    
    {% if age >= 18 %}
        <p>Adult</p>
    {% else %}
        <p>Minor</p>
    {% endif %}
    
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
    
    <!-- 模板继承 -->
    {% extends "base.html" %}
    {% block content %}
        <p>Content</p>
    {% endblock %}
</body>
</html>
```

### 蓝图（Blueprint）

模块化路由，组织大型应用。

```python
# users.py
from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def list_users():
    return 'User list'

@users_bp.route('/<int:id>')
def get_user(id):
    return f'User {id}'

# app.py
from flask import Flask
from users import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)

# 访问：/users/ 和 /users/123
```

### 数据库集成

```python
# Flask-SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# 定义模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# 创建表
with app.app_context():
    db.create_all()

# CRUD操作
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id})

@app.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data['username']
    db.session.commit()
    return jsonify({'id': user.id})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
```

### RESTful API设计

```python
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class UserList(Resource):
    def get(self):
        # GET /api/users
        return {'users': []}
    
    def post(self):
        # POST /api/users
        data = request.get_json()
        return {'id': 123}, 201

class UserDetail(Resource):
    def get(self, user_id):
        # GET /api/users/:id
        return {'id': user_id, 'name': 'Alice'}
    
    def put(self, user_id):
        # PUT /api/users/:id
        return {'id': user_id}
    
    def delete(self, user_id):
        # DELETE /api/users/:id
        return '', 204

api.add_resource(UserList, '/api/users')
api.add_resource(UserDetail, '/api/users/<int:user_id>')
```

## Django基础

### 项目结构

```bash
# 创建项目
django-admin startproject myproject

# 创建应用
python manage.py startapp myapp

# 结构
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── myapp/
    ├── migrations/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
```

### 模型（ORM）

```python
# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username

# 数据库操作
User.objects.create(username='alice', email='alice@example.com', age=25)
User.objects.filter(age__gte=18)
User.objects.get(username='alice')
User.objects.all()
User.objects.count()
```

### 视图

```python
# views.py
from django.http import JsonResponse
from django.views import View

class UserView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username
        })
    
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create(**data)
        return JsonResponse({'id': user.id}, status=201)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:user_id>/', views.UserView.as_view()),
]
```

## FastAPI（现代高性能框架）

### 基本应用

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

users_db = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users", response_model=list[User])
async def list_users():
    return users_db

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: User):
    users_db.append(user)
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# 自动生成OpenAPI文档：/docs
# 运行：uvicorn main:app --reload
```

### 依赖注入

```python
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
async def read_items(db = Depends(get_db)):
    return db.query()
```

## HTTP客户端

### requests完整示例

```python
import requests

# 完整请求
response = requests.request(
    method='GET',
    url='https://api.example.com/data',
    params={'key': 'value'},
    headers={'Authorization': 'Bearer token'},
    timeout=10
)

# Session（连接复用）
session = requests.Session()
session.headers.update({'User-Agent': 'MyApp'})
session.get(url1)
session.post(url2, json=data)

# 错误处理
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # 4xx/5xx抛异常
except requests.Timeout:
    print("Timeout")
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.RequestException as e:
    print(f"Error: {e}")

# 下载文件
response = requests.get(url, stream=True)
with open('file.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### aiohttp（异步HTTP）

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_all(urls):
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# 运行
urls = ['http://example.com/1', 'http://example.com/2']
results = asyncio.run(fetch_all(urls))
```

## WSGI和ASGI

### WSGI（Web Server Gateway Interface）

```python
# WSGI应用
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [b'Hello, WSGI!']

# 运行（使用gunicorn）
# gunicorn app:application
```

### ASGI（Asynchronous SGI）

```python
# ASGI应用（FastAPI/Starlette）
async def application(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/plain']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, ASGI!',
    })

# 运行（使用uvicorn）
# uvicorn app:application
```

## 最佳实践

### API设计

```text
# RESTful路由设计
GET    /api/users           # 列表
POST   /api/users           # 创建
GET    /api/users/:id       # 详情
PUT    /api/users/:id       # 更新
DELETE /api/users/:id       # 删除

# 版本控制
/api/v1/users
/api/v2/users

# 分页
/api/users?page=1&limit=20

# 过滤
/api/users?age_gte=18&city=Beijing

# 排序
/api/users?sort=-created_at
```

### 错误处理

```python
from flask import Flask, jsonify

app = Flask(__name__)

# 自定义错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# 统一响应格式
def success_response(data, message='Success'):
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    })

def error_response(message, code=400):
    return jsonify({
        'success': False,
        'message': message
    }), code
```

### 认证和授权

```python
from flask import Flask, request
from functools import wraps
import jwt

SECRET_KEY = 'your-secret-key'

# JWT生成
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# JWT验证装饰器
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorator

@app.route('/api/protected')
@token_required
def protected(current_user_id):
    return jsonify({'user_id': current_user_id})
```

## 数据库操作

### SQLAlchemy ORM

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 连接数据库
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 定义模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# 创建表
Base.metadata.create_all(engine)

# 使用
session = Session()

# 创建
user = User(username='alice', email='alice@example.com')
session.add(user)
session.commit()

# 查询
users = session.query(User).all()
user = session.query(User).filter_by(username='alice').first()
user = session.query(User).filter(User.age > 18).all()

# 更新
user.email = 'newemail@example.com'
session.commit()

# 删除
session.delete(user)
session.commit()

# 关闭
session.close()
```

## 缓存

### Flask-Caching

```python
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# 缓存视图
@app.route('/expensive')
@cache.cached(timeout=60)  # 缓存60秒
def expensive_operation():
    # 耗时操作
    return result

# 带参数的缓存
@cache.memoize(timeout=60)
def get_user(user_id):
    # 根据参数缓存
    return db.query(user_id)

# 手动缓存
cache.set('key', 'value', timeout=300)
value = cache.get('key')
cache.delete('key')
```

## 异步Web框架

### aiohttp服务器

```python
from aiohttp import web

# 定义处理器
async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    return web.json_response({'message': f'Hello, {name}'})

async def handle_post(request):
    data = await request.json()
    return web.json_response(data, status=201)

# 创建应用
app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/hello/{name}', handle)
app.router.add_post('/data', handle_post)

# 运行
web.run_app(app, port=8080)
```

## WebSocket

### Flask-SocketIO

```python
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# 接收消息
@socketio.on('message')
def handle_message(message):
    print(f'Received: {message}')
    emit('response', {'data': 'Message received'})

# 自定义事件
@socketio.on('custom_event')
def handle_custom(data):
    emit('custom_response', data, broadcast=True)  # 广播

# 运行
socketio.run(app, port=5000)
```

## 测试

### unittest

```python
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        # 每个测试前执行
        self.data = [1, 2, 3]
    
    def tearDown(self):
        # 每个测试后执行
        pass
    
    def test_sum(self):
        self.assertEqual(sum(self.data), 6)
    
    def test_len(self):
        self.assertEqual(len(self.data), 3)
    
    def test_contains(self):
        self.assertIn(2, self.data)
    
    def test_raises(self):
        with self.assertRaises(ValueError):
            int('abc')

if __name__ == '__main__':
    unittest.main()
```

### pytest（推荐）

```python
# test_math.py
def test_sum():
    assert sum([1, 2, 3]) == 6

def test_contains():
    assert 2 in [1, 2, 3]

# fixture
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    assert len(sample_data) == 5

# 参数化测试
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected

# 运行
# pytest
# pytest test_math.py
# pytest -v  # 详细输出
```

## 部署

### Gunicorn（生产WSGI服务器）

```bash
# 安装
pip install gunicorn

# 运行Flask应用
gunicorn app:app -w 4 -b 0.0.0.0:8000

# 参数：
# -w 4：4个worker进程
# -b：绑定地址
# --reload：自动重载（开发用）
# --daemon：后台运行
```

### Uvicorn（ASGI服务器）

```bash
# 安装
pip install uvicorn


# 运行FastAPI应用
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# 开发模式
uvicorn app:app --reload
```

### Docker部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:8000"]
```

```bash
# 构建
docker build -t myapp .

# 运行
docker run -p 8000:8000 myapp
```

## 框架对比

| 框架 | 类型 | 学习曲线 | 性能 | 适用场景 |
|------|------|---------|------|---------|
| Flask | 微框架 | 平缓 | 中 | 小型API、原型 |
| Django | 全栈 | 陡峭 | 中 | 企业应用、CMS |
| FastAPI | 异步 | 平缓 | 高 | 现代API、微服务 |
| Tornado | 异步 | 中等 | 高 | 长连接、WebSocket |
| Bottle | 微框架 | 平缓 | 中 | 简单应用 |

**选择：**
- 快速原型：Flask
- 企业项目：Django
- 高性能API：FastAPI
- WebSocket：Tornado或FastAPI

**核心：** Python Web生态成熟，根据项目需求选择框架。


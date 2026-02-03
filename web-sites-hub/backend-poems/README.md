# 每日诗词后端服务 (Poems Service)

这是一个轻量级的 Python 后端服务，为首页的 "每日诗词" 模块提供随机诗句数据。

## 📅 项目功能

- 提供随机古诗词接口。
- 支持跨域请求 (CORS)，允许前端静态页面直接调用。
- 内置精选诗词库。

## 🛠 技术栈

- **Python 3**
- **FastAPI** (或同类轻量级框架)
- **JSON**: 数据交换格式

## 🚀 快速开始

### 1. 环境准备

```bash
cd backend-poems
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
uvicorn main:app --reload --port 8080
```

*注意：诗词服务默认运行在 **8080** 端口。*

## 🔌 接口说明

- **GET /api/poems/random**
    - 返回：JSON 对象，包含 `content` (诗句), `author` (作者), `origin` (出处)。

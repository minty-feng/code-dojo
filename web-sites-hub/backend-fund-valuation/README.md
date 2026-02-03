# 基金估值助手后端服务 (Fund Valuation Service)

这是一个基于 Python **FastAPI** 框架构建的后端微服务，为前端 "基金估值助手" 提供数据支持。

## 📅 项目功能

1.  **Mock 数据生成**: 实时生成模拟的基金净值、估算净值和涨跌幅数据。
2.  **查询接口 (`/api/funds`)**: 
    - 支持按基金名称/代码模糊搜索。
    - 支持按基金类型（股票型、混合型等）筛选。
3.  **数据导出 (`/api/funds/download`)**: 支持将查询结果导出为 CSV 文件。

## 🛠 技术栈

- **Python 3.9+**
- **FastAPI**: 高性能 Web 框架
- **Uvicorn**: ASGI 服务器
- **Faker**: 用于生成真实的模拟数据

## 🚀 快速开始

### 1. 环境准备

```bash
cd backend-fund-valuation
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
uvicorn main:app --reload --port 8081
```

服务启动后，API 地址为: `http://localhost:8081`

## 📝 API 文档

启动服务后，访问 `http://localhost:8081/docs` 可查看自动生成的 Swagger UI 文档。

# 04 运行与扩展手册

## 本地启动

```bash
cd /Users/didi/Workspace/code-dojo/web-sites-hub/backend-platform-py
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8300
```

## 数据库说明

- 默认数据库：`backend-platform-py/data/app.db`
- ORM：SQLAlchemy 2.x
- 建表方式：应用启动时自动 `create_all`
- 种子数据：首次启动自动插入 demo 用户、content、fund 数据

## 管理后台

- 访问地址：`http://127.0.0.1:8300/admin`
- 管理能力：浏览、搜索、增删改查 Users/Contents/Funds/Diary Entries
- 用途：单人开发阶段快速校验数据，不需要额外写脚本
- 默认管理员账号：`admin / admin123`
- 建议在本地 shell 中设置：
  - `ADMIN_USERNAME`
  - `ADMIN_PASSWORD`
  - `ADMIN_SESSION_SECRET`

## 新增业务域步骤

1. 在 `schemas/` 增加请求与响应模型  
2. 在 `repositories/` 增加数据访问逻辑  
3. 在 `services/` 增加业务逻辑  
4. 在 `routers/` 增加路由并注册到 `main.py`  
5. 在 `docs/02-api-design.md` 补齐接口说明  

## 未来拆分建议

当单模块出现以下情况时，考虑拆服务：
- 变更频率明显高于其他模块
- 单独扩容需求明显
- 安全边界独立（例如 auth、支付）

# 01 架构设计（单服务版）

## 目标

在单人开发阶段，用一个服务承接多个前端项目的接口需求，同时保证：
- 代码可维护
- 模块可拆分
- 规则可复用

## 分层说明

- `routers/`：HTTP 路由层，只做参数校验和协议转换
- `services/`：业务层，处理业务规则
- `repositories/`：数据访问层，封装 SQLAlchemy 查询与写入
- `schemas/`：请求/响应模型定义
- `core/`：配置、异常、统一响应、数据库连接与模型定义

## 请求流转

`Client -> Router -> Service -> Repository -> Service -> Router -> Response`

## 为什么这样设计

- 单服务部署简单
- 分层后边界清晰，便于测试
- 后续拆服务时，可按 `service + repository + schema` 直接迁移
- 使用 SQLite 持久化，重启后数据仍可保留，便于本地联调

# 02 API 设计

统一前缀：`/api/v1`

## Auth

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`

## Users

- `GET /api/v1/users/me`
- `PUT /api/v1/users/me`

## Content

- `GET /api/v1/content/items`
- `GET /api/v1/content/items/{item_id}`

## Fund

- `GET /api/v1/fund/list`
- `GET /api/v1/fund/download`
- `GET /api/v1/market/gold/quote`（现货黄金美元/盎司；可选服务端 `GOLDAPI_IO_TOKEN`）
- `GET /api/v1/market/gold/history?days=240`（天级别历史收盘价与明日区间估算）
- `GET /api/v1/market/gold/history-30m?points=240`（30分钟级别滚动收盘价与下个30分钟估算）

详见 `docs/09-fund-gold-desk.md`（产品边界、公式、配置与商用建议）。

## System

- `GET /api/v1/system/health`
- `GET /api/v1/system/info`

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

## Diary

- `POST /api/v1/diary/entries`
- `GET /api/v1/diary/entries`

## System

- `GET /api/v1/system/health`
- `GET /api/v1/system/info`

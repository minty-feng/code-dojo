# 版本号配置

## version.txt

统一管理 CSS/JS 的缓存版本号，用于 `?v=xxx` 查询参数。

- **修改方式**：编辑 `version.txt`，写入新版本号（如 `20260207`）
- **生效时机**：执行 `./package-joketop.sh` 打包时，会自动注入到所有 HTML
- **CDN 更新**：部署后，新版本号会触发浏览器/CDN 拉取最新资源

## 环境变量

打包时可通过 `ASSETS_VERSION` 覆盖：

```bash
ASSETS_VERSION=20260207 ./package-joketop.sh
```

## 推荐格式

- `YYYYMMDD`：如 20260206
- 或带时间 `YYYYMMDDHH`：如 2026020614

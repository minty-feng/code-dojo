# 03 错误码规范

统一响应结构：

```json
{
  "success": false,
  "code": "USER_NOT_FOUND",
  "message": "用户不存在",
  "data": null
}
```

## 通用错误码

- `BAD_REQUEST`：参数错误
- `UNAUTHORIZED`：未授权
- `FORBIDDEN`：无权限
- `NOT_FOUND`：资源不存在
- `INTERNAL_ERROR`：服务内部错误

## 业务错误码（示例）

- `INVALID_CREDENTIALS`：账号或密码错误
- `TOKEN_EXPIRED`：访问 token 已过期
- `USER_NOT_FOUND`：用户不存在
- `CONTENT_NOT_FOUND`：内容不存在
- `DIARY_EMPTY_TITLE`：日记标题为空

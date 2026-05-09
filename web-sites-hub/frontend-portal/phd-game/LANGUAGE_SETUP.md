# 语言设置说明

## 概述

PhD Simulator 现在支持中文和英文两种语言。默认语言设置为中文。

## 语言文件

- **中文语言文件**: `static/rulesets/default/lang_zh.yaml`
- **英文语言文件**: `static/rulesets/default/lang.yaml`

## 如何切换语言

### 方法1: 使用网页界面切换器
1. 在游戏界面右上角找到语言选择器
2. 选择 "中文" 或 "English"
3. 页面会自动重新加载并应用新语言

### 方法2: 修改配置文件
1. 编辑 `static/index.html` 文件
2. 找到 `app_config` 部分
3. 修改 `languageFileUrl` 字段：
   - 中文: `"languageFileUrl": "rulesets/default/lang_zh.yaml"`
   - 英文: `"languageFileUrl": "rulesets/default/lang.yaml"`

## 添加新语言

要添加新的语言支持：

1. 创建新的语言文件，例如 `lang_ja.yaml` (日语)
2. 翻译所有必要的文本键值
3. 在 `index.html` 中添加新的语言选项
4. 更新语言切换逻辑

## 语言文件结构

语言文件使用 YAML 格式，包含以下主要部分：

- `ui.*`: 用户界面文本
- `item.*`: 物品名称和描述
- `status.*`: 状态名称和描述
- `message.*`: 游戏事件消息

## 注意事项

- 语言切换需要重新加载页面
- 确保所有文本键都有对应的翻译
- 中文文本支持 Markdown 格式
- 变量占位符使用 `{{variable}}` 格式

## 故障排除

如果语言没有正确加载：

1. 检查浏览器控制台是否有错误信息
2. 确认语言文件路径正确
3. 验证 YAML 文件格式是否正确
4. 清除浏览器缓存后重试

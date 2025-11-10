# 🏠 minty-feng 个人网站主站

现代化的个人网站导航页面，作为各个子站点的统一入口。

## ✨ 特性

- 🎨 **现代化设计**：豪华大气的视觉设计，渐变背景和动画效果
- 🌙 **暗色模式**：支持主题切换，自动保存用户偏好
- 📱 **响应式设计**：完美适配桌面、平板、手机
- ⚡ **流畅动画**：页面加载和悬停效果
- 🎯 **无障碍支持**：语义化 HTML，键盘导航

## 🚀 快速开始

### 本地预览

```bash
# 启动本地预览服务器
./scripts/preview.sh

# 或指定端口
./scripts/preview.sh 3000
```

访问 `http://localhost:8000` 查看效果。

### 部署到 GitHub Pages

1. 将代码推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 选择源分支（通常是 `main`）
4. 访问 `https://YOUR_USERNAME.github.io/momo/`

### 自定义域名

1. 在 GitHub Pages 设置中添加自定义域名
2. 在域名 DNS 中添加 CNAME 记录指向 GitHub Pages
3. 等待 DNS 生效

## 📁 项目结构

```
momo/
├── index.html              # 主页面
├── assets/
│   ├── css/
│   │   └── main.css       # 主样式文件
│   └── js/
│       └── main.js        # 交互脚本
├── scripts/
│   └── preview.sh         # 预览脚本
└── README.md              # 本文件
```

## 🔧 自定义配置

### 修改站点链接

编辑 `index.html`，更新各个站点卡片的链接：

```html
<a href="https://your-blog-url.com" class="site-card" data-site="blog">
  ...
</a>
```

### 修改主题颜色

编辑 `assets/css/main.css`，修改 CSS 变量：

```css
:root {
    --gradient-blog: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-projects: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    ...
}
```

### 添加新站点

在 `index.html` 的 `sites-grid` 中添加新的站点卡片，参考现有的卡片结构。

## 📝 许可证

MIT License

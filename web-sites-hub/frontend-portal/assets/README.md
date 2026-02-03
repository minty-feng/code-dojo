# 🏠 主站导航页面

这是个人网站的主导航页面，作为各个子站点的统一入口。

## 📁 文件结构

```
frontend-portal/
├── index.html              # 主页面
├── assets/
│   ├── css/
│   │   └── main.css       # 主样式文件
│   └── js/
│       └── main.js        # 交互脚本
└── README.md              # 本文件
```

## 🎨 功能特性

- ✅ **现代化设计**：简洁美观的卡片式布局
- ✅ **响应式设计**：完美适配桌面、平板、手机
- ✅ **暗色模式**：支持主题切换，自动保存偏好
- ✅ **平滑动画**：页面加载和悬停效果
- ✅ **无障碍支持**：语义化 HTML，键盘导航

## 🚀 部署

### GitHub Pages

1. 将代码推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 选择源分支（通常是 `main` 或 `gh-pages`）
4. 访问 `https://YOUR_USERNAME.github.io/frontend-portal/`

### 自定义域名

1. 在 GitHub Pages 设置中添加自定义域名
2. 在域名 DNS 中添加 CNAME 记录指向 GitHub Pages
3. 等待 DNS 生效（通常几分钟到几小时）

## 🔧 自定义配置

### 修改站点链接

编辑 `index.html`，更新各个站点卡片的链接：

```html
<a href="https://your-blog-url.com" class="site-card">
  ...
</a>
```

### 修改主题颜色

编辑 `assets/css/main.css`，修改 CSS 变量：

```css
:root {
    --accent-blog: #3b82f6;
    --accent-projects: #8b5cf6;
    --accent-resume: #10b981;
    --accent-life: #f59e0b;
}
```

### 添加新站点

在 `sites-grid` 中添加新的站点卡片：

```html
<a href="https://your-site.com" class="site-card" data-site="yoursite">
    <div class="card-icon yoursite-icon">
        <!-- SVG icon -->
    </div>
    <div class="card-content">
        <h2 class="card-title">站点名称</h2>
        <p class="card-description">站点描述</p>
        <div class="card-tags">
            <span class="tag">标签1</span>
            <span class="tag">标签2</span>
        </div>
    </div>
    <div class="card-arrow">
        <!-- Arrow SVG -->
    </div>
</a>
```

然后在 CSS 中添加对应的图标样式：

```css
.yoursite-icon {
    background: linear-gradient(135deg, rgba(r, g, b, 0.1) 0%, rgba(r, g, b, 0.1) 100%);
    color: #your-color;
}

.site-card[data-site="yoursite"]::before {
    background: linear-gradient(135deg, #color1 0%, #color2 100%);
}
```

## 📱 浏览器支持

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)
- 移动端浏览器

## 🎯 性能优化

- ✅ 使用 CSS 变量实现主题切换，无需重新加载
- ✅ 使用 `will-change` 优化动画性能
- ✅ 使用 `IntersectionObserver` 实现懒加载动画
- ✅ 使用原生 JavaScript，无外部依赖

## 📝 许可证

MIT License








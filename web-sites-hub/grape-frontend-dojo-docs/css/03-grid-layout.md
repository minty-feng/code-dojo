# 03-Grid布局

## 📋 学习目标
- 掌握CSS Grid布局系统
- 理解网格轨道和单元格
- 实现复杂二维布局
- 响应式网格设计

## 🎯 Grid基础

### 启用Grid布局
```css
.container {
    display: grid;        /* 块级grid容器 */
    /* 或 */
    display: inline-grid; /* 行内grid容器 */
}
```

### 基本概念
```
Grid Container（网格容器）
Grid Item（网格项目）
Grid Line（网格线）
Grid Track（网格轨道）- 行或列
Grid Cell（网格单元格）
Grid Area（网格区域）
```

## 📏 容器属性

### grid-template-columns / rows
```css
.container {
    /* 固定宽度 */
    grid-template-columns: 200px 200px 200px;
    
    /* 百分比 */
    grid-template-columns: 33.33% 33.33% 33.33%;
    
    /* fr单位（fraction）*/
    grid-template-columns: 1fr 1fr 1fr;
    
    /* 混合单位 */
    grid-template-columns: 200px 1fr 2fr;
    
    /* 命名网格线 */
    grid-template-columns: [start] 1fr [middle] 1fr [end];
    
    /* repeat() 函数 */
    grid-template-columns: repeat(3, 1fr);
    grid-template-columns: repeat(3, 200px);
    grid-template-columns: repeat(2, 1fr 2fr); /* 1fr 2fr 1fr 2fr */
    
    /* auto-fill：自动填充 */
    grid-template-columns: repeat(auto-fill, 200px);
    
    /* auto-fit：自动适应 */
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

/* 行高度 */
.container {
    grid-template-rows: 100px 200px 100px;
    grid-template-rows: repeat(3, 1fr);
}
```

### minmax()函数
```css
.container {
    /* 最小200px，最大1fr */
    grid-template-columns: repeat(3, minmax(200px, 1fr));
    
    /* 最小内容大小，最大无限 */
    grid-template-columns: minmax(min-content, max-content);
    
    /* 响应式列宽 */
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```

### grid-template-areas
```css
.container {
    display: grid;
    grid-template-columns: 200px 1fr 200px;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "header header header"
        "sidebar main aside"
        "footer footer footer";
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

/* 空白单元格用 . 表示 */
.container {
    grid-template-areas:
        "header header ."
        "sidebar main main"
        ". footer footer";
}
```

### grid-template（简写）
```css
.container {
    /* grid-template-rows / grid-template-columns */
    grid-template: 100px 1fr / 200px 1fr;
    
    /* 配合areas */
    grid-template:
        "header header" 100px
        "sidebar main" 1fr
        "footer footer" 100px
        / 200px 1fr;
}
```

### gap（间距）
```css
.container {
    /* 行列间距 */
    gap: 20px;
    
    /* 分别设置 */
    row-gap: 20px;
    column-gap: 10px;
    
    /* 简写 */
    gap: 20px 10px; /* 行 列 */
}

/* 旧属性名（兼容性）*/
.container {
    grid-gap: 20px;
    grid-row-gap: 20px;
    grid-column-gap: 10px;
}
```

### justify-items（水平对齐）
```css
.container {
    /* 起点对齐 */
    justify-items: start;
    
    /* 终点对齐 */
    justify-items: end;
    
    /* 居中对齐 */
    justify-items: center;
    
    /* 拉伸（默认） */
    justify-items: stretch;
}
```

### align-items（垂直对齐）
```css
.container {
    align-items: start;
    align-items: end;
    align-items: center;
    align-items: stretch; /* 默认 */
}
```

### place-items（复合属性）
```css
.container {
    /* align-items justify-items */
    place-items: center center;
    place-items: start end;
}
```

### justify-content（网格整体水平对齐）
```css
.container {
    /* 网格总宽度小于容器时 */
    justify-content: start;
    justify-content: end;
    justify-content: center;
    justify-content: stretch;
    justify-content: space-around;
    justify-content: space-between;
    justify-content: space-evenly;
}
```

### align-content（网格整体垂直对齐）
```css
.container {
    height: 100vh;
    align-content: start;
    align-content: end;
    align-content: center;
    align-content: stretch;
    align-content: space-around;
    align-content: space-between;
    align-content: space-evenly;
}
```

### place-content（复合属性）
```css
.container {
    /* align-content justify-content */
    place-content: center center;
}
```

### grid-auto-columns / rows
```css
.container {
    /* 隐式网格的列宽 */
    grid-auto-columns: 100px;
    grid-auto-columns: minmax(100px, auto);
    
    /* 隐式网格的行高 */
    grid-auto-rows: 100px;
    grid-auto-rows: minmax(100px, auto);
}
```

### grid-auto-flow
```css
.container {
    /* 先行后列（默认） */
    grid-auto-flow: row;
    
    /* 先列后行 */
    grid-auto-flow: column;
    
    /* 稠密填充 */
    grid-auto-flow: row dense;
    grid-auto-flow: column dense;
}
```

## 🎁 项目属性

### grid-column / row
```css
.item {
    /* 列起始线 / 列结束线 */
    grid-column-start: 1;
    grid-column-end: 3;
    
    /* 简写 */
    grid-column: 1 / 3;
    
    /* 跨越2列 */
    grid-column: span 2;
    
    /* 从第2列开始，跨越2列 */
    grid-column: 2 / span 2;
}

.item {
    /* 行位置 */
    grid-row-start: 1;
    grid-row-end: 3;
    grid-row: 1 / 3;
    grid-row: span 2;
}

/* 同时设置行列 */
.item {
    grid-column: 1 / 3;
    grid-row: 1 / 3;
}
```

### grid-area
```css
/* 方式1：指定区域名称 */
.item {
    grid-area: header;
}

/* 方式2：指定位置 */
.item {
    /* row-start / column-start / row-end / column-end */
    grid-area: 1 / 1 / 3 / 3;
}

/* 等同于 */
.item {
    grid-row: 1 / 3;
    grid-column: 1 / 3;
}
```

### justify-self / align-self
```css
.item {
    /* 水平对齐 */
    justify-self: start;
    justify-self: end;
    justify-self: center;
    justify-self: stretch;
    
    /* 垂直对齐 */
    align-self: start;
    align-self: end;
    align-self: center;
    align-self: stretch;
}
```

### place-self
```css
.item {
    /* align-self justify-self */
    place-self: center center;
}
```

## 🎨 常见布局

### 等宽列布局
```css
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
```

### 圣杯布局
```css
.container {
    display: grid;
    min-height: 100vh;
    grid-template-columns: 200px 1fr 200px;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "header header header"
        "sidebar main aside"
        "footer footer footer";
    gap: 20px;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }
```

### 瀑布流布局
```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    grid-auto-rows: 10px;
    gap: 16px;
}

.item {
    /* 通过JavaScript动态计算 */
    grid-row-end: span var(--row-span);
}
```

### 响应式网格
```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

/* 自动适应：少于3个时拉伸，超过时换行 */
```

### 12列栅格系统
```css
.row {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 16px;
}

.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-12 { grid-column: span 12; }
```

### 卡片布局
```css
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 20px;
}

.card {
    display: grid;
    grid-template-rows: auto 1fr auto;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.card-header {
    padding: 16px;
    background-color: #f5f5f5;
}

.card-body {
    padding: 16px;
}

.card-footer {
    padding: 16px;
    border-top: 1px solid #ddd;
}
```

### 图片画廊
```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    grid-auto-rows: 200px;
    gap: 10px;
}

.gallery-item {
    overflow: hidden;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* 特殊尺寸 */
.gallery-item--large {
    grid-column: span 2;
    grid-row: span 2;
}

.gallery-item--wide {
    grid-column: span 2;
}

.gallery-item--tall {
    grid-row: span 2;
}
```

## 🔧 实战技巧

### 自动响应式布局
```css
.auto-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
}
```

### 固定侧边栏
```css
.layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 20px;
}

@media (max-width: 768px) {
    .layout {
        grid-template-columns: 1fr;
    }
}
```

### 重叠元素
```css
.overlap-container {
    display: grid;
}

.background {
    grid-column: 1;
    grid-row: 1;
}

.content {
    grid-column: 1;
    grid-row: 1;
    z-index: 1;
    place-self: center;
}
```

### 命名网格线
```css
.container {
    display: grid;
    grid-template-columns:
        [full-start] 1fr
        [content-start] minmax(0, 1200px) [content-end]
        1fr [full-end];
}

.full-width {
    grid-column: full-start / full-end;
}

.content-width {
    grid-column: content-start / content-end;
}
```

## 📚 Grid vs Flexbox

### 何时使用Grid
- 二维布局（行和列）
- 复杂页面布局
- 需要精确控制行列
- 重叠元素布局

### 何时使用Flexbox
- 一维布局（行或列）
- 组件内部布局
- 内容驱动的布局
- 简单对齐需求

### 结合使用
```css
/* Grid用于页面布局 */
.page {
    display: grid;
    grid-template-areas:
        "header"
        "main"
        "footer";
}

/* Flexbox用于组件内部 */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

## 📚 完整示例

### 杂志风格布局
```html
<div class="magazine">
    <div class="item item-1">Article 1</div>
    <div class="item item-2">Article 2</div>
    <div class="item item-3">Article 3</div>
    <div class="item item-4">Article 4</div>
    <div class="item item-5">Article 5</div>
</div>

<style>
.magazine {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(3, 200px);
    gap: 10px;
}

.item-1 {
    grid-column: 1 / 3;
    grid-row: 1 / 3;
}

.item-2 {
    grid-column: 3 / 5;
}

.item-3 {
    grid-column: 3 / 5;
}

.item-4 {
    grid-column: 1 / 3;
}

.item-5 {
    grid-column: 3 / 5;
}
</style>
```

### 仪表板布局
```html
<div class="dashboard">
    <header class="header">Header</header>
    <nav class="sidebar">Sidebar</nav>
    <main class="main">Main Content</main>
    <aside class="widgets">Widgets</aside>
    <footer class="footer">Footer</footer>
</div>

<style>
.dashboard {
    display: grid;
    height: 100vh;
    grid-template-columns: 250px 1fr 300px;
    grid-template-rows: 60px 1fr 40px;
    grid-template-areas:
        "header header header"
        "sidebar main widgets"
        "footer footer footer";
    gap: 10px;
    padding: 10px;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.widgets { grid-area: widgets; }
.footer { grid-area: footer; }

@media (max-width: 1024px) {
    .dashboard {
        grid-template-columns: 200px 1fr;
        grid-template-areas:
            "header header"
            "sidebar main"
            "footer footer";
    }
    
    .widgets {
        display: none;
    }
}

@media (max-width: 768px) {
    .dashboard {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "main"
            "footer";
    }
    
    .sidebar {
        display: none;
    }
}
</style>
```

## 📚 实践练习

### 练习1：响应式网格
创建一个响应式产品网格：
- 大屏4列，中屏3列，平板2列，手机1列
- 使用auto-fit和minmax

### 练习2：复杂布局
实现一个新闻网站首页：
- 头部、侧边栏、主内容区、广告位、底部
- 某些文章占据2x2格子
- 响应式适配

### 练习3：图片画廊
创建一个图片画廊：
- 自动适应列数
- 支持不同尺寸的图片
- 悬停效果

## 📚 参考资料
- [CSS Grid完全指南](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [MDN Grid布局](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Grid_Layout)
- [Grid Garden](https://cssgridgarden.com/) - 游戏学习
- [Grid by Example](https://gridbyexample.com/)


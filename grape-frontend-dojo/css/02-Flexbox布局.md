# 02-Flexbox布局

## 📋 学习目标
- 理解Flexbox布局模型
- 掌握容器和项目属性
- 实现常见布局模式
- 解决实际布局问题

## 🎯 Flexbox基础

### 启用Flex布局
```css
.container {
    display: flex;        /* 块级flex容器 */
    /* 或 */
    display: inline-flex; /* 行内flex容器 */
}
```

### 主轴和交叉轴
```
默认（flex-direction: row）：
→ 主轴（Main Axis）水平方向
↓ 交叉轴（Cross Axis）垂直方向

flex-direction: column 时：
↓ 主轴垂直方向
→ 交叉轴水平方向
```

## 📦 容器属性

### flex-direction（主轴方向）
```css
.container {
    /* 水平，起点在左 */
    flex-direction: row;
    
    /* 水平，起点在右 */
    flex-direction: row-reverse;
    
    /* 垂直，起点在上 */
    flex-direction: column;
    
    /* 垂直，起点在下 */
    flex-direction: column-reverse;
}
```

### flex-wrap（换行）
```css
.container {
    /* 不换行（默认） */
    flex-wrap: nowrap;
    
    /* 换行，第一行在上 */
    flex-wrap: wrap;
    
    /* 换行，第一行在下 */
    flex-wrap: wrap-reverse;
}
```

### flex-flow（复合属性）
```css
.container {
    /* flex-direction 和 flex-wrap 的简写 */
    flex-flow: row wrap;
    flex-flow: column nowrap;
}
```

### justify-content（主轴对齐）
```css
.container {
    /* 起点对齐（默认） */
    justify-content: flex-start;
    
    /* 终点对齐 */
    justify-content: flex-end;
    
    /* 居中对齐 */
    justify-content: center;
    
    /* 两端对齐，项目间间隔相等 */
    justify-content: space-between;
    
    /* 每个项目两侧间隔相等 */
    justify-content: space-around;
    
    /* 项目间间隔相等（包括首尾） */
    justify-content: space-evenly;
}

/* 实际应用 */
.header {
    display: flex;
    justify-content: space-between;
}
/* Logo在左，导航在右 */
```

### align-items（交叉轴对齐）
```css
.container {
    /* 起点对齐 */
    align-items: flex-start;
    
    /* 终点对齐 */
    align-items: flex-end;
    
    /* 居中对齐 */
    align-items: center;
    
    /* 基线对齐 */
    align-items: baseline;
    
    /* 拉伸填满（默认） */
    align-items: stretch;
}

/* 垂直居中 */
.center-box {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
```

### align-content（多行对齐）
```css
.container {
    flex-wrap: wrap;
    
    /* 起点对齐 */
    align-content: flex-start;
    
    /* 终点对齐 */
    align-content: flex-end;
    
    /* 居中对齐 */
    align-content: center;
    
    /* 两端对齐 */
    align-content: space-between;
    
    /* 环绕对齐 */
    align-content: space-around;
    
    /* 均匀分布 */
    align-content: space-evenly;
    
    /* 拉伸（默认） */
    align-content: stretch;
}
```

### gap（间距）
```css
.container {
    display: flex;
    
    /* 行和列间距 */
    gap: 20px;
    
    /* 分别设置 */
    row-gap: 20px;
    column-gap: 10px;
    
    /* 简写 */
    gap: 20px 10px; /* 行 列 */
}
```

## 🎁 项目属性

### order（排序）
```css
.item {
    /* 数值越小越靠前，默认0 */
    order: 1;
}

.item:first-child {
    order: 2; /* 放到最后 */
}

.item:last-child {
    order: -1; /* 放到最前 */
}
```

### flex-grow（放大比例）
```css
.item {
    /* 不放大（默认） */
    flex-grow: 0;
    
    /* 放大，占据剩余空间 */
    flex-grow: 1;
}

/* 三列布局，中间列自适应 */
.sidebar {
    flex-grow: 0;
    width: 200px;
}

.main {
    flex-grow: 1; /* 占据剩余空间 */
}
```

### flex-shrink（缩小比例）
```css
.item {
    /* 空间不足时缩小，默认1 */
    flex-shrink: 1;
    
    /* 不缩小 */
    flex-shrink: 0;
}

/* 防止图片缩小 */
img {
    flex-shrink: 0;
}
```

### flex-basis（初始大小）
```css
.item {
    /* 根据内容自动计算（默认） */
    flex-basis: auto;
    
    /* 固定大小 */
    flex-basis: 200px;
    
    /* 百分比 */
    flex-basis: 50%;
    
    /* 0需要带单位 */
    flex-basis: 0px;
}
```

### flex（复合属性）
```css
.item {
    /* flex-grow flex-shrink flex-basis */
    flex: 1;           /* 1 1 0% */
    flex: auto;        /* 1 1 auto */
    flex: none;        /* 0 0 auto */
    flex: 0 1 auto;    /* 默认值 */
    
    /* 常用值 */
    flex: 1;           /* 平均分配空间 */
    flex: 0 0 200px;   /* 固定宽度 */
}

/* 三列等宽布局 */
.col {
    flex: 1;
}

/* 固定宽度 + 自适应 */
.sidebar {
    flex: 0 0 250px;
}
.main {
    flex: 1;
}
```

### align-self（单个项目对齐）
```css
.item {
    /* 继承容器的align-items（默认） */
    align-self: auto;
    
    /* 其他值同align-items */
    align-self: flex-start;
    align-self: flex-end;
    align-self: center;
    align-self: baseline;
    align-self: stretch;
}

/* 某个项目特殊对齐 */
.special-item {
    align-self: flex-end;
}
```

## 🎨 常见布局

### 水平垂直居中
```css
.center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
```

### 等高列布局
```css
.row {
    display: flex;
}

.col {
    flex: 1;
    /* 自动等高 */
}
```

### 圣杯布局
```css
.container {
    display: flex;
    min-height: 100vh;
    flex-direction: column;
}

.header, .footer {
    flex: 0 0 auto;
}

.content {
    display: flex;
    flex: 1;
}

.sidebar {
    flex: 0 0 200px;
}

.main {
    flex: 1;
}
```

### 固定底部
```css
.page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.content {
    flex: 1;
}

.footer {
    flex: 0 0 auto;
}
```

### 网格布局
```css
.grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.grid-item {
    flex: 0 0 calc(33.333% - 14px);
}

/* 响应式 */
@media (max-width: 768px) {
    .grid-item {
        flex: 0 0 calc(50% - 10px);
    }
}

@media (max-width: 480px) {
    .grid-item {
        flex: 0 0 100%;
    }
}
```

### 导航栏
```css
/* 水平导航 */
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-left {
    display: flex;
    gap: 20px;
}

.nav-right {
    display: flex;
    gap: 10px;
    margin-left: auto;
}

/* 垂直导航 */
.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
```

### 卡片布局
```css
.card {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.card-header {
    flex: 0 0 auto;
}

.card-body {
    flex: 1;
}

.card-footer {
    flex: 0 0 auto;
}
```

### 媒体对象
```css
.media {
    display: flex;
    gap: 16px;
}

.media-image {
    flex: 0 0 auto;
    width: 100px;
}

.media-body {
    flex: 1;
}
```

## 🔧 实战技巧

### 防止内容溢出
```css
.item {
    /* 防止flex项目被挤压 */
    min-width: 0;
    min-height: 0;
}

.text-container {
    flex: 1;
    min-width: 0;
}

.text {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
```

### 自动边距对齐
```css
.container {
    display: flex;
}

.item:last-child {
    margin-left: auto; /* 推到最右边 */
}

/* 垂直居中某个元素 */
.special {
    margin-top: auto;
    margin-bottom: auto;
}
```

### 响应式Flexbox
```css
.container {
    display: flex;
    flex-direction: column;
}

@media (min-width: 768px) {
    .container {
        flex-direction: row;
    }
}

/* 或使用flex-wrap */
.responsive-flex {
    display: flex;
    flex-wrap: wrap;
}

.item {
    flex: 1 1 300px; /* 最小300px，会自动换行 */
}
```

## 📚 完整示例

### 响应式头部
```html
<header class="header">
    <div class="logo">Logo</div>
    <nav class="nav">
        <a href="#">首页</a>
        <a href="#">产品</a>
        <a href="#">关于</a>
    </nav>
    <div class="actions">
        <button>登录</button>
        <button>注册</button>
    </div>
</header>

<style>
.header {
    display: flex;
    align-items: center;
    padding: 16px;
    gap: 20px;
    flex-wrap: wrap;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

.nav {
    display: flex;
    gap: 20px;
    margin-right: auto;
}

.actions {
    display: flex;
    gap: 10px;
}

@media (max-width: 768px) {
    .header {
        flex-direction: column;
        align-items: stretch;
    }
    
    .nav {
        flex-direction: column;
        margin-right: 0;
    }
}
</style>
```

### 产品卡片网格
```html
<div class="products">
    <div class="product-card">...</div>
    <div class="product-card">...</div>
    <div class="product-card">...</div>
</div>

<style>
.products {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    padding: 24px;
}

.product-card {
    flex: 1 1 300px;
    max-width: calc(33.333% - 16px);
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

@media (max-width: 1024px) {
    .product-card {
        max-width: calc(50% - 12px);
    }
}

@media (max-width: 640px) {
    .product-card {
        max-width: 100%;
    }
}
</style>
```

## 📚 实践练习

### 练习1：导航栏
实现一个响应式导航栏：
- Logo在左，导航在中，按钮在右
- 移动端垂直排列
- 使用Flexbox

### 练习2：卡片布局
创建响应式卡片网格：
- 大屏3列，中屏2列，小屏1列
- 卡片等高
- 图片、标题、内容、按钮

### 练习3：圣杯布局
实现经典圣杯布局：
- 头部和底部固定高度
- 中间内容区自适应
- 左右侧边栏固定宽度
- 主内容区自适应

## 💡 常见问题

**Q: flex: 1 和 flex-grow: 1 的区别？**
A: `flex: 1` 等于 `flex: 1 1 0%`，而单独设置 `flex-grow: 1` 时，flex-shrink和flex-basis保持默认值。

**Q: 为什么内容溢出容器？**
A: Flex项目默认不会缩小到小于内容的尺寸，设置 `min-width: 0` 或 `min-height: 0` 可解决。

**Q: 如何实现最后一项占据剩余空间？**
A: 使用 `margin-left: auto` 或 `flex-grow: 1`。

## 📚 参考资料
- [CSS Flexbox完全指南](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [MDN Flexbox](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Flexible_Box_Layout)
- [Flexbox Froggy](https://flexboxfroggy.com/) - 游戏学习


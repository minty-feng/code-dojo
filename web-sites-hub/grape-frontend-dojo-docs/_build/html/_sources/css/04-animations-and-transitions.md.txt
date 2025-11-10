# 04-动画与过渡

## 📋 学习目标
- 掌握CSS过渡(Transition)
- 学习关键帧动画(Animation)
- 理解Transform变换
- 实现流畅动画效果

## 🎬 CSS Transition

### 基本用法
```css
.button {
    background-color: #007bff;
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: #0056b3;
}
```

### transition属性
```css
.element {
    /* 单个属性 */
    transition-property: background-color;
    transition-duration: 0.3s;
    transition-timing-function: ease;
    transition-delay: 0s;
    
    /* 简写 */
    transition: background-color 0.3s ease 0s;
    
    /* 多个属性 */
    transition: 
        background-color 0.3s ease,
        transform 0.2s cubic-bezier(0.4, 0, 0.2, 1),
        opacity 0.3s linear 0.1s;
    
    /* 所有属性 */
    transition: all 0.3s ease;
}
```

### timing-function
```css
.element {
    /* 预定义 */
    transition-timing-function: linear;
    transition-timing-function: ease;        /* 默认 */
    transition-timing-function: ease-in;
    transition-timing-function: ease-out;
    transition-timing-function: ease-in-out;
    
    /* steps */
    transition-timing-function: steps(4);
    transition-timing-function: steps(4, jump-start);
    
    /* 贝塞尔曲线 */
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 实际应用
```css
/* 按钮悬停效果 */
.btn {
    padding: 12px 24px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn:active {
    transform: translateY(0);
}

/* 链接下划线动画 */
.link {
    position: relative;
    text-decoration: none;
    color: #333;
}

.link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #007bff;
    transition: width 0.3s ease;
}

.link:hover::after {
    width: 100%;
}

/* 卡片悬停 */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}
```

## 🎨 CSS Animation

### @keyframes定义
```css
/* 从-到 */
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

/* 百分比 */
@keyframes slideIn {
    0% {
        transform: translateX(-100%);
    }
    50% {
        transform: translateX(10px);
    }
    100% {
        transform: translateX(0);
    }
}

/* 多个属性 */
@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-20px);
    }
}
```

### animation属性
```css
.element {
    /* 完整写法 */
    animation-name: fadeIn;
    animation-duration: 1s;
    animation-timing-function: ease;
    animation-delay: 0s;
    animation-iteration-count: 1;
    animation-direction: normal;
    animation-fill-mode: none;
    animation-play-state: running;
    
    /* 简写 */
    animation: fadeIn 1s ease 0s 1 normal none running;
    
    /* 常用简写 */
    animation: fadeIn 1s ease;
    animation: slideIn 0.5s ease-out forwards;
    animation: bounce 2s infinite;
}
```

### animation详细属性
```css
.element {
    /* 动画名称 */
    animation-name: slideIn;
    
    /* 持续时间 */
    animation-duration: 2s;
    
    /* 计时函数 */
    animation-timing-function: ease-in-out;
    
    /* 延迟 */
    animation-delay: 0.5s;
    
    /* 循环次数 */
    animation-iteration-count: 3;
    animation-iteration-count: infinite;
    
    /* 方向 */
    animation-direction: normal;         /* 正向 */
    animation-direction: reverse;        /* 反向 */
    animation-direction: alternate;      /* 交替 */
    animation-direction: alternate-reverse;
    
    /* 填充模式 */
    animation-fill-mode: none;           /* 默认 */
    animation-fill-mode: forwards;       /* 保持最后状态 */
    animation-fill-mode: backwards;      /* 应用第一帧 */
    animation-fill-mode: both;           /* 两者都应用 */
    
    /* 播放状态 */
    animation-play-state: running;
    animation-play-state: paused;
}

/* 暂停动画示例 */
.animated:hover {
    animation-play-state: paused;
}
```

### 常用动画效果
```css
/* 淡入 */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* 滑入 */
@keyframes slideInLeft {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* 缩放 */
@keyframes zoomIn {
    from {
        transform: scale(0);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

/* 旋转 */
@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* 弹跳 */
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-30px);
    }
    60% {
        transform: translateY(-15px);
    }
}

/* 摇晃 */
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
    20%, 40%, 60%, 80% { transform: translateX(10px); }
}

/* 脉冲 */
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* 呼吸灯 */
@keyframes breathing {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
```

## 🔄 Transform

### 2D变换
```css
/* 平移 */
.element {
    transform: translate(50px, 100px);
    transform: translateX(50px);
    transform: translateY(100px);
}

/* 缩放 */
.element {
    transform: scale(1.5);           /* 等比缩放 */
    transform: scale(2, 1.5);        /* 宽高不等比 */
    transform: scaleX(2);
    transform: scaleY(1.5);
}

/* 旋转 */
.element {
    transform: rotate(45deg);
    transform: rotate(-90deg);
}

/* 倾斜 */
.element {
    transform: skew(15deg, 10deg);
    transform: skewX(15deg);
    transform: skewY(10deg);
}

/* 组合变换 */
.element {
    transform: translate(50px, 50px) rotate(45deg) scale(1.2);
}
```

### 3D变换
```css
/* 3D平移 */
.element {
    transform: translate3d(50px, 100px, 0);
    transform: translateZ(50px);
}

/* 3D旋转 */
.element {
    transform: rotateX(45deg);
    transform: rotateY(45deg);
    transform: rotateZ(45deg);
    transform: rotate3d(1, 1, 1, 45deg);
}

/* 3D缩放 */
.element {
    transform: scale3d(2, 2, 2);
    transform: scaleZ(2);
}

/* 透视 */
.container {
    perspective: 1000px;
}

.element {
    transform: rotateY(45deg);
}

/* transform-style */
.parent {
    transform-style: preserve-3d;
}

/* backface-visibility */
.element {
    backface-visibility: hidden;
}
```

### transform-origin
```css
.element {
    /* 默认中心 */
    transform-origin: center center;
    transform-origin: 50% 50%;
    
    /* 左上角 */
    transform-origin: top left;
    transform-origin: 0 0;
    
    /* 自定义 */
    transform-origin: 100px 50px;
    transform-origin: 20% 80%;
}

/* 翻转卡片示例 */
.card {
    transform-origin: center center;
    transition: transform 0.6s;
}

.card:hover {
    transform: rotateY(180deg);
}
```

## 🎯 实战案例

### 加载动画
```html
<div class="spinner"></div>

<style>
.spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
```

### 进度条动画
```html
<div class="progress-bar">
    <div class="progress"></div>
</div>

<style>
.progress-bar {
    width: 100%;
    height: 4px;
    background-color: #f0f0f0;
    overflow: hidden;
}

.progress {
    height: 100%;
    background-color: #007bff;
    animation: loading 2s ease-in-out infinite;
}

@keyframes loading {
    0% {
        transform: translateX(-100%);
    }
    100% {
        transform: translateX(100%);
    }
}
</style>
```

### 翻转卡片
```html
<div class="card-flip">
    <div class="card-front">Front</div>
    <div class="card-back">Back</div>
</div>

<style>
.card-flip {
    width: 200px;
    height: 300px;
    position: relative;
    perspective: 1000px;
}

.card-front,
.card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    transition: transform 0.6s;
}

.card-back {
    transform: rotateY(180deg);
}

.card-flip:hover .card-front {
    transform: rotateY(-180deg);
}

.card-flip:hover .card-back {
    transform: rotateY(0);
}
</style>
```

### 脉冲按钮
```html
<button class="pulse-button">Click Me</button>

<style>
.pulse-button {
    position: relative;
    padding: 12px 24px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.pulse-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 4px;
    background-color: #007bff;
    opacity: 0.7;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {
        transform: scale(1);
        opacity: 0.7;
    }
    50% {
        transform: scale(1.05);
        opacity: 0;
    }
    100% {
        transform: scale(1);
        opacity: 0;
    }
}
</style>
```

### 打字机效果
```html
<div class="typewriter">
    <p>Hello, World!</p>
</div>

<style>
.typewriter p {
    overflow: hidden;
    border-right: 0.15em solid #333;
    white-space: nowrap;
    margin: 0;
    animation: 
        typing 3.5s steps(13, end),
        blink-caret 0.75s step-end infinite;
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blink-caret {
    from, to { border-color: transparent; }
    50% { border-color: #333; }
}
</style>
```

### 悬浮效果
```css
.hover-lift {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

/* 3D悬浮 */
.hover-3d {
    transition: transform 0.3s ease;
}

.hover-3d:hover {
    transform: perspective(1000px) rotateX(10deg) translateY(-10px);
}
```

## ⚡ 性能优化

### 使用transform和opacity
```css
/* ✅ 高性能（GPU加速） */
.element {
    transform: translateX(100px);
    opacity: 0.5;
}

/* ❌ 低性能（触发重排） */
.element {
    left: 100px;
    display: none;
}
```

### will-change提示
```css
.element {
    /* 提前告知浏览器将要变化的属性 */
    will-change: transform, opacity;
}

.element:hover {
    transform: scale(1.1);
    opacity: 0.8;
}

/* 注意：不要滥用will-change */
```

### 使用transform3d强制GPU加速
```css
.element {
    /* 即使是2D变换，也使用3D */
    transform: translate3d(0, 0, 0);
    transform: translateZ(0);
}
```

## 💡 最佳实践

### 1. 选择合适的属性
```css
/* 优先使用这些属性（不触发重排） */
transform
opacity

/* 避免动画这些属性（触发重排/重绘） */
width, height
top, left
margin, padding
```

### 2. 使用requestAnimationFrame
```javascript
function animate() {
    element.style.transform = `translateX(${x}px)`;
    x++;
    requestAnimationFrame(animate);
}
```

### 3. 减少动画复杂度
```css
/* ❌ 复杂动画 */
.element {
    animation: complex 1s ease-in-out infinite;
}

@keyframes complex {
    0% { transform: translate(0, 0) rotate(0) scale(1); }
    25% { transform: translate(50px, 0) rotate(45deg) scale(1.2); }
    50% { transform: translate(50px, 50px) rotate(90deg) scale(1); }
    75% { transform: translate(0, 50px) rotate(135deg) scale(0.8); }
    100% { transform: translate(0, 0) rotate(180deg) scale(1); }
}

/* ✅ 简化动画 */
.element {
    animation: simple 1s ease-in-out infinite;
}

@keyframes simple {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}
```

## 📚 实践练习

### 练习1：加载动画
创建3种不同的加载动画：
- 旋转圆圈
- 跳动的点
- 进度条

### 练习2：交互卡片
实现一个交互卡片：
- 悬停时抬起效果
- 点击时翻转
- 平滑过渡

### 练习3：导航菜单
创建动画导航菜单：
- 下拉菜单滑入效果
- 菜单项逐个淡入
- 悬停高亮动画

## 📚 参考资料
- [MDN CSS Transitions](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Transitions)
- [MDN CSS Animations](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Animations)
- [Animate.css](https://animate.style/) - 动画库
- [Cubic Bezier](https://cubic-bezier.com/) - 贝塞尔曲线编辑器


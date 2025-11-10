# 04-Canvas与SVG

## 📋 学习目标
- 掌握Canvas 2D绘图API
- 理解SVG矢量图形
- 学习Canvas与SVG的应用场景
- 实现图表和交互式图形

## 🎨 Canvas基础

### Canvas元素
```html
<canvas id="myCanvas" width="800" height="600">
    您的浏览器不支持Canvas
</canvas>

<script>
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
</script>
```

**要点**：
- width和height属性设置画布尺寸（默认300x150）
- 不要用CSS设置尺寸，会导致缩放失真
- 使用getContext('2d')获取2D渲染上下文

### 绘制基本形状

#### 矩形
```javascript
const ctx = canvas.getContext('2d');

// 填充矩形
ctx.fillStyle = '#ff6b6b';
ctx.fillRect(10, 10, 100, 100);

// 描边矩形
ctx.strokeStyle = '#339af0';
ctx.lineWidth = 2;
ctx.strokeRect(120, 10, 100, 100);

// 清除矩形
ctx.clearRect(50, 50, 20, 20);
```

#### 路径绘制
```javascript
// 三角形
ctx.beginPath();
ctx.moveTo(250, 10);
ctx.lineTo(300, 110);
ctx.lineTo(200, 110);
ctx.closePath();
ctx.fillStyle = '#51cf66';
ctx.fill();
ctx.strokeStyle = '#2f9e44';
ctx.stroke();

// 圆形
ctx.beginPath();
ctx.arc(400, 60, 50, 0, Math.PI * 2);
ctx.fillStyle = '#ffd43b';
ctx.fill();

// 圆弧
ctx.beginPath();
ctx.arc(500, 60, 50, 0, Math.PI, false);
ctx.strokeStyle = '#ff6b6b';
ctx.lineWidth = 3;
ctx.stroke();

// 贝塞尔曲线
ctx.beginPath();
ctx.moveTo(600, 10);
ctx.quadraticCurveTo(650, 10, 650, 60); // 二次贝塞尔
ctx.bezierCurveTo(650, 110, 600, 110, 600, 60); // 三次贝塞尔
ctx.stroke();
```

### 样式和颜色

#### 颜色设置
```javascript
// 填充颜色
ctx.fillStyle = '#ff6b6b';
ctx.fillStyle = 'rgb(255, 107, 107)';
ctx.fillStyle = 'rgba(255, 107, 107, 0.5)';

// 描边颜色
ctx.strokeStyle = '#339af0';

// 渐变
const gradient = ctx.createLinearGradient(0, 0, 200, 0);
gradient.addColorStop(0, '#ff6b6b');
gradient.addColorStop(1, '#339af0');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 200, 100);

// 径向渐变
const radialGradient = ctx.createRadialGradient(100, 100, 10, 100, 100, 50);
radialGradient.addColorStop(0, '#fff');
radialGradient.addColorStop(1, '#000');
ctx.fillStyle = radialGradient;
ctx.fillRect(50, 50, 100, 100);

// 图案
const img = new Image();
img.src = 'pattern.png';
img.onload = () => {
    const pattern = ctx.createPattern(img, 'repeat');
    ctx.fillStyle = pattern;
    ctx.fillRect(0, 0, 200, 200);
};
```

#### 线条样式
```javascript
ctx.lineWidth = 5;
ctx.lineCap = 'round';  // butt, round, square
ctx.lineJoin = 'round'; // miter, round, bevel
ctx.setLineDash([5, 10]); // 虚线
ctx.lineDashOffset = 0;
```

### 文本绘制
```javascript
// 填充文本
ctx.font = '30px Arial';
ctx.fillStyle = '#000';
ctx.fillText('Hello Canvas', 10, 50);

// 描边文本
ctx.strokeStyle = '#ff6b6b';
ctx.lineWidth = 2;
ctx.strokeText('Hello Canvas', 10, 100);

// 文本对齐
ctx.textAlign = 'left';   // left, right, center, start, end
ctx.textBaseline = 'top'; // top, middle, bottom, alphabetic, hanging

// 测量文本
const metrics = ctx.measureText('Hello');
console.log(metrics.width); // 文本宽度
```

### 图像处理
```javascript
const img = new Image();
img.src = 'photo.jpg';
img.onload = () => {
    // 绘制图像
    ctx.drawImage(img, 0, 0);
    
    // 缩放
    ctx.drawImage(img, 0, 0, 200, 150);
    
    // 裁剪和绘制
    ctx.drawImage(
        img,
        50, 50, 100, 100,  // 源图像裁剪区域
        0, 0, 200, 200     // 目标画布区域
    );
};

// 像素操作
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
const pixels = imageData.data; // [r, g, b, a, r, g, b, a, ...]

// 灰度化
for (let i = 0; i < pixels.length; i += 4) {
    const avg = (pixels[i] + pixels[i + 1] + pixels[i + 2]) / 3;
    pixels[i] = avg;     // R
    pixels[i + 1] = avg; // G
    pixels[i + 2] = avg; // B
}

ctx.putImageData(imageData, 0, 0);
```

### 变换

#### 基本变换
```javascript
// 平移
ctx.translate(100, 100);

// 旋转（弧度）
ctx.rotate(Math.PI / 4);

// 缩放
ctx.scale(2, 2);

// 重置变换
ctx.setTransform(1, 0, 0, 1, 0, 0);

// 矩阵变换
ctx.transform(1, 0, 0, 1, 0, 0);
```

#### 保存和恢复状态
```javascript
ctx.fillStyle = '#ff6b6b';
ctx.save(); // 保存当前状态

ctx.fillStyle = '#339af0';
ctx.fillRect(0, 0, 100, 100);

ctx.restore(); // 恢复之前的状态
ctx.fillRect(120, 0, 100, 100); // 使用红色
```

### 动画

#### 基本动画循环
```javascript
let x = 0;

function animate() {
    // 清除画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 绘制
    ctx.fillStyle = '#ff6b6b';
    ctx.fillRect(x, 100, 50, 50);
    
    // 更新位置
    x += 2;
    if (x > canvas.width) x = -50;
    
    // 下一帧
    requestAnimationFrame(animate);
}

animate();
```

#### 小球弹跳动画
```javascript
const ball = {
    x: 100,
    y: 100,
    vx: 5,
    vy: 2,
    radius: 20,
    color: '#ff6b6b'
};

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    ctx.closePath();
}

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBall();
    
    // 更新位置
    ball.x += ball.vx;
    ball.y += ball.vy;
    
    // 边界检测
    if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        ball.vx = -ball.vx;
    }
    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        ball.vy = -ball.vy;
    }
    
    requestAnimationFrame(update);
}

update();
```

## 📐 SVG基础

### SVG元素
```html
<!-- 内联SVG -->
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="80" fill="#ff6b6b"/>
</svg>

<!-- 外部SVG文件 -->
<img src="image.svg" alt="SVG图片">
<object data="image.svg" type="image/svg+xml"></object>
<embed src="image.svg" type="image/svg+xml">

<!-- 背景图片 -->
<div style="background-image: url('image.svg')"></div>
```

### 基本形状

#### 矩形
```html
<svg width="300" height="200">
    <!-- 基本矩形 -->
    <rect x="10" y="10" width="100" height="80" fill="#ff6b6b"/>
    
    <!-- 圆角矩形 -->
    <rect x="120" y="10" width="100" height="80" rx="10" ry="10" fill="#339af0"/>
    
    <!-- 描边矩形 -->
    <rect x="230" y="10" width="60" height="80" 
          fill="none" stroke="#51cf66" stroke-width="3"/>
</svg>
```

#### 圆形和椭圆
```html
<svg width="400" height="200">
    <!-- 圆形 -->
    <circle cx="100" cy="100" r="80" fill="#ffd43b"/>
    
    <!-- 椭圆 -->
    <ellipse cx="250" cy="100" rx="100" ry="60" fill="#ff6b6b"/>
</svg>
```

#### 线条和多边形
```html
<svg width="400" height="300">
    <!-- 直线 -->
    <line x1="10" y1="10" x2="200" y2="100" 
          stroke="#339af0" stroke-width="2"/>
    
    <!-- 折线 -->
    <polyline points="10,150 50,100 90,130 130,90 170,110"
              fill="none" stroke="#ff6b6b" stroke-width="2"/>
    
    <!-- 多边形 -->
    <polygon points="250,50 300,150 200,150"
             fill="#51cf66" stroke="#2f9e44" stroke-width="2"/>
</svg>
```

#### 路径
```html
<svg width="400" height="300">
    <!-- 基本路径 -->
    <path d="M 10 10 L 100 10 L 100 100 Z" fill="#ff6b6b"/>
    
    <!-- 曲线路径 -->
    <path d="M 150 10 Q 200 50 150 100" 
          fill="none" stroke="#339af0" stroke-width="2"/>
    
    <!-- 贝塞尔曲线 -->
    <path d="M 250 10 C 250 50, 350 50, 350 100"
          fill="none" stroke="#51cf66" stroke-width="2"/>
    
    <!-- 圆弧 -->
    <path d="M 50 150 A 50 50 0 0 1 150 150"
          fill="none" stroke="#ffd43b" stroke-width="2"/>
</svg>
```

**路径命令**：
- M/m: 移动到 (moveto)
- L/l: 直线到 (lineto)
- H/h: 水平线 (horizontal)
- V/v: 垂直线 (vertical)
- C/c: 三次贝塞尔曲线
- Q/q: 二次贝塞尔曲线
- A/a: 圆弧
- Z/z: 闭合路径

### SVG样式

#### 填充和描边
```html
<svg width="400" height="200">
    <!-- 填充 -->
    <circle cx="100" cy="100" r="50" fill="#ff6b6b"/>
    
    <!-- 描边 -->
    <circle cx="250" cy="100" r="50" 
            fill="none" 
            stroke="#339af0" 
            stroke-width="5"
            stroke-dasharray="5,5"
            stroke-linecap="round"/>
</svg>
```

#### 渐变
```html
<svg width="400" height="200">
    <defs>
        <!-- 线性渐变 -->
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1"/>
            <stop offset="100%" style="stop-color:#339af0;stop-opacity:1"/>
        </linearGradient>
        
        <!-- 径向渐变 -->
        <radialGradient id="grad2">
            <stop offset="0%" style="stop-color:#fff;stop-opacity:1"/>
            <stop offset="100%" style="stop-color:#ff6b6b;stop-opacity:1"/>
        </radialGradient>
    </defs>
    
    <rect x="10" y="10" width="180" height="180" fill="url(#grad1)"/>
    <circle cx="300" cy="100" r="80" fill="url(#grad2)"/>
</svg>
```

#### 滤镜
```html
<svg width="400" height="200">
    <defs>
        <!-- 模糊滤镜 -->
        <filter id="blur">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5"/>
        </filter>
        
        <!-- 阴影 -->
        <filter id="shadow">
            <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.5"/>
        </filter>
    </defs>
    
    <rect x="10" y="10" width="100" height="100" 
          fill="#ff6b6b" filter="url(#blur)"/>
    
    <circle cx="250" cy="60" r="50" 
            fill="#339af0" filter="url(#shadow)"/>
</svg>
```

### SVG动画

#### CSS动画
```html
<svg width="200" height="200">
    <circle cx="100" cy="100" r="50" fill="#ff6b6b">
        <animate attributeName="r" 
                 from="50" to="80" 
                 dur="1s" 
                 repeatCount="indefinite"
                 direction="alternate"/>
    </circle>
</svg>

<style>
@keyframes pulse {
    0%, 100% { r: 50px; }
    50% { r: 80px; }
}

circle {
    animation: pulse 2s infinite;
}
</style>
```

#### SMIL动画
```html
<svg width="400" height="200">
    <!-- 移动动画 -->
    <circle cx="50" cy="100" r="20" fill="#ff6b6b">
        <animate attributeName="cx" 
                 from="50" to="350" 
                 dur="3s" 
                 repeatCount="indefinite"/>
    </circle>
    
    <!-- 路径动画 -->
    <path id="motionPath" 
          d="M 50 50 Q 200 150 350 50" 
          fill="none" stroke="#ddd"/>
    <circle r="10" fill="#339af0">
        <animateMotion dur="3s" repeatCount="indefinite">
            <mpath href="#motionPath"/>
        </animateMotion>
    </circle>
</svg>
```

## 🎯 实战案例

### Canvas图表示例
```javascript
// 柱状图
function drawBarChart(data) {
    const canvas = document.getElementById('chart');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    const maxValue = Math.max(...data.map(d => d.value));
    const barWidth = width / data.length - 20;
    const scale = (height - 40) / maxValue;
    
    ctx.clearRect(0, 0, width, height);
    
    data.forEach((item, index) => {
        const barHeight = item.value * scale;
        const x = index * (barWidth + 20) + 10;
        const y = height - barHeight - 20;
        
        // 绘制柱子
        ctx.fillStyle = '#339af0';
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // 绘制标签
        ctx.fillStyle = '#000';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(item.label, x + barWidth / 2, height - 5);
        
        // 绘制数值
        ctx.fillText(item.value, x + barWidth / 2, y - 5);
    });
}

// 使用
const chartData = [
    { label: '一月', value: 120 },
    { label: '二月', value: 80 },
    { label: '三月', value: 150 },
    { label: '四月', value: 100 }
];
drawBarChart(chartData);
```

### SVG交互图标
```html
<svg width="200" height="200" id="interactive-icon">
    <defs>
        <style>
            .icon-part {
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .icon-part:hover {
                fill: #ff6b6b;
                transform: scale(1.1);
            }
        </style>
    </defs>
    
    <g class="icon-part">
        <circle cx="100" cy="100" r="40" fill="#339af0"/>
        <path d="M 80 100 L 120 100 M 100 80 L 100 120" 
              stroke="#fff" stroke-width="4"/>
    </g>
</svg>

<script>
document.getElementById('interactive-icon').addEventListener('click', () => {
    alert('图标被点击！');
});
</script>
```

## ⚖️ Canvas vs SVG对比

### Canvas优势
- 像素级操作
- 高性能动画
- 适合大量对象
- 游戏开发
- 图像处理

### SVG优势
- 矢量图形，无损缩放
- 可通过CSS和JavaScript操作
- 可访问性更好
- 文件体积小
- 适合图表和图标

### 选择建议
```
Canvas适用于：
- 实时游戏渲染
- 复杂动画效果
- 像素级图像处理
- 大量对象（>1000）

SVG适用于：
- 图标和Logo
- 数据可视化
- 需要交互的图形
- 响应式图形
```

## 📚 实践练习

### 练习1：Canvas时钟
实现一个实时时钟，包含：
- 表盘、刻度、指针
- 时分秒实时更新
- 平滑动画效果

### 练习2：SVG图表
创建一个SVG饼图，要求：
- 数据驱动
- 鼠标悬停提示
- 动画过渡效果

### 练习3：Canvas画板
实现一个简单的画板应用：
- 自由绘制
- 颜色选择
- 线条粗细
- 橡皮擦和清空

## 📚 参考资料
- [MDN Canvas教程](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API)
- [MDN SVG教程](https://developer.mozilla.org/zh-CN/docs/Web/SVG)
- [SVG规范](https://www.w3.org/TR/SVG2/)


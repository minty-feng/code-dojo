# 🎨 CSS 核心技术

CSS（Cascading Style Sheets）是控制网页外观的样式语言，掌握现代CSS技术是构建精美网页的关键。

## 🎯 学习目标

### 核心能力
- **选择器精通**：掌握各类选择器及其优先级规则
- **布局系统**：Flexbox、Grid、定位、浮动等布局技术
- **响应式设计**：媒体查询、移动优先、自适应布局
- **动画效果**：过渡、关键帧动画、transform变换
- **预处理器**：Sass/Less变量、嵌套、混合、函数

### 技术深度
- **CSS架构**：BEM、OOCSS、SMACSS命名方法论
- **性能优化**：选择器性能、重绘重排、CSS加载优化
- **现代特性**：CSS变量、Grid、容器查询、层叠层
- **工程化**：PostCSS、CSS Modules、CSS-in-JS

## 📚 学习路径

### 第一阶段：CSS基础
1. **选择器与优先级**：各类选择器、特异性计算、继承
2. **盒模型与定位**：标准盒模型、定位方式、层叠上下文
3. **文本与颜色**：字体、文本样式、颜色系统

### 第二阶段：布局技术
4. **Flexbox布局**：弹性盒子模型、主轴交叉轴、对齐方式
5. **Grid布局**：网格系统、区域划分、自动布局
6. **响应式设计**：媒体查询、断点设计、移动优先

### 第三阶段：高级特性
7. **动画与过渡**：transition、animation、transform
8. **预处理器**：Sass/Less语法、模块化、工程化
9. **现代CSS**：CSS变量、容器查询、新特性

## 🎨 技术要点

### 选择器性能
```css
/* 高效选择器 */
.button { }
#header { }

/* 低效选择器（避免） */
* { }
div div div div { }
[type="text"] { }
```

### 布局最佳实践
```css
/* Flexbox - 一维布局 */
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Grid - 二维布局 */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}
```

### 响应式设计
```css
/* 移动优先 */
.element {
    width: 100%;
}

@media (min-width: 768px) {
    .element {
        width: 50%;
    }
}

@media (min-width: 1024px) {
    .element {
        width: 33.33%;
    }
}
```

## 💡 实践建议

### 代码规范
- 使用有意义的类名
- 保持选择器简洁
- 遵循命名规范（BEM等）
- 组织CSS结构（按功能模块）

### 性能优化
- 避免过度嵌套选择器
- 减少使用通配符和属性选择器
- 合理使用CSS变量
- 压缩和合并CSS文件

### 兼容性
- 使用Autoprefixer自动添加前缀
- 渐进增强而非优雅降级
- 测试主流浏览器
- 使用Can I Use查询兼容性

## 🔧 常用工具

### 预处理器
- **Sass/SCSS**：变量、嵌套、混合、继承
- **Less**：轻量级预处理器
- **Stylus**：简洁语法

### PostCSS插件
- **Autoprefixer**：自动添加浏览器前缀
- **cssnano**：压缩优化
- **postcss-preset-env**：使用未来CSS特性

### CSS框架
- **Tailwind CSS**：原子化CSS框架
- **Bootstrap**：组件化UI框架
- **Bulma**：纯CSS框架


# 03-语义化与可访问性

## 📋 学习目标
- 理解HTML5语义化标签的重要性
- 掌握ARIA属性的使用
- 学习Web可访问性最佳实践
- 提升SEO优化能力

## 🏷️ HTML5语义化标签

### 页面结构标签
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>语义化页面示例</title>
</head>
<body>
    <!-- 页眉 -->
    <header>
        <h1>网站名称</h1>
        <nav>
            <ul>
                <li><a href="/">首页</a></li>
                <li><a href="/about">关于</a></li>
                <li><a href="/contact">联系</a></li>
            </ul>
        </nav>
    </header>
    
    <!-- 主要内容 -->
    <main>
        <!-- 文章 -->
        <article>
            <header>
                <h2>文章标题</h2>
                <p>
                    <time datetime="2025-10-21">2025年10月21日</time>
                    作者：<span>张三</span>
                </p>
            </header>
            
            <section>
                <h3>章节标题</h3>
                <p>章节内容...</p>
            </section>
            
            <footer>
                <p>标签：<a href="/tag/html">HTML</a></p>
            </footer>
        </article>
        
        <!-- 侧边栏 -->
        <aside>
            <section>
                <h3>相关文章</h3>
                <ul>
                    <li><a href="#">文章1</a></li>
                    <li><a href="#">文章2</a></li>
                </ul>
            </section>
        </aside>
    </main>
    
    <!-- 页脚 -->
    <footer>
        <p>&copy; 2025 网站名称. All rights reserved.</p>
    </footer>
</body>
</html>
```

### 语义化标签详解

#### header - 页眉
```html
<!-- 页面级header -->
<header>
    <h1>网站标题</h1>
    <nav>导航菜单</nav>
</header>

<!-- 文章级header -->
<article>
    <header>
        <h2>文章标题</h2>
        <p>发布时间和作者信息</p>
    </header>
</article>

<!-- section级header -->
<section>
    <header>
        <h3>章节标题</h3>
    </header>
</section>
```

#### nav - 导航
```html
<!-- 主导航 -->
<nav aria-label="主导航">
    <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/products">产品</a></li>
        <li><a href="/about">关于</a></li>
    </ul>
</nav>

<!-- 面包屑导航 -->
<nav aria-label="面包屑">
    <ol>
        <li><a href="/">首页</a></li>
        <li><a href="/category">分类</a></li>
        <li aria-current="page">当前页</li>
    </ol>
</nav>

<!-- 目录导航 -->
<nav aria-label="目录">
    <h2>文章目录</h2>
    <ul>
        <li><a href="#section1">第一节</a></li>
        <li><a href="#section2">第二节</a></li>
    </ul>
</nav>
```

#### main - 主要内容
```html
<!-- 每个页面只能有一个main标签 -->
<main>
    <h1>页面主要内容</h1>
    <p>这是页面的核心内容区域</p>
</main>

<!-- 错误：多个main -->
<!-- <main>内容1</main> -->
<!-- <main>内容2</main> -->
```

#### article - 独立文章
```html
<!-- 博客文章 -->
<article>
    <header>
        <h2>文章标题</h2>
        <p>
            <time datetime="2025-10-21T14:30:00">2025年10月21日 14:30</time>
            作者：<a href="/author/zhangsan">张三</a>
        </p>
    </header>
    
    <p>文章正文内容...</p>
    
    <footer>
        <p>分类：<a href="/category/tech">技术</a></p>
        <p>标签：
            <a href="/tag/html">HTML</a>
            <a href="/tag/css">CSS</a>
        </p>
    </footer>
</article>

<!-- 用户评论 -->
<article class="comment">
    <header>
        <h4>用户名</h4>
        <time datetime="2025-10-21">2025年10月21日</time>
    </header>
    <p>评论内容...</p>
</article>
```

#### section - 章节
```html
<article>
    <h1>完整教程</h1>
    
    <section>
        <h2>第一章：基础知识</h2>
        <p>基础内容...</p>
    </section>
    
    <section>
        <h2>第二章：进阶技巧</h2>
        <p>进阶内容...</p>
    </section>
</article>
```

#### aside - 侧边内容
```html
<!-- 侧边栏 -->
<aside>
    <section>
        <h3>热门文章</h3>
        <ul>
            <li><a href="#">文章1</a></li>
            <li><a href="#">文章2</a></li>
        </ul>
    </section>
    
    <section>
        <h3>标签云</h3>
        <a href="/tag/html">HTML</a>
        <a href="/tag/css">CSS</a>
    </section>
</aside>

<!-- 文章中的补充说明 -->
<article>
    <h2>主要内容</h2>
    <p>正文...</p>
    
    <aside>
        <h4>小贴士</h4>
        <p>这是一个相关的补充说明</p>
    </aside>
</article>
```

#### footer - 页脚
```html
<!-- 页面页脚 -->
<footer>
    <nav aria-label="页脚导航">
        <a href="/about">关于我们</a>
        <a href="/privacy">隐私政策</a>
        <a href="/terms">服务条款</a>
    </nav>
    <p>&copy; 2025 公司名称</p>
</footer>

<!-- 文章页脚 -->
<article>
    <h2>文章标题</h2>
    <p>文章内容...</p>
    <footer>
        <p>最后更新：<time datetime="2025-10-21">2025年10月21日</time></p>
    </footer>
</article>
```

### 其他语义化标签

#### figure和figcaption
```html
<!-- 图片及说明 -->
<figure>
    <img src="chart.png" alt="销售数据图表">
    <figcaption>图1：2025年第一季度销售数据</figcaption>
</figure>

<!-- 代码示例 -->
<figure>
    <pre><code>
function hello() {
    console.log('Hello World');
}
    </code></pre>
    <figcaption>示例1：Hello World函数</figcaption>
</figure>

<!-- 引用 -->
<figure>
    <blockquote>
        <p>生存还是毁灭，这是一个问题。</p>
    </blockquote>
    <figcaption>—— 莎士比亚，《哈姆雷特》</figcaption>
</figure>
```

#### details和summary
```html
<!-- 可折叠内容 -->
<details>
    <summary>点击查看详情</summary>
    <p>这是隐藏的详细内容</p>
    <ul>
        <li>列表项1</li>
        <li>列表项2</li>
    </ul>
</details>

<!-- 默认展开 -->
<details open>
    <summary>FAQ问题</summary>
    <p>答案内容...</p>
</details>

<!-- 嵌套使用 -->
<details>
    <summary>第一章</summary>
    <details>
        <summary>1.1 节</summary>
        <p>内容...</p>
    </details>
    <details>
        <summary>1.2 节</summary>
        <p>内容...</p>
    </details>
</details>
```

#### mark - 高亮
```html
<p>搜索结果中的<mark>关键词</mark>会被高亮显示</p>
```

#### time - 时间
```html
<!-- 日期 -->
<time datetime="2025-10-21">2025年10月21日</time>

<!-- 日期时间 -->
<time datetime="2025-10-21T14:30:00+08:00">
    2025年10月21日 14:30
</time>

<!-- 持续时间 -->
<time datetime="PT2H30M">2小时30分钟</time>
```

## ♿ Web可访问性（A11y）

### ARIA属性

#### role属性
```html
<!-- Landmark Roles -->
<div role="banner">页眉内容（等同于header）</div>
<div role="navigation">导航菜单（等同于nav）</div>
<div role="main">主要内容（等同于main）</div>
<div role="complementary">补充内容（等同于aside）</div>
<div role="contentinfo">页脚信息（等同于footer）</div>
<div role="search">搜索区域</div>

<!-- Widget Roles -->
<div role="button" tabindex="0">自定义按钮</div>
<div role="tab">标签页</div>
<div role="tabpanel">标签面板</div>
<div role="dialog">对话框</div>
<div role="alert">警告信息</div>
<div role="tooltip">工具提示</div>

<!-- Document Structure Roles -->
<div role="article">文章</div>
<div role="list">列表</div>
<div role="listitem">列表项</div>
```

**注意**：优先使用HTML5语义化标签，只有在必要时才使用role属性。

#### aria-label和aria-labelledby
```html
<!-- aria-label：直接提供标签文本 -->
<button aria-label="关闭对话框">
    <svg>...</svg> <!-- 图标 -->
</button>

<nav aria-label="主导航">
    <ul>...</ul>
</nav>

<!-- aria-labelledby：引用其他元素作为标签 -->
<h2 id="section-title">用户信息</h2>
<section aria-labelledby="section-title">
    <p>用户详细信息...</p>
</section>

<!-- 多个元素组合 -->
<div aria-labelledby="title description">
    <h3 id="title">商品名称</h3>
    <p id="description">商品描述</p>
</div>
```

#### aria-describedby
```html
<!-- 为元素提供描述 -->
<input type="email" 
       id="email"
       aria-describedby="email-hint">
<span id="email-hint">请输入有效的邮箱地址</span>

<!-- 表单验证 -->
<input type="password" 
       id="password"
       aria-describedby="password-requirement password-error"
       aria-invalid="true">
<span id="password-requirement">密码至少8位</span>
<span id="password-error" role="alert">密码过于简单</span>
```

#### aria-hidden
```html
<!-- 对屏幕阅读器隐藏装饰性内容 -->
<button>
    <span aria-hidden="true">🔍</span>
    搜索
</button>

<!-- 隐藏重复内容 -->
<a href="/article/123">
    <h3>文章标题</h3>
    <p>文章摘要...</p>
    <span aria-hidden="true">阅读更多 →</span>
</a>
```

#### aria-live
```html
<!-- 实时更新区域 -->
<div aria-live="polite" aria-atomic="true">
    <p>新消息：您有3条未读消息</p>
</div>

<!-- aria-live取值 -->
<!-- off: 默认，不通知 -->
<!-- polite: 礼貌通知（等待用户操作完成） -->
<!-- assertive: 立即通知（打断用户） -->

<!-- 加载状态 -->
<div aria-live="polite" aria-busy="true">
    <p>正在加载...</p>
</div>
```

#### aria-expanded
```html
<!-- 展开/折叠状态 -->
<button aria-expanded="false" aria-controls="menu">
    菜单
</button>
<ul id="menu" hidden>
    <li>选项1</li>
    <li>选项2</li>
</ul>

<script>
const button = document.querySelector('[aria-expanded]');
const menu = document.getElementById('menu');

button.addEventListener('click', () => {
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', !isExpanded);
    menu.hidden = isExpanded;
});
</script>
```

#### aria-selected和aria-current
```html
<!-- 标签页 -->
<div role="tablist">
    <button role="tab" aria-selected="true">标签1</button>
    <button role="tab" aria-selected="false">标签2</button>
    <button role="tab" aria-selected="false">标签3</button>
</div>

<!-- 当前页 -->
<nav>
    <a href="/">首页</a>
    <a href="/products">产品</a>
    <a href="/about" aria-current="page">关于</a>
</nav>

<!-- aria-current取值 -->
<!-- page: 当前页面 -->
<!-- step: 当前步骤 -->
<!-- location: 当前位置 -->
<!-- date: 当前日期 -->
<!-- time: 当前时间 -->
<!-- true: 当前项 -->
```

### 键盘可访问性

#### tabindex
```html
<!-- tabindex="0": 自然顺序 -->
<div tabindex="0" role="button">可聚焦的div</div>

<!-- tabindex="-1": 不在Tab顺序中，但可通过JavaScript聚焦 -->
<div tabindex="-1" id="modal-content">
    模态框内容
</div>

<!-- tabindex="1+": 指定顺序（不推荐，会破坏自然顺序） -->
<input tabindex="3">
<input tabindex="1">
<input tabindex="2">
```

#### 键盘事件处理
```html
<!-- 自定义按钮 -->
<div role="button" 
     tabindex="0"
     onclick="handleClick()"
     onkeydown="handleKeyDown(event)">
    点击我
</div>

<script>
function handleClick() {
    console.log('Clicked');
}

function handleKeyDown(event) {
    // Enter或Space键触发
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        handleClick();
    }
}
</script>

<!-- 可关闭的对话框 -->
<div role="dialog" 
     aria-modal="true"
     aria-labelledby="dialog-title"
     onkeydown="handleDialogKeyDown(event)">
    <h2 id="dialog-title">对话框标题</h2>
    <p>内容...</p>
    <button onclick="closeDialog()">关闭</button>
</div>

<script>
function handleDialogKeyDown(event) {
    if (event.key === 'Escape') {
        closeDialog();
    }
}
</script>
```

### 焦点管理
```javascript
// 焦点陷阱（模态框中）
const modal = document.getElementById('modal');
const focusableElements = modal.querySelectorAll(
    'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
);
const firstElement = focusableElements[0];
const lastElement = focusableElements[focusableElements.length - 1];

modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
});

// 打开模态框时设置焦点
function openModal() {
    modal.style.display = 'block';
    firstElement.focus();
}

// 关闭模态框时恢复焦点
let previousFocus;
function openModal() {
    previousFocus = document.activeElement;
    modal.style.display = 'block';
    firstElement.focus();
}

function closeModal() {
    modal.style.display = 'none';
    previousFocus.focus();
}
```

### 图片替代文本
```html
<!-- 内容性图片 -->
<img src="chart.png" alt="2025年Q1销售额同比增长25%">

<!-- 装饰性图片 -->
<img src="decoration.png" alt="">

<!-- 链接中的图片 -->
<a href="/home">
    <img src="logo.png" alt="公司名称 - 首页">
</a>

<!-- 复杂图表 -->
<figure>
    <img src="complex-chart.png" 
         alt="销售数据图表"
         aria-describedby="chart-description">
    <figcaption id="chart-description">
        该图表展示了2025年第一季度各产品线的销售数据。
        产品A销售额为100万，产品B为80万，产品C为60万。
    </figcaption>
</figure>

<!-- SVG图标 -->
<svg role="img" aria-labelledby="icon-title">
    <title id="icon-title">搜索</title>
    <path d="..."></path>
</svg>
```

## 🔍 SEO优化

### 结构化数据
```html
<!-- JSON-LD格式 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "HTML语义化详解",
  "author": {
    "@type": "Person",
    "name": "张三"
  },
  "datePublished": "2025-10-21",
  "image": "https://example.com/image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "技术博客",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
</script>

<!-- 面包屑 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "首页",
    "item": "https://example.com"
  },{
    "@type": "ListItem",
    "position": 2,
    "name": "技术文章",
    "item": "https://example.com/tech"
  },{
    "@type": "ListItem",
    "position": 3,
    "name": "HTML教程"
  }]
}
</script>
```

### 语义化HTML与SEO
```html
<!-- 良好的标题层级 -->
<h1>网站主标题</h1>
<article>
    <h2>文章标题</h2>
    <section>
        <h3>章节标题</h3>
        <h4>小节标题</h4>
    </section>
</article>

<!-- 使用strong和em -->
<p>这是<strong>重要内容</strong>，这是<em>强调内容</em>。</p>

<!-- 链接文本要有意义 -->
<!-- 不好 -->
<a href="/article">点击这里</a>

<!-- 好 -->
<a href="/article">阅读完整文章：HTML语义化详解</a>
```

## 🎯 完整示例

### 可访问的模态框
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>可访问的模态框示例</title>
    <style>
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
        }
        
        .modal-content {
            position: relative;
            margin: 10% auto;
            padding: 20px;
            background: white;
            width: 80%;
            max-width: 500px;
        }
        
        .modal.open {
            display: block;
        }
    </style>
</head>
<body>
    <button id="openModal">打开模态框</button>
    
    <div id="modal" 
         class="modal" 
         role="dialog" 
         aria-modal="true"
         aria-labelledby="modal-title"
         aria-describedby="modal-description">
        <div class="modal-content">
            <h2 id="modal-title">模态框标题</h2>
            <p id="modal-description">这是模态框的描述内容</p>
            
            <form>
                <label for="name">姓名：</label>
                <input type="text" id="name" required>
                
                <label for="email">邮箱：</label>
                <input type="email" id="email" required>
                
                <button type="submit">提交</button>
                <button type="button" id="closeModal">取消</button>
            </form>
        </div>
    </div>
    
    <script>
        const openBtn = document.getElementById('openModal');
        const closeBtn = document.getElementById('closeModal');
        const modal = document.getElementById('modal');
        let previousFocus;
        
        // 获取可聚焦元素
        const focusableElements = modal.querySelectorAll(
            'a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
        );
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];
        
        // 打开模态框
        function openModal() {
            previousFocus = document.activeElement;
            modal.classList.add('open');
            firstFocusable.focus();
            document.body.style.overflow = 'hidden';
        }
        
        // 关闭模态框
        function closeModal() {
            modal.classList.remove('open');
            document.body.style.overflow = '';
            previousFocus.focus();
        }
        
        // 焦点陷阱
        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeModal();
            }
            
            if (e.key === 'Tab') {
                if (e.shiftKey && document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        });
        
        openBtn.addEventListener('click', openModal);
        closeBtn.addEventListener('click', closeModal);
        
        // 点击背景关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    </script>
</body>
</html>
```

## 📚 实践练习

### 练习1：语义化博客页面
创建一个语义化的博客文章页面，包含：
- 正确的文档结构
- 面包屑导航
- 文章元信息（作者、时间、分类）
- 相关文章侧边栏
- 评论区

### 练习2：可访问的下拉菜单
实现一个完全可访问的下拉菜单，要求：
- 键盘可操作（Tab、Enter、Escape、方向键）
- 正确的ARIA属性
- 焦点管理
- 屏幕阅读器友好

### 练习3：SEO优化页面
创建一个SEO优化的产品页面，包含：
- 完整的meta标签
- 结构化数据（Product schema）
- 语义化HTML
- 图片优化

## 💡 最佳实践

### 1. 优先使用语义化标签
```html
<!-- 不推荐 -->
<div class="header">
    <div class="nav">...</div>
</div>

<!-- 推荐 -->
<header>
    <nav>...</nav>
</header>
```

### 2. 提供多种访问方式
- 键盘导航
- 屏幕阅读器支持
- 触摸操作
- 语音控制

### 3. 测试工具
- **axe DevTools**：自动化可访问性测试
- **WAVE**：网页可访问性评估工具
- **Lighthouse**：综合评分（包含可访问性）
- **NVDA/JAWS**：屏幕阅读器测试

## 📚 参考资料
- [WCAG 2.1指南](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA最佳实践](https://www.w3.org/WAI/ARIA/apg/)
- [MDN可访问性](https://developer.mozilla.org/zh-CN/docs/Web/Accessibility)
- [Schema.org结构化数据](https://schema.org/)


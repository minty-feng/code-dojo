# 01-基础标签与文档结构

## 📋 学习目标
- 理解HTML文档的基本结构
- 掌握常用HTML标签的使用
- 了解DOCTYPE和字符编码
- 学习页面元信息配置

## 🏗️ HTML文档结构

### 基本结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="页面描述">
    <meta name="keywords" content="关键词1,关键词2">
    <meta name="author" content="作者名">
    <title>页面标题</title>
    
    <!-- CSS样式 -->
    <link rel="stylesheet" href="styles.css">
    
    <!-- 图标 -->
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>
    <!-- 页面内容 -->
    <header>
        <h1>网站标题</h1>
        <nav>导航菜单</nav>
    </header>
    
    <main>
        <article>主要内容</article>
        <aside>侧边栏</aside>
    </main>
    
    <footer>页脚信息</footer>
    
    <!-- JavaScript脚本 -->
    <script src="script.js"></script>
</body>
</html>
```

### DOCTYPE声明
```html
<!-- HTML5文档类型声明（推荐） -->
<!DOCTYPE html>

<!-- HTML4.01严格模式 -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" 
"http://www.w3.org/TR/html4/strict.dtd">

<!-- XHTML 1.0严格模式 -->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
```

**要点**：
- HTML5的DOCTYPE声明最简洁
- DOCTYPE必须位于文档第一行
- 声明文档类型影响浏览器渲染模式

## 📝 Head区域元信息

### 字符编码
```html
<!-- UTF-8编码（推荐） -->
<meta charset="UTF-8">

<!-- 旧版本写法 -->
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
```

### 视口配置
```html
<!-- 响应式设计必备 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- 禁止用户缩放 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, 
maximum-scale=1.0, user-scalable=no">

<!-- 设置特定宽度 -->
<meta name="viewport" content="width=375, initial-scale=1.0">
```

### SEO相关meta标签
```html
<!-- 页面描述（搜索结果摘要） -->
<meta name="description" content="这是一个前端学习网站，提供HTML、CSS、JavaScript等技术教程">

<!-- 关键词 -->
<meta name="keywords" content="HTML,CSS,JavaScript,前端开发,Web开发">

<!-- 作者信息 -->
<meta name="author" content="张三">

<!-- robots控制 -->
<meta name="robots" content="index,follow">
<meta name="robots" content="noindex,nofollow">

<!-- 页面刷新和跳转 -->
<meta http-equiv="refresh" content="30">
<meta http-equiv="refresh" content="5;url=https://example.com">
```

### Open Graph协议（社交分享）
```html
<!-- 基本信息 -->
<meta property="og:title" content="页面标题">
<meta property="og:type" content="website">
<meta property="og:url" content="https://example.com">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:description" content="页面描述">

<!-- 更多信息 -->
<meta property="og:site_name" content="网站名称">
<meta property="og:locale" content="zh_CN">

<!-- Twitter卡片 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@username">
<meta name="twitter:creator" content="@username">
<meta name="twitter:title" content="页面标题">
<meta name="twitter:description" content="页面描述">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### 资源链接
```html
<!-- CSS样式表 -->
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="print.css" media="print">

<!-- 图标 -->
<link rel="icon" href="favicon.ico" type="image/x-icon">
<link rel="apple-touch-icon" href="apple-icon.png">

<!-- 预连接、预加载、预获取 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://example.com">
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="prefetch" href="next-page.html">

<!-- 规范URL -->
<link rel="canonical" href="https://example.com/page">

<!-- RSS订阅 -->
<link rel="alternate" type="application/rss+xml" title="RSS" href="rss.xml">
```

## 🏷️ 文本标签

### 标题标签
```html
<h1>一级标题（页面主标题，每页只应有一个）</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<h4>四级标题</h4>
<h5>五级标题</h5>
<h6>六级标题</h6>
```

**最佳实践**：
- 一个页面只使用一个h1标签
- 保持标题层级的逻辑性（不要跳级）
- 标题应描述内容，有助于SEO

### 段落和文本
```html
<!-- 段落 -->
<p>这是一个段落。</p>

<!-- 换行 -->
第一行<br>第二行

<!-- 水平线 -->
<hr>

<!-- 文本格式化 -->
<strong>重要文本（加粗）</strong>
<em>强调文本（斜体）</em>
<b>粗体文本（无语义）</b>
<i>斜体文本（无语义）</i>
<u>下划线文本</u>
<s>删除线文本</s>
<mark>高亮文本</mark>
<small>小号文本</small>
<sub>下标</sub>
<sup>上标</sup>

<!-- 代码相关 -->
<code>代码片段</code>
<pre>预格式化文本</pre>
<kbd>键盘输入</kbd>
<samp>程序输出</samp>
<var>变量</var>

<!-- 引用 -->
<q>行内引用</q>
<blockquote cite="https://example.com">
    块级引用内容
</blockquote>
<cite>引用来源</cite>

<!-- 缩写和定义 -->
<abbr title="HyperText Markup Language">HTML</abbr>
<dfn>定义术语</dfn>

<!-- 时间 -->
<time datetime="2025-10-21">2025年10月21日</time>
<time datetime="2025-10-21T14:30:00">下午2:30</time>
```

## 🔗 链接和导航

### 超链接
```html
<!-- 基本链接 -->
<a href="https://example.com">外部链接</a>
<a href="page.html">相对路径</a>
<a href="/absolute/path.html">绝对路径</a>

<!-- 新窗口打开 -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
    在新窗口打开
</a>

<!-- 锚点链接 -->
<a href="#section1">跳转到section1</a>
<div id="section1">目标位置</div>

<!-- 邮件和电话 -->
<a href="mailto:email@example.com">发送邮件</a>
<a href="mailto:email@example.com?subject=主题&body=内容">带主题的邮件</a>
<a href="tel:+86-138-0000-0000">拨打电话</a>
<a href="sms:+86-138-0000-0000">发送短信</a>

<!-- 下载链接 -->
<a href="file.pdf" download>下载PDF</a>
<a href="file.pdf" download="自定义文件名.pdf">下载并重命名</a>

<!-- 关系属性 -->
<a href="https://example.com" rel="nofollow">不传递权重</a>
<a href="https://example.com" rel="sponsored">赞助链接</a>
<a href="https://example.com" rel="ugc">用户生成内容</a>
```

## 📋 列表

### 无序列表
```html
<ul>
    <li>列表项1</li>
    <li>列表项2</li>
    <li>列表项3</li>
</ul>

<!-- 嵌套列表 -->
<ul>
    <li>一级列表
        <ul>
            <li>二级列表</li>
            <li>二级列表</li>
        </ul>
    </li>
</ul>
```

### 有序列表
```html
<ol>
    <li>第一步</li>
    <li>第二步</li>
    <li>第三步</li>
</ol>

<!-- 自定义起始编号 -->
<ol start="5">
    <li>从5开始</li>
    <li>6</li>
</ol>

<!-- 倒序 -->
<ol reversed>
    <li>3</li>
    <li>2</li>
    <li>1</li>
</ol>

<!-- 编号类型 -->
<ol type="A">
    <li>A</li>
    <li>B</li>
</ol>
<!-- type: 1(数字), A(大写字母), a(小写字母), I(大写罗马), i(小写罗马) -->
```

### 描述列表
```html
<dl>
    <dt>术语1</dt>
    <dd>术语1的描述</dd>
    
    <dt>术语2</dt>
    <dd>术语2的描述1</dd>
    <dd>术语2的描述2</dd>
</dl>
```

## 🖼️ 图片

### 基本用法
```html
<!-- 基本图片 -->
<img src="image.jpg" alt="图片描述">

<!-- 指定尺寸 -->
<img src="image.jpg" alt="图片描述" width="300" height="200">

<!-- 图片链接 -->
<a href="large-image.jpg">
    <img src="thumbnail.jpg" alt="缩略图">
</a>
```

### 响应式图片
```html
<!-- srcset：不同分辨率 -->
<img src="image.jpg" 
     srcset="image-1x.jpg 1x, image-2x.jpg 2x, image-3x.jpg 3x"
     alt="响应式图片">

<!-- srcset：不同尺寸 -->
<img src="image.jpg"
     srcset="small.jpg 300w, medium.jpg 600w, large.jpg 1200w"
     sizes="(max-width: 600px) 300px, (max-width: 1200px) 600px, 1200px"
     alt="响应式图片">

<!-- picture元素 -->
<picture>
    <source media="(min-width: 1200px)" srcset="large.jpg">
    <source media="(min-width: 600px)" srcset="medium.jpg">
    <img src="small.jpg" alt="图片描述">
</picture>

<!-- WebP格式回退 -->
<picture>
    <source srcset="image.webp" type="image/webp">
    <source srcset="image.jpg" type="image/jpeg">
    <img src="image.jpg" alt="图片描述">
</picture>
```

### 图片优化
```html
<!-- 懒加载 -->
<img src="image.jpg" alt="图片描述" loading="lazy">

<!-- 解码方式 -->
<img src="image.jpg" alt="图片描述" decoding="async">

<!-- 完整优化示例 -->
<img src="image.jpg" 
     srcset="image-300.jpg 300w, image-600.jpg 600w"
     sizes="(max-width: 600px) 300px, 600px"
     alt="图片描述"
     loading="lazy"
     decoding="async"
     width="600"
     height="400">
```

## 🎯 实践练习

### 练习1：创建个人简历页面
要求：
- 使用语义化标签构建页面结构
- 包含个人信息、教育背景、工作经历、技能
- 正确使用标题层级
- 添加完整的meta信息

### 练习2：制作文章页面
要求：
- 使用article和section组织内容
- 包含标题、发布时间、作者信息
- 使用合适的文本格式化标签
- 添加目录锚点链接

### 练习3：响应式图片展示
要求：
- 使用picture元素实现响应式图片
- 提供WebP格式和JPEG格式
- 实现图片懒加载
- 添加图片说明

## 📚 参考资料

- [MDN HTML文档](https://developer.mozilla.org/zh-CN/docs/Web/HTML)
- [W3C HTML规范](https://www.w3.org/TR/html/)
- [HTML5规范](https://html.spec.whatwg.org/)
- [Can I Use](https://caniuse.com/) - 浏览器兼容性查询

## ⚡ 小结

### 核心要点
1. HTML5使用简洁的`<!DOCTYPE html>`声明
2. 正确配置字符编码和视口
3. 使用语义化标签提升可访问性和SEO
4. 掌握meta标签优化社交分享和搜索引擎
5. 合理使用响应式图片技术

### 常见问题
Q: 为什么要使用语义化标签？
A: 语义化标签能提升代码可读性、SEO优化、可访问性，有助于搜索引擎和辅助技术理解页面结构。

Q: alt属性为什么重要？
A: alt属性为图片提供替代文本，在图片加载失败或使用屏幕阅读器时显示，对SEO和可访问性至关重要。

Q: target="_blank"需要配合rel="noopener noreferrer"吗？
A: 是的，这能防止新页面访问window.opener，避免安全风险和性能问题。


# 01-选择器与优先级

## 📋 学习目标
- 掌握所有CSS选择器类型
- 理解CSS优先级计算规则
- 学习选择器性能优化
- 掌握继承和层叠规则

## 🎯 基本选择器

### 通用选择器
```css
/* 选择所有元素 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* 性能影响：慎用 */
```

### 元素选择器
```css
/* 选择所有p元素 */
p {
    line-height: 1.6;
    color: #333;
}

h1 {
    font-size: 2em;
    margin-bottom: 0.5em;
}

/* 多个元素 */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Arial', sans-serif;
}
```

### 类选择器
```css
/* 选择class="button"的元素 */
.button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
}

/* 多个类 */
.button.primary {
    background-color: #ff6b6b;
}

/* 同时有两个类 */
.card.featured {
    border: 2px solid gold;
}
```

### ID选择器
```css
/* 选择id="header"的元素 */
#header {
    background-color: #fff;
    padding: 20px;
}

/* 注意：ID在页面中应该是唯一的 */
/* 避免过度使用ID选择器，优先级过高 */
```

## 🔗 组合选择器

### 后代选择器
```css
/* 选择article内的所有p元素 */
article p {
    color: #555;
}

/* 多层嵌套 */
.sidebar .widget ul li {
    list-style: none;
}

/* 性能考虑：避免过深嵌套 */
```

### 子选择器
```css
/* 只选择直接子元素 */
.menu > li {
    display: inline-block;
}

/* 与后代选择器对比 */
.menu li { }     /* 所有后代li */
.menu > li { }   /* 只有直接子li */
```

### 相邻兄弟选择器
```css
/* 选择h1后面紧邻的p元素 */
h1 + p {
    font-size: 1.2em;
    color: #666;
}

/* 示例 */
/* <h1>标题</h1>
   <p>这段会被选中</p>
   <p>这段不会被选中</p> */
```

### 通用兄弟选择器
```css
/* 选择h1后面所有的p元素 */
h1 ~ p {
    margin-top: 1em;
}

/* 示例 */
/* <h1>标题</h1>
   <p>会被选中</p>
   <div>...</div>
   <p>也会被选中</p> */
```

## 🎨 属性选择器

### 基本属性选择器
```css
/* 存在属性 */
[title] {
    cursor: help;
}

/* 精确匹配 */
[type="text"] {
    border: 1px solid #ddd;
}

input[type="submit"] {
    background-color: #007bff;
    color: white;
}

/* 多个属性 */
input[type="text"][required] {
    border-color: #ff6b6b;
}
```

### 模糊匹配
```css
/* 以...开始 */
a[href^="https"] {
    color: green;
}

a[href^="http://"] {
    color: blue;
}

/* 以...结束 */
a[href$=".pdf"] {
    background: url('pdf-icon.png') no-repeat;
    padding-left: 20px;
}

img[src$=".jpg"],
img[src$=".png"] {
    border: 1px solid #ddd;
}

/* 包含... */
a[href*="example"] {
    font-weight: bold;
}

[class*="col-"] {
    float: left;
}
```

### 其他匹配
```css
/* 以空格分隔的单词中包含 */
[class~="featured"] {
    background-color: yellow;
}

/* 以连字符分隔，以...开始 */
[lang|="en"] {
    font-family: Arial;
}
/* 匹配 lang="en" 或 lang="en-US" */
```

## 🎭 伪类选择器

### 链接和用户行为
```css
/* 未访问的链接 */
a:link {
    color: blue;
}

/* 已访问的链接 */
a:visited {
    color: purple;
}

/* 鼠标悬停 */
a:hover {
    color: red;
    text-decoration: underline;
}

/* 激活状态（点击瞬间） */
a:active {
    color: orange;
}

/* 获得焦点 */
input:focus {
    outline: 2px solid #007bff;
    border-color: #007bff;
}

/* 顺序很重要：LVHA（LoVe HAte） */
```

### 结构伪类
```css
/* 第一个子元素 */
li:first-child {
    font-weight: bold;
}

/* 最后一个子元素 */
li:last-child {
    border-bottom: none;
}

/* 第n个子元素 */
li:nth-child(2) {
    background-color: #f0f0f0;
}

/* 奇数行 */
tr:nth-child(odd) {
    background-color: #f9f9f9;
}

/* 偶数行 */
tr:nth-child(even) {
    background-color: #fff;
}

/* 公式：an + b */
li:nth-child(3n) {
    /* 每3个：3, 6, 9, ... */
}

li:nth-child(3n+1) {
    /* 3, 6, 9... 的下一个：1, 4, 7, ... */
}

/* 倒数第n个 */
li:nth-last-child(2) {
    color: red;
}

/* 唯一子元素 */
p:only-child {
    margin: 0;
}
```

### 类型伪类
```css
/* 同类型中的第一个 */
p:first-of-type {
    font-size: 1.2em;
}

/* 同类型中的最后一个 */
p:last-of-type {
    margin-bottom: 0;
}

/* 同类型中的第n个 */
p:nth-of-type(2) {
    color: blue;
}

/* 唯一的同类型元素 */
p:only-of-type {
    text-align: center;
}
```

### 表单伪类
```css
/* 启用状态 */
input:enabled {
    background-color: white;
}

/* 禁用状态 */
input:disabled {
    background-color: #f0f0f0;
    cursor: not-allowed;
}

/* 选中状态（单选框、复选框） */
input:checked + label {
    font-weight: bold;
}

/* 必填字段 */
input:required {
    border-left: 3px solid #ff6b6b;
}

/* 可选字段 */
input:optional {
    border-left: 3px solid #ddd;
}

/* 有效输入 */
input:valid {
    border-color: #51cf66;
}

/* 无效输入 */
input:invalid {
    border-color: #ff6b6b;
}

/* 范围内 */
input:in-range {
    border-color: green;
}

/* 超出范围 */
input:out-of-range {
    border-color: red;
}

/* 只读 */
input:read-only {
    background-color: #f5f5f5;
}

/* 可读写 */
input:read-write {
    background-color: white;
}
```

### 其他伪类
```css
/* 空元素 */
p:empty {
    display: none;
}

/* 非... */
li:not(.active) {
    opacity: 0.5;
}

/* 目标元素（URL锚点） */
:target {
    background-color: yellow;
    animation: highlight 2s;
}

/* 根元素 */
:root {
    --main-color: #007bff;
    --spacing: 16px;
}
```

## 👻 伪元素选择器

### ::before和::after
```css
/* 在元素前插入内容 */
.quote::before {
    content: '"';
    font-size: 2em;
    color: #ddd;
}

.quote::after {
    content: '"';
    font-size: 2em;
    color: #ddd;
}

/* 装饰性图标 */
.external-link::after {
    content: ' ↗';
    font-size: 0.8em;
}

/* 清除浮动 */
.clearfix::after {
    content: '';
    display: table;
    clear: both;
}

/* 创建几何图形 */
.triangle::before {
    content: '';
    display: inline-block;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 10px solid #000;
}
```

### 其他伪元素
```css
/* 首字母 */
p::first-letter {
    font-size: 2em;
    font-weight: bold;
    float: left;
    line-height: 1;
    margin-right: 5px;
}

/* 首行 */
p::first-line {
    font-weight: bold;
    color: #333;
}

/* 选中文本 */
::selection {
    background-color: #ff6b6b;
    color: white;
}

/* 占位符文本 */
input::placeholder {
    color: #999;
    font-style: italic;
}
```

## 📊 优先级（特异性）

### 优先级计算

优先级由四个部分组成：(a, b, c, d)

- **a**: 内联样式（style属性）
- **b**: ID选择器的数量
- **c**: 类、属性、伪类选择器的数量
- **d**: 元素、伪元素选择器的数量

```css
/* 优先级示例 */
* { }                      /* (0, 0, 0, 0) */
li { }                     /* (0, 0, 0, 1) */
ul li { }                  /* (0, 0, 0, 2) */
.list { }                  /* (0, 0, 1, 0) */
.list li { }               /* (0, 0, 1, 1) */
.list .item { }            /* (0, 0, 2, 0) */
#header { }                /* (0, 1, 0, 0) */
#header .nav { }           /* (0, 1, 1, 0) */
#header .nav li { }        /* (0, 1, 1, 1) */
style="color: red"         /* (1, 0, 0, 0) */

/* !important */
.button {
    color: blue !important;  /* 最高优先级 */
}
```

### 优先级规则
```css
/* 规则1：特异性高的优先 */
p { color: black; }           /* (0,0,0,1) */
.text { color: blue; }        /* (0,0,1,0) - 优先 */

/* 规则2：特异性相同，后面的优先 */
.button { color: red; }
.button { color: blue; }      /* 优先 */

/* 规则3：!important最高 */
.text { color: green !important; }

/* 规则4：内联样式高于外部样式 */
<div class="text" style="color: purple;"> /* 内联优先 */

/* 规则5：继承的优先级最低 */
body { color: gray; }
p { } /* 即使为空，也比继承优先级高 */
```

### 最佳实践
```css
/* ❌ 避免过度使用!important */
.button {
    color: red !important;
}

/* ✅ 提高选择器特异性 */
.header .button {
    color: red;
}

/* ❌ 避免过深嵌套 */
.nav ul li a span { }

/* ✅ 使用类选择器 */
.nav-link-text { }

/* ❌ 避免ID选择器样式 */
#sidebar { }

/* ✅ 使用类选择器 */
.sidebar { }
```

## 🔄 继承

### 可继承属性
```css
/* 文本相关（大部分可继承） */
body {
    color: #333;           /* 继承 */
    font-family: Arial;    /* 继承 */
    font-size: 16px;       /* 继承 */
    line-height: 1.6;      /* 继承 */
    text-align: left;      /* 继承 */
}

/* 列表相关 */
ul {
    list-style-type: none; /* 继承 */
}

/* 表格相关 */
table {
    border-collapse: collapse; /* 继承 */
}
```

### 不可继承属性
```css
/* 盒模型 */
div {
    width: 100px;          /* 不继承 */
    height: 100px;         /* 不继承 */
    margin: 10px;          /* 不继承 */
    padding: 10px;         /* 不继承 */
    border: 1px solid;     /* 不继承 */
}

/* 定位 */
.element {
    position: absolute;    /* 不继承 */
    top: 0;                /* 不继承 */
    left: 0;               /* 不继承 */
}

/* 背景 */
.box {
    background-color: red; /* 不继承 */
}
```

### 控制继承
```css
/* inherit：强制继承 */
.child {
    border: inherit;
}

/* initial：重置为初始值 */
.element {
    color: initial;
}

/* unset：可继承则继承，否则initial */
.element {
    color: unset;
}

/* revert：恢复到浏览器默认样式 */
.element {
    all: revert;
}
```

## 🎯 选择器性能

### 性能排序（快→慢）
```css
/* 1. ID选择器（最快） */
#header { }

/* 2. 类选择器 */
.button { }

/* 3. 元素选择器 */
div { }

/* 4. 相邻兄弟选择器 */
h1 + p { }

/* 5. 子选择器 */
ul > li { }

/* 6. 后代选择器 */
ul li { }

/* 7. 通配符选择器 */
* { }

/* 8. 属性选择器（最慢） */
[type="text"] { }
```

### 优化建议
```css
/* ❌ 避免 */
* { }
div div div div { }
[type="text"] { }

/* ✅ 推荐 */
.specific-class { }
#unique-id { }

/* ❌ 过度限定 */
ul li.item { }
div.container { }

/* ✅ 简洁选择器 */
.item { }
.container { }

/* ❌ 链式选择器过长 */
.header .nav .menu .item .link { }

/* ✅ 使用更具体的类名 */
.nav-link { }
```

## 📚 实践练习

### 练习1：选择器练习
为以下HTML编写CSS：
- 第一个段落字体加粗
- 偶数行表格背景色
- 外部链接添加图标
- 必填输入框左边框红色

### 练习2：优先级计算
计算以下选择器的优先级：
- `#nav .menu li a`
- `.container div.box`
- `ul > li:first-child`
- `[type="text"]:focus`

### 练习3：伪类应用
实现以下效果：
- 鼠标悬停改变颜色
- 奇偶行不同背景
- 选中复选框后标签加粗
- 表单验证视觉反馈

## 📚 参考资料
- [MDN CSS选择器](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Selectors)
- [CSS选择器规范](https://www.w3.org/TR/selectors/)
- [特异性计算器](https://specificity.keegan.st/)


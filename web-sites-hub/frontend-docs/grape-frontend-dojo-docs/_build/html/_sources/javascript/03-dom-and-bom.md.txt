# 03-DOM与BOM操作

## 📋 学习目标
- 掌握DOM操作核心API
- 学习事件处理机制
- 理解BOM浏览器对象
- 掌握性能优化技巧

## 🌳 DOM操作

### 元素选择
```javascript
// getElementById
const element = document.getElementById('myId');

// querySelector（推荐）
const element = document.querySelector('.class');
const element = document.querySelector('#id');
const element = document.querySelector('[data-id="123"]');

// querySelectorAll
const elements = document.querySelectorAll('.items');
// 返回NodeList，可以forEach
elements.forEach(el => console.log(el));

// 转换为数组
const array = Array.from(elements);
const array = [...elements];

// 其他选择器（不推荐）
document.getElementsByClassName('class');
document.getElementsByTagName('div');
document.getElementsByName('name');
```

### 元素创建与插入
```javascript
// 创建元素
const div = document.createElement('div');
div.className = 'container';
div.id = 'main';
div.textContent = 'Hello';

// 设置HTML
div.innerHTML = '<span>Content</span>';

// 设置属性
div.setAttribute('data-id', '123');
div.dataset.id = '123';  // 推荐

// 插入元素
document.body.appendChild(div);
document.body.append(div, 'text', anotherElement);

// 在前面插入
parent.insertBefore(newNode, referenceNode);
parent.prepend(newNode);

// 在后面插入
parent.after(newNode);

// 替换
parent.replaceChild(newNode, oldNode);

// 移除
element.remove();
parent.removeChild(child);

// 克隆
const clone = element.cloneNode(true);  // true表示深拷贝
```

### 元素属性操作
```javascript
// 类名操作
element.classList.add('active');
element.classList.remove('active');
element.classList.toggle('active');
element.classList.contains('active');
element.classList.replace('old', 'new');

// 样式操作
element.style.color = 'red';
element.style.backgroundColor = 'blue';
element.style.cssText = 'color: red; font-size: 16px;';

// 获取计算样式
const styles = window.getComputedStyle(element);
const color = styles.getPropertyValue('color');

// 属性操作
element.getAttribute('data-id');
element.setAttribute('data-id', '123');
element.removeAttribute('data-id');
element.hasAttribute('data-id');

// dataset（推荐）
element.dataset.userId = '123';  // <div data-user-id="123">
const userId = element.dataset.userId;
```

### DOM遍历
```javascript
// 父元素
element.parentElement;
element.parentNode;

// 子元素
element.children;  // HTMLCollection
element.childNodes;  // NodeList（包含文本节点）
element.firstElementChild;
element.lastElementChild;

// 兄弟元素
element.nextElementSibling;
element.previousElementSibling;

// 最近的匹配元素
element.closest('.container');

// 检查包含关系
parent.contains(child);

// 遍历所有子元素
for (const child of element.children) {
    console.log(child);
}
```

## 📅 事件处理

### 事件监听
```javascript
// 添加事件监听
element.addEventListener('click', function(e) {
    console.log('Clicked!', e);
});

// 箭头函数（注意this指向）
element.addEventListener('click', (e) => {
    console.log(e.target);
});

// 移除事件监听
function handleClick(e) {
    console.log('Clicked');
}
element.addEventListener('click', handleClick);
element.removeEventListener('click', handleClick);

// 只执行一次
element.addEventListener('click', handleClick, {once: true});

// 捕获阶段
element.addEventListener('click', handleClick, {capture: true});

// 阻止默认行为
element.addEventListener('click', (e) => {
    e.preventDefault();
});

// 阻止冒泡
element.addEventListener('click', (e) => {
    e.stopPropagation();
});
```

### 事件委托
```javascript
// ❌ 为每个元素添加监听
document.querySelectorAll('.item').forEach(item => {
    item.addEventListener('click', handleClick);
});

// ✅ 事件委托（推荐）
document.querySelector('.list').addEventListener('click', (e) => {
    if (e.target.matches('.item')) {
        handleItemClick(e.target);
    }
});

// 实际应用
const list = document.querySelector('.todo-list');

list.addEventListener('click', (e) => {
    const target = e.target;
    
    if (target.matches('.delete-btn')) {
        const item = target.closest('.todo-item');
        item.remove();
    }
    
    if (target.matches('.toggle-btn')) {
        const item = target.closest('.todo-item');
        item.classList.toggle('completed');
    }
});
```

### 常用事件
```javascript
// 鼠标事件
element.addEventListener('click', handler);
element.addEventListener('dblclick', handler);
element.addEventListener('mousedown', handler);
element.addEventListener('mouseup', handler);
element.addEventListener('mousemove', handler);
element.addEventListener('mouseenter', handler);
element.addEventListener('mouseleave', handler);
element.addEventListener('mouseover', handler);
element.addEventListener('mouseout', handler);

// 键盘事件
element.addEventListener('keydown', (e) => {
    console.log(e.key, e.code, e.keyCode);
    if (e.key === 'Enter') {
        // 处理回车
    }
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        // Ctrl+S保存
    }
});

element.addEventListener('keyup', handler);
element.addEventListener('keypress', handler);  // 已废弃

// 表单事件
input.addEventListener('input', (e) => {
    console.log(e.target.value);
});
input.addEventListener('change', handler);
input.addEventListener('focus', handler);
input.addEventListener('blur', handler);
form.addEventListener('submit', (e) => {
    e.preventDefault();
    // 处理提交
});

// 窗口事件
window.addEventListener('load', handler);  // 页面完全加载
window.addEventListener('DOMContentLoaded', handler);  // DOM加载完成
window.addEventListener('beforeunload', (e) => {
    e.returnValue = '';  // 离开页面提示
});
window.addEventListener('resize', handler);
window.addEventListener('scroll', handler);
```

### 自定义事件
```javascript
// 创建自定义事件
const event = new CustomEvent('myEvent', {
    detail: {
        message: 'Hello',
        value: 123
    },
    bubbles: true,
    cancelable: true
});

// 监听自定义事件
element.addEventListener('myEvent', (e) => {
    console.log(e.detail.message);
});

// 触发事件
element.dispatchEvent(event);

// 实际应用：组件通信
class Component {
    constructor(element) {
        this.element = element;
    }
    
    emit(eventName, data) {
        const event = new CustomEvent(eventName, {
            detail: data,
            bubbles: true
        });
        this.element.dispatchEvent(event);
    }
    
    on(eventName, handler) {
        this.element.addEventListener(eventName, handler);
    }
}

const comp = new Component(document.querySelector('.component'));
comp.on('update', (e) => {
    console.log('Updated:', e.detail);
});
comp.emit('update', {value: 'new value'});
```

## 🌐 BOM操作

### window对象
```javascript
// 窗口尺寸
window.innerWidth;   // 视口宽度
window.innerHeight;  // 视口高度
window.outerWidth;   // 浏览器窗口宽度
window.outerHeight;  // 浏览器窗口高度

// 滚动
window.scrollX;  // 水平滚动距离
window.scrollY;  // 垂直滚动距离

window.scrollTo(0, 100);  // 滚动到指定位置
window.scrollTo({
    top: 100,
    behavior: 'smooth'  // 平滑滚动
});

window.scrollBy(0, 100);  // 相对滚动

// 打开新窗口
const newWindow = window.open(
    'https://example.com',
    '_blank',
    'width=800,height=600'
);

// 关闭窗口
newWindow.close();

// 对话框
window.alert('提示信息');
const result = window.confirm('确认吗？');
const input = window.prompt('请输入：', '默认值');
```

### location对象
```javascript
// URL信息
location.href;      // 完整URL
location.protocol;  // 协议（http:）
location.host;      // 主机名和端口
location.hostname;  // 主机名
location.port;      // 端口
location.pathname;  // 路径
location.search;    // 查询字符串（?key=value）
location.hash;      // 锚点（#section）

// 导航
location.href = 'https://example.com';  // 跳转
location.assign('https://example.com'); // 跳转
location.replace('https://example.com'); // 替换（不产生历史记录）
location.reload();  // 刷新
location.reload(true);  // 强制从服务器刷新

// URLSearchParams
const params = new URLSearchParams(location.search);
params.get('id');  // 获取参数
params.set('page', '2');  // 设置参数
params.delete('old');  // 删除参数
params.toString();  // 转为字符串

// 实际应用
function getQueryParams() {
    const params = new URLSearchParams(location.search);
    const result = {};
    for (const [key, value] of params) {
        result[key] = value;
    }
    return result;
}
```

### history对象
```javascript
// 导航
history.back();     // 后退
history.forward();  // 前进
history.go(-2);     // 后退2页
history.go(1);      // 前进1页

// HTML5 History API
history.pushState({page: 1}, 'title', '/page1');
history.replaceState({page: 2}, 'title', '/page2');

// 监听历史变化
window.addEventListener('popstate', (e) => {
    console.log('State:', e.state);
});

// 实际应用：单页应用路由
class Router {
    constructor() {
        this.routes = {};
        window.addEventListener('popstate', () => {
            this.handleRoute();
        });
    }
    
    route(path, handler) {
        this.routes[path] = handler;
    }
    
    navigate(path) {
        history.pushState({}, '', path);
        this.handleRoute();
    }
    
    handleRoute() {
        const path = location.pathname;
        const handler = this.routes[path];
        if (handler) handler();
    }
}
```

### navigator对象
```javascript
// 浏览器信息
navigator.userAgent;
navigator.language;
navigator.languages;
navigator.onLine;  // 是否在线
navigator.cookieEnabled;

// 地理位置
navigator.geolocation.getCurrentPosition(
    (position) => {
        console.log(position.coords.latitude, position.coords.longitude);
    },
    (error) => {
        console.error(error);
    }
);

// 剪贴板
navigator.clipboard.writeText('复制的文本');
navigator.clipboard.readText().then(text => console.log(text));

// 分享
navigator.share({
    title: '分享标题',
    text: '分享内容',
    url: 'https://example.com'
});
```

### screen对象
```javascript
screen.width;   // 屏幕宽度
screen.height;  // 屏幕高度
screen.availWidth;   // 可用宽度
screen.availHeight;  // 可用高度
screen.colorDepth;   // 颜色深度
screen.pixelDepth;   // 像素深度
```

## ⚡ 性能优化

### 防抖和节流
```javascript
// 防抖
function debounce(fn, delay) {
    let timer = null;
    return function(...args) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
            fn.apply(this, args);
        }, delay);
    };
}

// 使用
const handleInput = debounce((e) => {
    console.log('Search:', e.target.value);
}, 500);

input.addEventListener('input', handleInput);

// 节流
function throttle(fn, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            lastCall = now;
            fn.apply(this, args);
        }
    };
}

// 使用
const handleScroll = throttle(() => {
    console.log('Scrolled');
}, 200);

window.addEventListener('scroll', handleScroll);
```

### DocumentFragment
```javascript
// ❌ 多次操作DOM
for (let i = 0; i < 1000; i++) {
    const li = document.createElement('li');
    li.textContent = `Item ${i}`;
    ul.appendChild(li);  // 触发1000次重排
}

// ✅ 使用DocumentFragment
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
    const li = document.createElement('li');
    li.textContent = `Item ${i}`;
    fragment.appendChild(li);
}
ul.appendChild(fragment);  // 只触发1次重排
```

### IntersectionObserver
```javascript
// 懒加载图片
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
});

document.querySelectorAll('img[data-src]').forEach(img => {
    observer.observe(img);
});

// 无限滚动
const sentinel = document.querySelector('.sentinel');
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        loadMore();
    }
});
observer.observe(sentinel);
```

## 📚 实践练习

### 练习1：Todo列表
实现功能：
- 添加、删除Todo
- 标记完成
- 过滤显示
- 本地存储

### 练习2：图片懒加载
实现：
- IntersectionObserver
- 占位图
- 加载动画

### 练习3：无限滚动
实现：
- 滚动加载
- 加载状态
- 错误处理

## 📚 参考资料
- [MDN DOM文档](https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model)
- [DOM Standard](https://dom.spec.whatwg.org/)
- [JavaScript.info DOM](https://javascript.info/document)


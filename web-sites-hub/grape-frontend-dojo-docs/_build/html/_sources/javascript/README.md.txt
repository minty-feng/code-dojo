# 📜 JavaScript 核心技术

JavaScript是前端开发的核心语言，掌握现代JavaScript（ES6+）特性是成为优秀前端工程师的必经之路。

## 🎯 学习目标

### 核心能力
- **语法基础**：变量、数据类型、运算符、控制流
- **函数编程**：函数声明、箭头函数、闭包、高阶函数
- **面向对象**：原型链、类、继承、封装
- **异步编程**：Promise、async/await、事件循环
- **模块化**：ES6模块、CommonJS、模块打包

### 技术深度
- **ES6+特性**：解构、展开、模板字符串、Symbol等
- **DOM操作**：选择器、事件处理、节点操作
- **异步模式**：回调、Promise、Generator、Async/Await
- **设计模式**：单例、工厂、观察者、发布订阅

## 📚 学习路径

### 第一阶段：JavaScript基础
1. **基础语法**：变量、数据类型、运算符、控制结构
2. **函数与作用域**：函数定义、作用域链、闭包
3. **对象与数组**：对象操作、数组方法、解构赋值

### 第二阶段：进阶特性
4. **ES6+新特性**：let/const、箭头函数、Promise、Class
5. **异步编程**：回调、Promise、async/await
6. **DOM与BOM**：DOM操作、事件处理、浏览器API

### 第三阶段：高级应用
7. **模块化开发**：ES6模块、动态导入、模块打包
8. **函数式编程**：纯函数、不可变性、柯里化
9. **设计模式**：常用设计模式在JavaScript中的应用

## 🎨 技术要点

### 现代语法
```javascript
// ES6+ 特性
const [a, b] = [1, 2];
const {name, age} = person;
const arr = [...arr1, ...arr2];
const str = `Hello ${name}`;

// 箭头函数
const add = (a, b) => a + b;

// 解构与默认值
const greet = ({name = 'Guest'} = {}) => `Hello ${name}`;
```

### 异步处理
```javascript
// Promise
fetch('/api/data')
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));

// Async/Await
async function getData() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        return data;
    } catch (err) {
        console.error(err);
    }
}
```

### DOM操作
```javascript
// 现代选择器
const el = document.querySelector('.class');
const els = document.querySelectorAll('.items');

// 事件监听
el.addEventListener('click', (e) => {
    console.log('Clicked!', e.target);
});

// 修改DOM
el.classList.add('active');
el.textContent = 'New Text';
el.setAttribute('data-id', '123');
```

## 💡 实践建议

### 代码规范
- 使用const/let代替var
- 优先使用箭头函数
- 使用模板字符串
- 保持代码简洁和可读性

### 性能优化
- 避免不必要的DOM操作
- 使用事件委托
- 防抖和节流
- 合理使用闭包

### 最佳实践
- 编写纯函数
- 避免全局变量污染
- 使用严格模式
- 适当添加注释


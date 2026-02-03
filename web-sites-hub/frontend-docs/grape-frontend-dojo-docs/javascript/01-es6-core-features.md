# 01-ES6+核心特性

## 📋 学习目标
- 掌握let/const变量声明
- 理解解构赋值和展开运算符
- 学习箭头函数和模板字符串
- 掌握Promise和async/await

## 🔤 变量声明

### let和const
```javascript
// var的问题
console.log(x); // undefined (变量提升)
var x = 5;
var x = 10; // 可重复声明

if (true) {
    var y = 20;
}
console.log(y); // 20 (无块级作用域)

// let：块级作用域，不可重复声明
let a = 1;
// let a = 2; // 报错

if (true) {
    let b = 2;
}
// console.log(b); // 报错

// const：常量，不可重新赋值
const PI = 3.14159;
// PI = 3.14; // 报错

// 对象属性可以修改
const obj = {name: 'John'};
obj.name = 'Jane'; // 可以
// obj = {}; // 报错

// 数组元素可以修改
const arr = [1, 2, 3];
arr.push(4); // 可以
// arr = []; // 报错
```

### 暂时性死区
```javascript
console.log(x); // ReferenceError
let x = 5;

// typeof也不安全
typeof y; // ReferenceError
let y;
```

### 最佳实践
```javascript
// 默认使用const
const MAX_COUNT = 100;
const userList = [];

// 需要重新赋值时使用let
let count = 0;
count++;

// 不再使用var
```

## 🎯 解构赋值

### 数组解构
```javascript
// 基本用法
const [a, b, c] = [1, 2, 3];
console.log(a, b, c); // 1 2 3

// 跳过元素
const [first, , third] = [1, 2, 3];
console.log(first, third); // 1 3

// 默认值
const [x = 1, y = 2] = [10];
console.log(x, y); // 10 2

// 剩余运算符
const [head, ...tail] = [1, 2, 3, 4];
console.log(head); // 1
console.log(tail); // [2, 3, 4]

// 交换变量
let m = 1, n = 2;
[m, n] = [n, m];
console.log(m, n); // 2 1

// 函数返回多个值
function getCoordinates() {
    return [10, 20];
}
const [x, y] = getCoordinates();
```

### 对象解构
```javascript
// 基本用法
const {name, age} = {name: 'John', age: 30};
console.log(name, age); // John 30

// 重命名
const {name: userName, age: userAge} = person;
console.log(userName, userAge);

// 默认值
const {city = 'Beijing'} = {};
console.log(city); // Beijing

// 嵌套解构
const user = {
    name: 'John',
    address: {
        city: 'Beijing',
        street: '123 Main St'
    }
};
const {address: {city, street}} = user;

// 剩余属性
const {a, b, ...rest} = {a: 1, b: 2, c: 3, d: 4};
console.log(rest); // {c: 3, d: 4}

// 函数参数解构
function greet({name, age = 18}) {
    console.log(`Hello ${name}, you are ${age}`);
}
greet({name: 'John'}); // Hello John, you are 18

// 实际应用：配置对象
function createServer({
    port = 3000,
    host = 'localhost',
    protocol = 'http'
} = {}) {
    console.log(`${protocol}://${host}:${port}`);
}
createServer({port: 8080});
```

## 📊 展开运算符

### 数组展开
```javascript
// 合并数组
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const merged = [...arr1, ...arr2];
console.log(merged); // [1, 2, 3, 4, 5, 6]

// 复制数组（浅拷贝）
const original = [1, 2, 3];
const copy = [...original];

// 转换为数组
const str = 'hello';
const chars = [...str]; // ['h', 'e', 'l', 'l', 'o']

const nodeList = document.querySelectorAll('div');
const array = [...nodeList];

// Math函数应用
const numbers = [1, 5, 3, 9, 2];
console.log(Math.max(...numbers)); // 9

// 插入元素
const arr = [1, 2, 3];
const newArr = [0, ...arr, 4]; // [0, 1, 2, 3, 4]
```

### 对象展开
```javascript
// 合并对象
const obj1 = {a: 1, b: 2};
const obj2 = {c: 3, d: 4};
const merged = {...obj1, ...obj2};

// 浅拷贝
const original = {name: 'John', age: 30};
const copy = {...original};

// 覆盖属性
const defaults = {port: 3000, host: 'localhost'};
const config = {...defaults, port: 8080};
console.log(config); // {port: 8080, host: 'localhost'}

// 添加属性
const user = {name: 'John'};
const userWithAge = {...user, age: 30};

// 条件属性
const includeAge = true;
const person = {
    name: 'John',
    ...(includeAge && {age: 30})
};
```

## ➡️ 箭头函数

### 基本语法
```javascript
// 传统函数
function add(a, b) {
    return a + b;
}

// 箭头函数
const add = (a, b) => a + b;

// 单个参数可省略括号
const square = x => x * x;

// 无参数
const greet = () => 'Hello';

// 多行函数体
const multiply = (a, b) => {
    const result = a * b;
    return result;
};

// 返回对象（需要括号）
const makePerson = (name, age) => ({name, age});
```

### this绑定
```javascript
// 传统函数：this指向调用者
const obj = {
    name: 'John',
    sayHello: function() {
        console.log(`Hello, ${this.name}`);
    }
};
obj.sayHello(); // Hello, John

// 箭头函数：this继承自外层
const obj2 = {
    name: 'John',
    sayHello: () => {
        console.log(`Hello, ${this.name}`); // this不指向obj2
    }
};

// 实际应用：解决this问题
class Counter {
    constructor() {
        this.count = 0;
    }
    
    // 传统方式需要bind
    incrementOld() {
        setTimeout(function() {
            this.count++; // this指向window
        }.bind(this), 1000);
    }
    
    // 箭头函数自动绑定
    increment() {
        setTimeout(() => {
            this.count++; // this正确指向Counter实例
        }, 1000);
    }
}
```

### 使用限制
```javascript
// 不能作为构造函数
const Person = (name) => {
    this.name = name;
};
// new Person('John'); // 报错

// 没有arguments对象
const sum = () => {
    // console.log(arguments); // 报错
};

// 使用剩余参数代替
const sum2 = (...args) => {
    return args.reduce((a, b) => a + b, 0);
};

// 不能用作Generator函数
// const gen = *() => {}; // 语法错误
```

## 📝 模板字符串

### 基本用法
```javascript
// 传统字符串拼接
const name = 'John';
const age = 30;
const message = 'Hello, ' + name + '. You are ' + age + ' years old.';

// 模板字符串
const message2 = `Hello, ${name}. You are ${age} years old.`;

// 多行字符串
const html = `
    <div>
        <h1>${title}</h1>
        <p>${content}</p>
    </div>
`;

// 表达式
const price = 100;
const tax = 0.1;
console.log(`Total: $${price * (1 + tax)}`);

// 函数调用
const upper = name => name.toUpperCase();
console.log(`Hello, ${upper('john')}`);
```

### 标签模板
```javascript
// 自定义模板处理
function highlight(strings, ...values) {
    return strings.reduce((result, str, i) => {
        return result + str + (values[i] ? `<mark>${values[i]}</mark>` : '');
    }, '');
}

const name = 'John';
const age = 30;
const result = highlight`Name: ${name}, Age: ${age}`;
// Name: <mark>John</mark>, Age: <mark>30</mark>

// 实际应用：SQL查询（防注入）
function sql(strings, ...values) {
    // 自动转义values
    return strings.reduce((query, str, i) => {
        const value = values[i];
        const escaped = typeof value === 'string' 
            ? value.replace(/'/g, "''") 
            : value;
        return query + str + (escaped !== undefined ? `'${escaped}'` : '');
    }, '');
}

const userInput = "'; DROP TABLE users; --";
const query = sql`SELECT * FROM users WHERE name = ${userInput}`;
```

## 🎁 默认参数

### 函数默认值
```javascript
// ES5方式
function greet(name) {
    name = name || 'Guest';
    return 'Hello ' + name;
}

// ES6默认参数
function greet(name = 'Guest') {
    return `Hello ${name}`;
}

// 表达式作为默认值
function add(a, b = a * 2) {
    return a + b;
}
add(5); // 15

// 函数调用作为默认值
function getDefault() {
    return 'default';
}
function test(value = getDefault()) {
    return value;
}

// 解构 + 默认值
function createUser({
    name = 'Anonymous',
    age = 18,
    role = 'user'
} = {}) {
    return {name, age, role};
}
```

## 📦 对象增强

### 属性简写
```javascript
// 传统方式
const name = 'John';
const age = 30;
const person = {
    name: name,
    age: age
};

// 简写
const person2 = {name, age};
```

### 方法简写
```javascript
// 传统方式
const obj = {
    sayHello: function() {
        return 'Hello';
    }
};

// 简写
const obj2 = {
    sayHello() {
        return 'Hello';
    }
};
```

### 计算属性名
```javascript
// 动态属性名
const prop = 'name';
const obj = {
    [prop]: 'John',
    ['age']: 30,
    [`${prop}Upper`]: 'JOHN'
};

// 实际应用
const prefix = 'user';
const user = {
    [`${prefix}Name`]: 'John',
    [`${prefix}Age`]: 30,
    [`${prefix}Email`]: 'john@example.com'
};
```

## ⭐ Symbol

### 创建Symbol
```javascript
// 创建唯一标识符
const sym1 = Symbol();
const sym2 = Symbol();
console.log(sym1 === sym2); // false

// 带描述
const sym = Symbol('mySymbol');
console.log(sym.toString()); // Symbol(mySymbol)

// Symbol.for：全局Symbol注册表
const s1 = Symbol.for('app.id');
const s2 = Symbol.for('app.id');
console.log(s1 === s2); // true
```

### 作为属性键
```javascript
const NAME = Symbol('name');
const user = {
    [NAME]: 'John',
    age: 30
};

console.log(user[NAME]); // John
console.log(Object.keys(user)); // ['age'] - Symbol属性不可枚举

// 获取Symbol属性
console.log(Object.getOwnPropertySymbols(user)); // [Symbol(name)]
console.log(Reflect.ownKeys(user)); // ['age', Symbol(name)]
```

### 内置Symbol
```javascript
// Symbol.iterator
const arr = [1, 2, 3];
const iterator = arr[Symbol.iterator]();
console.log(iterator.next()); // {value: 1, done: false}

// Symbol.toStringTag
class MyClass {
    get [Symbol.toStringTag]() {
        return 'MyClass';
    }
}
console.log(Object.prototype.toString.call(new MyClass())); 
// [object MyClass]
```

## 📚 实践练习

### 练习1：数组操作
使用ES6+特性实现：
- 数组去重
- 数组扁平化
- 找出数组交集/并集/差集

### 练习2：对象转换
实现函数：
- 对象属性名转驼峰
- 深度克隆对象
- 合并多个对象

### 练习3：实用工具
编写工具函数：
- 防抖和节流
- 深度比较两个对象
- 字符串模板引擎

## 💡 最佳实践

1. **优先使用const**，需要重新赋值时才用let
2. **使用解构赋值**简化代码
3. **展开运算符**代替concat、apply等
4. **箭头函数**简化回调，注意this绑定
5. **模板字符串**代替字符串拼接

## 📚 参考资料
- [MDN JavaScript](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript)
- [ES6入门教程](https://es6.ruanyifeng.com/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)


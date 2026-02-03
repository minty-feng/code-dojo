# 02-异步编程

## 📋 学习目标
- 理解JavaScript事件循环机制
- 掌握Promise的使用和原理
- 精通async/await异步语法
- 理解并发控制和错误处理

## 🔄 事件循环

### 执行模型
```javascript
// 同步任务
console.log('1');

// 宏任务(MacroTask)
setTimeout(() => {
    console.log('2');
}, 0);

// 微任务(MicroTask)
Promise.resolve().then(() => {
    console.log('3');
});

console.log('4');

// 输出顺序：1 4 3 2
```

### 任务队列
```javascript
/*
执行顺序：
1. 同步代码
2. 微任务队列(Promise, MutationObserver)
3. 宏任务队列(setTimeout, setInterval, I/O)
*/

console.log('script start');

setTimeout(() => {
    console.log('setTimeout');
}, 0);

Promise.resolve()
    .then(() => {
        console.log('promise1');
    })
    .then(() => {
        console.log('promise2');
    });

console.log('script end');

// 输出：
// script start
// script end
// promise1
// promise2
// setTimeout
```

## 📞 回调函数

### 基本回调
```javascript
// 简单回调
function getData(callback) {
    setTimeout(() => {
        callback({name: 'John', age: 30});
    }, 1000);
}

getData((data) => {
    console.log(data);
});

// Node.js错误优先回调
fs.readFile('file.txt', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    console.log(data);
});
```

### 回调地狱
```javascript
// 回调地狱示例
getUser(userId, (err, user) => {
    if (err) {
        handleError(err);
    } else {
        getOrders(user.id, (err, orders) => {
            if (err) {
                handleError(err);
            } else {
                getOrderDetails(orders[0].id, (err, details) => {
                    if (err) {
                        handleError(err);
                    } else {
                        // 继续嵌套...
                    }
                });
            }
        });
    }
});
```

## 🎁 Promise

### 基本用法
```javascript
// 创建Promise
const promise = new Promise((resolve, reject) => {
    // 异步操作
    setTimeout(() => {
        const success = true;
        if (success) {
            resolve('Success!');
        } else {
            reject(new Error('Failed!'));
        }
    }, 1000);
});

// 使用Promise
promise
    .then(result => {
        console.log(result); // Success!
        return 'Next value';
    })
    .then(result => {
        console.log(result); // Next value
    })
    .catch(error => {
        console.error(error);
    })
    .finally(() => {
        console.log('Cleanup');
    });
```

### Promise状态
```javascript
/*
三种状态：
1. pending（进行中）
2. fulfilled（已成功）
3. rejected（已失败）

状态只能从pending改变为fulfilled或rejected
状态一旦改变就不会再变
*/

const p1 = Promise.resolve('Success'); // 立即fulfilled
const p2 = Promise.reject(new Error('Failed')); // 立即rejected
```

### 链式调用
```javascript
function getUser(id) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({id, name: 'John'});
        }, 1000);
    });
}

function getOrders(userId) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve([{id: 1}, {id: 2}]);
        }, 1000);
    });
}

// 链式调用
getUser(1)
    .then(user => {
        console.log('User:', user);
        return getOrders(user.id);
    })
    .then(orders => {
        console.log('Orders:', orders);
    })
    .catch(error => {
        console.error('Error:', error);
    });
```

### Promise静态方法
```javascript
// Promise.all - 所有成功才成功
const p1 = Promise.resolve(1);
const p2 = Promise.resolve(2);
const p3 = Promise.resolve(3);

Promise.all([p1, p2, p3])
    .then(results => {
        console.log(results); // [1, 2, 3]
    })
    .catch(error => {
        console.error('One failed:', error);
    });

// Promise.allSettled - 等待所有完成
Promise.allSettled([p1, p2, Promise.reject('error')])
    .then(results => {
        results.forEach(result => {
            if (result.status === 'fulfilled') {
                console.log('Success:', result.value);
            } else {
                console.log('Failed:', result.reason);
            }
        });
    });

// Promise.race - 最快的一个
Promise.race([
    fetch('/api/slow'),
    new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 3000)
    )
])
    .then(result => console.log(result))
    .catch(error => console.error(error));

// Promise.any - 任意一个成功
Promise.any([
    fetch('/api/1').catch(() => 'API1 failed'),
    fetch('/api/2').catch(() => 'API2 failed'),
    fetch('/api/3').catch(() => 'API3 failed')
])
    .then(result => console.log('First success:', result))
    .catch(() => console.log('All failed'));
```

### Promise实现
```javascript
class MyPromise {
    constructor(executor) {
        this.state = 'pending';
        this.value = undefined;
        this.reason = undefined;
        this.onFulfilledCallbacks = [];
        this.onRejectedCallbacks = [];
        
        const resolve = (value) => {
            if (this.state === 'pending') {
                this.state = 'fulfilled';
                this.value = value;
                this.onFulfilledCallbacks.forEach(fn => fn());
            }
        };
        
        const reject = (reason) => {
            if (this.state === 'pending') {
                this.state = 'rejected';
                this.reason = reason;
                this.onRejectedCallbacks.forEach(fn => fn());
            }
        };
        
        try {
            executor(resolve, reject);
        } catch (error) {
            reject(error);
        }
    }
    
    then(onFulfilled, onRejected) {
        onFulfilled = typeof onFulfilled === 'function' 
            ? onFulfilled 
            : value => value;
        onRejected = typeof onRejected === 'function' 
            ? onRejected 
            : reason => { throw reason };
            
        return new MyPromise((resolve, reject) => {
            if (this.state === 'fulfilled') {
                setTimeout(() => {
                    try {
                        const result = onFulfilled(this.value);
                        resolve(result);
                    } catch (error) {
                        reject(error);
                    }
                });
            }
            
            if (this.state === 'rejected') {
                setTimeout(() => {
                    try {
                        const result = onRejected(this.reason);
                        resolve(result);
                    } catch (error) {
                        reject(error);
                    }
                });
            }
            
            if (this.state === 'pending') {
                this.onFulfilledCallbacks.push(() => {
                    setTimeout(() => {
                        try {
                            const result = onFulfilled(this.value);
                            resolve(result);
                        } catch (error) {
                            reject(error);
                        }
                    });
                });
                
                this.onRejectedCallbacks.push(() => {
                    setTimeout(() => {
                        try {
                            const result = onRejected(this.reason);
                            resolve(result);
                        } catch (error) {
                            reject(error);
                        }
                    });
                });
            }
        });
    }
}
```

## 🚀 Async/Await

### 基本用法
```javascript
// async函数返回Promise
async function getData() {
    return 'data';
}

getData().then(data => console.log(data)); // data

// await等待Promise
async function fetchUser() {
    const response = await fetch('/api/user');
    const user = await response.json();
    return user;
}

// 等同于
function fetchUser() {
    return fetch('/api/user')
        .then(response => response.json());
}
```

### 错误处理
```javascript
// try-catch捕获错误
async function getData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// 统一错误处理
async function request(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
}

async function main() {
    try {
        const data = await request('/api/data');
        console.log(data);
    } catch (error) {
        console.error('Failed:', error.message);
    }
}

// 顶层await（ES2022）
const data = await fetch('/api/data').then(r => r.json());
```

### 并发执行
```javascript
// ❌ 串行执行（慢）
async function sequential() {
    const user = await fetchUser();      // 1秒
    const orders = await fetchOrders();  // 1秒
    const products = await fetchProducts(); // 1秒
    return {user, orders, products};     // 总共3秒
}

// ✅ 并发执行（快）
async function concurrent() {
    const [user, orders, products] = await Promise.all([
        fetchUser(),
        fetchOrders(),
        fetchProducts()
    ]);
    return {user, orders, products};     // 总共1秒
}

// 部分依赖
async function partial() {
    const user = await fetchUser();
    // 这两个可以并发
    const [orders, profile] = await Promise.all([
        fetchOrders(user.id),
        fetchProfile(user.id)
    ]);
    return {user, orders, profile};
}
```

### 循环中的异步
```javascript
// ❌ forEach不等待
async function wrong() {
    const ids = [1, 2, 3];
    ids.forEach(async (id) => {
        const data = await fetchData(id);
        console.log(data);
    });
    console.log('Done'); // 会立即执行
}

// ✅ for...of串行执行
async function serial() {
    const ids = [1, 2, 3];
    for (const id of ids) {
        const data = await fetchData(id);
        console.log(data);
    }
    console.log('Done');
}

// ✅ Promise.all并发执行
async function parallel() {
    const ids = [1, 2, 3];
    const promises = ids.map(id => fetchData(id));
    const results = await Promise.all(promises);
    results.forEach(data => console.log(data));
    console.log('Done');
}

// ✅ map + Promise.all
async function mapAsync() {
    const ids = [1, 2, 3];
    const results = await Promise.all(
        ids.map(async (id) => {
            const data = await fetchData(id);
            return processData(data);
        })
    );
    return results;
}
```

## 🔧 实战技巧

### 超时控制
```javascript
function timeout(ms) {
    return new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Timeout')), ms);
    });
}

async function fetchWithTimeout(url, ms = 3000) {
    return Promise.race([
        fetch(url),
        timeout(ms)
    ]);
}

// 使用
try {
    const response = await fetchWithTimeout('/api/data', 5000);
    const data = await response.json();
} catch (error) {
    console.error('Request failed or timeout:', error);
}
```

### 重试机制
```javascript
async function retry(fn, maxAttempts = 3, delay = 1000) {
    for (let i = 0; i < maxAttempts; i++) {
        try {
            return await fn();
        } catch (error) {
            if (i === maxAttempts - 1) throw error;
            console.log(`Attempt ${i + 1} failed, retrying...`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// 使用
const data = await retry(() => fetch('/api/data'), 3, 2000);
```

### 并发限制
```javascript
class PromisePool {
    constructor(maxConcurrency) {
        this.maxConcurrency = maxConcurrency;
        this.currentCount = 0;
        this.queue = [];
    }
    
    async add(promiseFactory) {
        while (this.currentCount >= this.maxConcurrency) {
            await Promise.race(this.queue);
        }
        
        this.currentCount++;
        const promise = promiseFactory();
        const queueItem = promise.then(
            () => this.remove(queueItem),
            () => this.remove(queueItem)
        );
        this.queue.push(queueItem);
        
        return promise;
    }
    
    remove(promise) {
        const index = this.queue.indexOf(promise);
        this.queue.splice(index, 1);
        this.currentCount--;
    }
}

// 使用
const pool = new PromisePool(3);
const tasks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const results = await Promise.all(
    tasks.map(id => pool.add(() => fetchData(id)))
);
```

### 取消请求
```javascript
// 使用AbortController
const controller = new AbortController();
const signal = controller.signal;

fetch('/api/data', {signal})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => {
        if (error.name === 'AbortError') {
            console.log('Request cancelled');
        }
    });

// 取消请求
controller.abort();

// 超时取消
async function fetchWithAbort(url, timeout = 5000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {signal: controller.signal});
        clearTimeout(timeoutId);
        return await response.json();
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    }
}
```

### 缓存Promise
```javascript
const cache = new Map();

function getCachedData(key, fetcher) {
    if (!cache.has(key)) {
        cache.set(key, fetcher());
    }
    return cache.get(key);
}

// 使用
const userData = await getCachedData('user:1', () => fetchUser(1));

// 带过期时间的缓存
class PromiseCache {
    constructor(ttl = 60000) {
        this.cache = new Map();
        this.ttl = ttl;
    }
    
    async get(key, fetcher) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.ttl) {
            return cached.value;
        }
        
        const value = await fetcher();
        this.cache.set(key, {
            value,
            timestamp: Date.now()
        });
        return value;
    }
}
```

## 📚 实践练习

### 练习1：Promise实现
手动实现：
- Promise.all
- Promise.race
- Promise.allSettled
- Promise.any

### 练习2：异步工具函数
实现以下工具：
- 带超时的fetch
- 重试机制
- 并发控制
- 请求队列

### 练习3：实际应用
创建一个数据获取层：
- 支持缓存
- 支持取消
- 支持重试
- 错误处理

## 💡 最佳实践

1. **优先使用async/await**而不是Promise链
2. **注意Promise.all的失败处理**
3. **合理使用并发和串行**
4. **总是处理异步错误**
5. **避免在循环中使用await**（除非需要串行）

## 📚 参考资料
- [MDN Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [MDN async/await](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function)
- [JavaScript异步编程](https://javascript.info/async)


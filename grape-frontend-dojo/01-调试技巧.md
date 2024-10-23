# 01-调试技巧

## 📋 学习目标
- 掌握浏览器调试工具
- 学习JavaScript调试技巧
- 理解性能分析方法
- 掌握React/Vue调试工具

## 🔍 Chrome DevTools

### Console调试
```javascript
// 基本输出
console.log('Hello');
console.info('Information');
console.warn('Warning');
console.error('Error');

// 格式化输出
console.log('%c Styled Log', 'color: blue; font-size: 20px;');

// 表格显示
const users = [
    {name: 'John', age: 30},
    {name: 'Jane', age: 25}
];
console.table(users);

// 分组
console.group('User Info');
console.log('Name: John');
console.log('Age: 30');
console.groupEnd();

// 计时
console.time('fetch');
await fetch('/api/data');
console.timeEnd('fetch'); // fetch: 123.45ms

// 计数
for (let i = 0; i < 3; i++) {
    console.count('loop'); // loop: 1, loop: 2, loop: 3
}

// 断言
console.assert(1 === 2, 'Values are not equal');

// 追踪调用栈
console.trace('Trace point');
```

### 断点调试
```javascript
// 1. debugger语句
function calculate(a, b) {
    debugger; // 代码会在此处暂停
    return a + b;
}

// 2. 条件断点
// 在DevTools中右键断点，设置条件
for (let i = 0; i < 100; i++) {
    // 只有i === 50时才暂停
    console.log(i);
}

// 3. 监听DOM变化
// Elements -> 右键元素 -> Break on -> Subtree modifications
```

### Network调试
```javascript
// 查看请求
fetch('/api/data')
    .then(res => res.json())
    .then(data => console.log(data));

// 模拟慢网络
// Network -> Throttling -> Slow 3G

// 过滤请求
// Network -> Filter: XHR, JS, CSS, etc.

// 复制请求
// Network -> 右键请求 -> Copy -> Copy as fetch
```

### Performance分析
```javascript
// 性能标记
performance.mark('start');

// 执行代码
for (let i = 0; i < 1000000; i++) {
    // heavy operation
}

performance.mark('end');
performance.measure('operation', 'start', 'end');

const measures = performance.getEntriesByType('measure');
console.log(measures[0].duration);

// 使用Chrome DevTools
// Performance -> Record -> 执行操作 -> Stop
```

## 🔧 JavaScript调试技巧

### 错误处理
```javascript
// try-catch
try {
    const data = JSON.parse(invalidJSON);
} catch (error) {
    console.error('Parse error:', error);
    console.error('Stack trace:', error.stack);
}

// 全局错误捕获
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Promise错误
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// 自定义错误
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

function validate(value) {
    if (!value) {
        throw new ValidationError('Value is required');
    }
}
```

### 调试工具函数
```javascript
// 深拷贝调试
function debugClone(obj) {
    console.log('Original:', obj);
    const cloned = JSON.parse(JSON.stringify(obj));
    console.log('Cloned:', cloned);
    return cloned;
}

// 函数性能测试
function measurePerformance(fn, label = 'Function') {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${label} took ${(end - start).toFixed(2)}ms`);
    return result;
}

// 内存泄漏检测
class LeakDetector {
    constructor() {
        this.listeners = new Set();
    }
    
    track(element, event, handler) {
        element.addEventListener(event, handler);
        this.listeners.add({element, event, handler});
        console.log(`Tracking ${this.listeners.size} listeners`);
    }
    
    cleanup() {
        this.listeners.forEach(({element, event, handler}) => {
            element.removeEventListener(event, handler);
        });
        this.listeners.clear();
        console.log('All listeners cleaned up');
    }
}
```

### 调试异步代码
```javascript
// Promise调试
async function debugFetch(url) {
    console.log('Fetching:', url);
    
    try {
        const response = await fetch(url);
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Data:', data);
        
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// 并发调试
async function debugParallel() {
    console.time('parallel');
    
    const results = await Promise.all([
        fetch('/api/1').then(r => {
            console.log('API 1 done');
            return r.json();
        }),
        fetch('/api/2').then(r => {
            console.log('API 2 done');
            return r.json();
        })
    ]);
    
    console.timeEnd('parallel');
    return results;
}
```

## ⚛️ React调试

### React DevTools
```jsx
// 查看组件Props和State
function Counter() {
    const [count, setCount] = useState(0);
    
    // 在React DevTools中可以看到count值
    // 可以直接修改state测试
    
    return (
        <div>
            <p>{count}</p>
            <button onClick={() => setCount(c => c + 1)}>+</button>
        </div>
    );
}

// Profiler分析性能
import {Profiler} from 'react';

function onRenderCallback(id, phase, actualDuration) {
    console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

function App() {
    return (
        <Profiler id="App" onRender={onRenderCallback}>
            <MyComponent />
        </Profiler>
    );
}
```

### React调试技巧
```jsx
// useDebugValue
function useCustomHook(value) {
    useDebugValue(value > 0 ? 'Positive' : 'Negative');
    return value;
}

// 调试Hooks
function DebugComponent() {
    const [count, setCount] = useState(0);
    
    useEffect(() => {
        console.log('Component mounted');
        return () => console.log('Component unmounted');
    }, []);
    
    useEffect(() => {
        console.log('Count changed:', count);
    }, [count]);
    
    return <div>{count}</div>;
}

// Why-did-you-render
import whyDidYouRender from '@welldone-software/why-did-you-render';

whyDidYouRender(React, {
    trackAllPureComponents: true,
});

// 标记组件
MyComponent.whyDidYouRender = true;
```

## 💚 Vue调试

### Vue DevTools
```vue
<script setup>
import {ref, watch} from 'vue';

const count = ref(0);

// 在Vue DevTools中查看响应式数据
watch(count, (newVal, oldVal) => {
    console.log(`Count: ${oldVal} -> ${newVal}`);
});

// 调试computed
const double = computed(() => {
    console.log('Computing double');
    return count.value * 2;
});
</script>
```

### Vue调试技巧
```vue
<script setup>
// 调试Props
const props = defineProps({
    title: String
});

watch(() => props.title, (val) => {
    console.log('Title changed:', val);
}, {immediate: true});

// 调试生命周期
onMounted(() => {
    console.log('Component mounted');
});

onUpdated(() => {
    console.log('Component updated');
});

onBeforeUnmount(() => {
    console.log('Component will unmount');
});

// 调试Provide/Inject
const theme = inject('theme', 'light');
console.log('Injected theme:', theme);
</script>
```

## 🌐 网络调试

### 请求拦截
```javascript
// 使用axios拦截器
axios.interceptors.request.use(config => {
    console.log('Request:', config.method, config.url);
    console.log('Data:', config.data);
    return config;
});

axios.interceptors.response.use(
    response => {
        console.log('Response:', response.status, response.data);
        return response;
    },
    error => {
        console.error('Request failed:', error);
        return Promise.reject(error);
    }
);
```

### 模拟数据
```javascript
// 使用MSW (Mock Service Worker)
import {rest} from 'msw';
import {setupWorker} from 'msw/browser';

const worker = setupWorker(
    rest.get('/api/user', (req, res, ctx) => {
        console.log('Mocking /api/user');
        return res(
            ctx.json({
                name: 'John',
                age: 30
            })
        );
    })
);

worker.start();
```

## 🔍 内存调试

### 内存泄漏检测
```javascript
// 检查DOM节点泄漏
class DOMLeakDetector {
    constructor() {
        this.nodes = new WeakSet();
    }
    
    track(node) {
        this.nodes.add(node);
    }
    
    check() {
        // 使用Chrome DevTools Memory Profiler
        // 1. Take Heap Snapshot
        // 2. 执行操作
        // 3. Take another Snapshot
        // 4. 比较两个快照
    }
}

// 避免闭包泄漏
function createClosure() {
    const largeData = new Array(1000000);
    
    // ❌ 泄漏
    return function() {
        console.log(largeData.length);
    };
    
    // ✅ 不泄漏
    const length = largeData.length;
    return function() {
        console.log(length);
    };
}
```

## 💡 调试最佳实践

### 1. 使用Source Maps
```javascript
// vite.config.ts
export default {
    build: {
        sourcemap: true
    }
};
```

### 2. 日志分级
```javascript
const DEBUG = process.env.NODE_ENV === 'development';

const logger = {
    debug: (...args) => DEBUG && console.log('[DEBUG]', ...args),
    info: (...args) => console.log('[INFO]', ...args),
    warn: (...args) => console.warn('[WARN]', ...args),
    error: (...args) => console.error('[ERROR]', ...args)
};

logger.debug('Debug message');
logger.error('Error occurred');
```

### 3. 条件断点
```javascript
// 只在特定条件下断点
function processItems(items) {
    for (let item of items) {
        // 添加条件断点：item.id === 123
        processItem(item);
    }
}
```

### 4. 错误边界
```jsx
// React错误边界
class ErrorBoundary extends React.Component {
    state = {hasError: false};
    
    static getDerivedStateFromError(error) {
        return {hasError: true};
    }
    
    componentDidCatch(error, errorInfo) {
        console.error('Error:', error);
        console.error('Error Info:', errorInfo);
        // 发送到错误跟踪服务
    }
    
    render() {
        if (this.state.hasError) {
            return <h1>Something went wrong.</h1>;
        }
        return this.props.children;
    }
}
```

## 📚 调试工具推荐

### 浏览器扩展
- React DevTools
- Vue DevTools
- Redux DevTools
- Apollo Client DevTools
- Lighthouse

### VSCode扩展
- Debugger for Chrome
- Error Lens
- Console Ninja
- Quokka.js

## 📚 参考资料
- [Chrome DevTools文档](https://developer.chrome.com/docs/devtools/)
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Vue DevTools](https://devtools.vuejs.org/)


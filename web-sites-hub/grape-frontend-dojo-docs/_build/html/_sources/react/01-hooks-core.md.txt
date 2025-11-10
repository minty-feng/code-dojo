# 01-React Hooks核心

## 📋 学习目标
- 掌握常用Hooks的使用
- 理解Hooks的原理和规则
- 学习自定义Hook开发
- 掌握性能优化Hooks

## 🪝 useState

### 基本用法
```jsx
import {useState} from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(c => c + 1)}>+1 (函数式)</button>
        </div>
    );
}

// 初始值可以是函数
function ExpensiveComponent() {
    const [data, setData] = useState(() => {
        return computeExpensiveValue();
    });
}
```

### 对象和数组状态
```jsx
function Form() {
    const [user, setUser] = useState({
        name: '',
        age: 0
    });
    
    // 更新对象（需要创建新对象）
    const updateName = (name) => {
        setUser({...user, name});
        // 或
        setUser(prev => ({...prev, name}));
    };
    
    // 数组状态
    const [items, setItems] = useState([]);
    
    const addItem = (item) => {
        setItems([...items, item]);
    };
    
    const removeItem = (index) => {
        setItems(items.filter((_, i) => i !== index));
    };
}
```

## 🎬 useEffect

### 基本用法
```jsx
import {useEffect} from 'react';

function Component() {
    // 每次渲染都执行
    useEffect(() => {
        console.log('Rendered');
    });
    
    // 仅首次渲染执行
    useEffect(() => {
        console.log('Mounted');
    }, []);
    
    // 依赖变化时执行
    useEffect(() => {
        console.log('Count changed:', count);
    }, [count]);
    
    // 清理函数
    useEffect(() => {
        const timer = setInterval(() => {
            console.log('Tick');
        }, 1000);
        
        return () => {
            clearInterval(timer);
        };
    }, []);
}
```

### 实际应用
```jsx
// 数据获取
function UserProfile({userId}) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        let isCancelled = false;
        
        async function fetchUser() {
            setLoading(true);
            try {
                const response = await fetch(`/api/users/${userId}`);
                const data = await response.json();
                if (!isCancelled) {
                    setUser(data);
                }
            } catch (error) {
                console.error(error);
            } finally {
                if (!isCancelled) {
                    setLoading(false);
                }
            }
        }
        
        fetchUser();
        
        return () => {
            isCancelled = true;
        };
    }, [userId]);
    
    if (loading) return <div>Loading...</div>;
    return <div>{user?.name}</div>;
}

// 订阅事件
function WindowSize() {
    const [size, setSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight
    });
    
    useEffect(() => {
        const handleResize = () => {
            setSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        };
        
        window.addEventListener('resize', handleResize);
        
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);
    
    return <div>{size.width} x {size.height}</div>;
}
```

## 🎯 useContext

### 基本用法
```jsx
import {createContext, useContext} from 'react';

// 创建Context
const ThemeContext = createContext('light');

// Provider
function App() {
    return (
        <ThemeContext.Provider value="dark">
            <Toolbar />
        </ThemeContext.Provider>
    );
}

// 使用Context
function Toolbar() {
    const theme = useContext(ThemeContext);
    return <div className={theme}>Toolbar</div>;
}

// 复杂Context
const UserContext = createContext(null);

export function UserProvider({children}) {
    const [user, setUser] = useState(null);
    
    const login = async (credentials) => {
        const userData = await api.login(credentials);
        setUser(userData);
    };
    
    const logout = () => {
        setUser(null);
    };
    
    return (
        <UserContext.Provider value={{user, login, logout}}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within UserProvider');
    }
    return context;
}
```

## 🔄 useReducer

### 基本用法
```jsx
import {useReducer} from 'react';

// Reducer函数
function counterReducer(state, action) {
    switch (action.type) {
        case 'increment':
            return {count: state.count + 1};
        case 'decrement':
            return {count: state.count - 1};
        case 'reset':
            return {count: 0};
        default:
            throw new Error('Unknown action type');
    }
}

function Counter() {
    const [state, dispatch] = useReducer(counterReducer, {count: 0});
    
    return (
        <div>
            <p>Count: {state.count}</p>
            <button onClick={() => dispatch({type: 'increment'})}>+</button>
            <button onClick={() => dispatch({type: 'decrement'})}>-</button>
            <button onClick={() => dispatch({type: 'reset'})}>Reset</button>
        </div>
    );
}

// TypeScript版本
type State = {count: number};
type Action = 
    | {type: 'increment'}
    | {type: 'decrement'}
    | {type: 'reset'};

function counterReducer(state: State, action: Action): State {
    // ...
}
```

### 复杂表单管理
```jsx
function formReducer(state, action) {
    switch (action.type) {
        case 'UPDATE_FIELD':
            return {
                ...state,
                [action.field]: action.value
            };
        case 'RESET':
            return action.initialState;
        default:
            return state;
    }
}

function Form() {
    const initialState = {
        name: '',
        email: '',
        message: ''
    };
    
    const [formData, dispatch] = useReducer(formReducer, initialState);
    
    const handleChange = (field) => (e) => {
        dispatch({
            type: 'UPDATE_FIELD',
            field,
            value: e.target.value
        });
    };
    
    return (
        <form>
            <input
                value={formData.name}
                onChange={handleChange('name')}
            />
            <input
                value={formData.email}
                onChange={handleChange('email')}
            />
        </form>
    );
}
```

## 📌 useRef

### 基本用法
```jsx
import {useRef, useEffect} from 'react';

function Input() {
    const inputRef = useRef(null);
    
    useEffect(() => {
        // 自动聚焦
        inputRef.current.focus();
    }, []);
    
    return <input ref={inputRef} />;
}

// 存储可变值（不触发重渲染）
function Timer() {
    const intervalRef = useRef(null);
    const [count, setCount] = useState(0);
    
    const start = () => {
        if (intervalRef.current) return;
        intervalRef.current = setInterval(() => {
            setCount(c => c + 1);
        }, 1000);
    };
    
    const stop = () => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
    };
    
    useEffect(() => {
        return () => stop();
    }, []);
    
    return (
        <div>
            <p>{count}</p>
            <button onClick={start}>Start</button>
            <button onClick={stop}>Stop</button>
        </div>
    );
}
```

## ⚡ useMemo

### 基本用法
```jsx
import {useMemo} from 'react';

function ExpensiveComponent({items}) {
    // 缓存计算结果
    const total = useMemo(() => {
        console.log('Computing total...');
        return items.reduce((sum, item) => sum + item.price, 0);
    }, [items]);
    
    return <div>Total: ${total}</div>;
}

// 缓存对象引用
function Parent() {
    const [count, setCount] = useState(0);
    
    // 每次渲染都会创建新对象
    // const config = {theme: 'dark'};
    
    // 使用useMemo缓存
    const config = useMemo(() => ({theme: 'dark'}), []);
    
    return <Child config={config} />;
}

const Child = React.memo(({config}) => {
    console.log('Child rendered');
    return <div>{config.theme}</div>;
});
```

## 🔄 useCallback

### 基本用法
```jsx
import {useCallback} from 'react';

function Parent() {
    const [count, setCount] = useState(0);
    
    // 每次渲染都创建新函数
    // const handleClick = () => setCount(c => c + 1);
    
    // 缓存函数
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []);
    
    return <Child onClick={handleClick} />;
}

const Child = React.memo(({onClick}) => {
    console.log('Child rendered');
    return <button onClick={onClick}>Click</button>;
});

// 实际应用
function SearchInput({onSearch}) {
    const [query, setQuery] = useState('');
    
    // 防抖搜索
    const debouncedSearch = useCallback(
        debounce((value) => {
            onSearch(value);
        }, 500),
        [onSearch]
    );
    
    const handleChange = (e) => {
        const value = e.target.value;
        setQuery(value);
        debouncedSearch(value);
    };
    
    return <input value={query} onChange={handleChange} />;
}
```

## 🛠️ 自定义Hook

### 基本自定义Hook
```jsx
// useLocalStorage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : initialValue;
    });
    
    const setStoredValue = (newValue) => {
        setValue(newValue);
        localStorage.setItem(key, JSON.stringify(newValue));
    };
    
    return [value, setStoredValue];
}

// 使用
function App() {
    const [name, setName] = useLocalStorage('name', '');
    return <input value={name} onChange={e => setName(e.target.value)} />;
}

// useFetch
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        let isCancelled = false;
        
        async function fetchData() {
            try {
                const response = await fetch(url);
                const json = await response.json();
                if (!isCancelled) {
                    setData(json);
                    setError(null);
                }
            } catch (err) {
                if (!isCancelled) {
                    setError(err);
                }
            } finally {
                if (!isCancelled) {
                    setLoading(false);
                }
            }
        }
        
        fetchData();
        
        return () => {
            isCancelled = true;
        };
    }, [url]);
    
    return {data, loading, error};
}

// 使用
function UserList() {
    const {data, loading, error} = useFetch('/api/users');
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    
    return (
        <ul>
            {data.map(user => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
}
```

### 高级自定义Hook
```jsx
// useDebounce
function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);
    
    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);
        
        return () => clearTimeout(timer);
    }, [value, delay]);
    
    return debouncedValue;
}

// useInterval
function useInterval(callback, delay) {
    const savedCallback = useRef();
    
    useEffect(() => {
        savedCallback.current = callback;
    }, [callback]);
    
    useEffect(() => {
        if (delay === null) return;
        
        const tick = () => savedCallback.current();
        const id = setInterval(tick, delay);
        
        return () => clearInterval(id);
    }, [delay]);
}

// usePrevious
function usePrevious(value) {
    const ref = useRef();
    
    useEffect(() => {
        ref.current = value;
    }, [value]);
    
    return ref.current;
}
```

## 📏 Hooks规则

### 两大规则
```jsx
// ✅ 规则1：只在顶层调用Hook
function Component() {
    const [count, setCount] = useState(0);
    
    // ❌ 不要在条件语句中调用
    if (count > 0) {
        // const [name, setName] = useState('');
    }
    
    // ❌ 不要在循环中调用
    for (let i = 0; i < 10; i++) {
        // const [item, setItem] = useState(i);
    }
}

// ✅ 规则2：只在React函数中调用Hook
function Component() {
    const [count, setCount] = useState(0); // ✅
}

function useCustomHook() {
    const [value, setValue] = useState(0); // ✅
}

// ❌ 不要在普通函数中调用
function normalFunction() {
    // const [value, setValue] = useState(0);
}
```

## 📚 实践练习

### 练习1：自定义Hook
实现以下自定义Hook：
- useToggle：布尔值切换
- useArray：数组操作
- useAsync：异步操作

### 练习2：表单管理
使用useReducer实现表单管理：
- 字段验证
- 错误提示
- 提交处理

### 练习3：性能优化
优化以下组件：
- 大列表渲染
- 复杂计算
- 频繁更新

## 📚 参考资料
- [React Hooks官方文档](https://react.dev/reference/react)
- [usehooks.com](https://usehooks.com/)
- [React Hooks Cheatsheet](https://react-hooks-cheatsheet.com/)


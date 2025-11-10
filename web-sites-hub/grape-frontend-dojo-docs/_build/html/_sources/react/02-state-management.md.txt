# 02-React状态管理

## 📋 学习目标
- 掌握Context API状态共享
- 学习Redux Toolkit使用
- 理解Zustand轻量状态库
- 掌握状态管理最佳实践

## 🎯 Context API

### 基本用法
```jsx
import {createContext, useContext, useState} from 'react';

// 创建Context
const ThemeContext = createContext(null);

// Provider组件
export function ThemeProvider({children}) {
    const [theme, setTheme] = useState('light');
    
    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };
    
    return (
        <ThemeContext.Provider value={{theme, toggleTheme}}>
            {children}
        </ThemeContext.Provider>
    );
}

// 自定义Hook
export function useTheme() {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within ThemeProvider');
    }
    return context;
}

// 使用
function App() {
    return (
        <ThemeProvider>
            <Header />
            <Main />
        </ThemeProvider>
    );
}

function Header() {
    const {theme, toggleTheme} = useTheme();
    return (
        <header className={theme}>
            <button onClick={toggleTheme}>
                Toggle Theme
            </button>
        </header>
    );
}
```

### 复杂状态管理
```jsx
import {createContext, useContext, useReducer} from 'react';

// 定义状态和Actions
const initialState = {
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
};

function authReducer(state, action) {
    switch (action.type) {
        case 'LOGIN_START':
            return {...state, loading: true, error: null};
        case 'LOGIN_SUCCESS':
            return {
                ...state,
                loading: false,
                isAuthenticated: true,
                user: action.payload
            };
        case 'LOGIN_ERROR':
            return {
                ...state,
                loading: false,
                error: action.payload
            };
        case 'LOGOUT':
            return initialState;
        default:
            return state;
    }
}

// Context
const AuthContext = createContext(null);

// Provider
export function AuthProvider({children}) {
    const [state, dispatch] = useReducer(authReducer, initialState);
    
    const login = async (credentials) => {
        dispatch({type: 'LOGIN_START'});
        try {
            const user = await api.login(credentials);
            dispatch({type: 'LOGIN_SUCCESS', payload: user});
        } catch (error) {
            dispatch({type: 'LOGIN_ERROR', payload: error.message});
        }
    };
    
    const logout = () => {
        dispatch({type: 'LOGOUT'});
    };
    
    return (
        <AuthContext.Provider value={{...state, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
}

// Hook
export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}
```

## 🔴 Redux Toolkit

### 安装和配置
```bash
pnpm add @reduxjs/toolkit react-redux
```

### 创建Store
```javascript
// store.js
import {configureStore} from '@reduxjs/toolkit';
import counterReducer from './features/counter/counterSlice';
import userReducer from './features/user/userSlice';

export const store = configureStore({
    reducer: {
        counter: counterReducer,
        user: userReducer
    },
    middleware: (getDefaultMiddleware) => 
        getDefaultMiddleware({
            serializableCheck: false
        })
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 创建Slice
```javascript
// counterSlice.js
import {createSlice, PayloadAction} from '@reduxjs/toolkit';

interface CounterState {
    value: number;
    status: 'idle' | 'loading';
}

const initialState: CounterState = {
    value: 0,
    status: 'idle'
};

export const counterSlice = createSlice({
    name: 'counter',
    initialState,
    reducers: {
        increment: (state) => {
            state.value += 1;
        },
        decrement: (state) => {
            state.value -= 1;
        },
        incrementByAmount: (state, action: PayloadAction<number>) => {
            state.value += action.payload;
        },
        reset: (state) => {
            state.value = 0;
        }
    }
});

export const {increment, decrement, incrementByAmount, reset} = counterSlice.actions;
export default counterSlice.reducer;
```

### 异步Thunk
```javascript
import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';

// 异步Thunk
export const fetchUser = createAsyncThunk(
    'user/fetchUser',
    async (userId: string) => {
        const response = await fetch(`/api/users/${userId}`);
        return response.json();
    }
);

interface UserState {
    data: User | null;
    loading: boolean;
    error: string | null;
}

const initialState: UserState = {
    data: null,
    loading: false,
    error: null
};

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        clearUser: (state) => {
            state.data = null;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchUser.fulfilled, (state, action) => {
                state.loading = false;
                state.data = action.payload;
            })
            .addCase(fetchUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch';
            });
    }
});

export const {clearUser} = userSlice.actions;
export default userSlice.reducer;
```

### 使用Redux
```jsx
// App.tsx
import {Provider} from 'react-redux';
import {store} from './store';

function App() {
    return (
        <Provider store={store}>
            <Counter />
        </Provider>
    );
}

// Counter.tsx
import {useSelector, useDispatch} from 'react-redux';
import {increment, decrement, incrementByAmount} from './counterSlice';
import type {RootState, AppDispatch} from './store';

function Counter() {
    const count = useSelector((state: RootState) => state.counter.value);
    const dispatch = useDispatch<AppDispatch>();
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => dispatch(increment())}>+</button>
            <button onClick={() => dispatch(decrement())}>-</button>
            <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
        </div>
    );
}

// 带异步的组件
function UserProfile({userId}) {
    const {data, loading, error} = useSelector((state: RootState) => state.user);
    const dispatch = useDispatch<AppDispatch>();
    
    useEffect(() => {
        dispatch(fetchUser(userId));
    }, [userId, dispatch]);
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    
    return <div>{data?.name}</div>;
}
```

### 类型安全的Hooks
```typescript
// hooks.ts
import {useDispatch, useSelector, TypedUseSelectorHook} from 'react-redux';
import type {RootState, AppDispatch} from './store';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// 使用
import {useAppDispatch, useAppSelector} from './hooks';

function Component() {
    const count = useAppSelector(state => state.counter.value);
    const dispatch = useAppDispatch();
    // ...
}
```

## 🐻 Zustand

### 基本用法
```tsx
import {create} from 'zustand';

// 创建Store
interface CounterStore {
    count: number;
    increment: () => void;
    decrement: () => void;
    reset: () => void;
}

export const useCounterStore = create<CounterStore>((set) => ({
    count: 0,
    increment: () => set((state) => ({count: state.count + 1})),
    decrement: () => set((state) => ({count: state.count - 1})),
    reset: () => set({count: 0})
}));

// 使用
function Counter() {
    const {count, increment, decrement, reset} = useCounterStore();
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
            <button onClick={reset}>Reset</button>
        </div>
    );
}

// 选择性订阅（性能优化）
function Display() {
    const count = useCounterStore(state => state.count);
    // 只有count变化时才重渲染
    return <div>{count}</div>;
}
```

### 异步Actions
```javascript
interface UserStore {
    user: User | null;
    loading: boolean;
    error: string | null;
    fetchUser: (id: string) => Promise<void>;
}

export const useUserStore = create<UserStore>((set) => ({
    user: null,
    loading: false,
    error: null,
    
    fetchUser: async (id) => {
        set({loading: true, error: null});
        try {
            const response = await fetch(`/api/users/${id}`);
            const user = await response.json();
            set({user, loading: false});
        } catch (error) {
            set({error: error.message, loading: false});
        }
    }
}));
```

### 中间件
```javascript
import {create} from 'zustand';
import {persist, devtools} from 'zustand/middleware';

// 持久化
export const useStore = create(
    persist(
        (set) => ({
            count: 0,
            increment: () => set((state) => ({count: state.count + 1}))
        }),
        {
            name: 'counter-storage' // localStorage key
        }
    )
);

// DevTools
export const useStore = create(
    devtools(
        (set) => ({
            count: 0,
            increment: () => set((state) => ({count: state.count + 1}))
        }),
        {name: 'CounterStore'}
    )
);

// 组合中间件
export const useStore = create(
    devtools(
        persist(
            (set) => ({
                user: null,
                setUser: (user) => set({user})
            }),
            {name: 'user-storage'}
        ),
        {name: 'UserStore'}
    )
);
```

### Immer集成
```javascript
import {create} from 'zustand';
import {immer} from 'zustand/middleware/immer';

export const useStore = create(
    immer((set) => ({
        todos: [],
        addTodo: (text) => set((state) => {
            state.todos.push({id: Date.now(), text, done: false});
        }),
        toggleTodo: (id) => set((state) => {
            const todo = state.todos.find(t => t.id === id);
            if (todo) todo.done = !todo.done;
        })
    }))
);
```

## 🎯 状态管理对比

### 何时使用Context
- 主题、语言等全局配置
- 用户认证状态
- 简单的状态共享
- 不频繁更新的数据

### 何时使用Redux
- 复杂的状态逻辑
- 需要时间旅行调试
- 多个组件需要相同数据
- 需要中间件（如logger、saga）

### 何时使用Zustand
- 中小型应用
- 需要简洁的API
- 性能要求高
- 不需要复杂的调试工具

## 💡 最佳实践

### 1. 状态设计原则
```typescript
// ✅ 扁平化状态
interface State {
    users: {[id: string]: User};
    posts: {[id: string]: Post};
    currentUserId: string | null;
}

// ❌ 深层嵌套
interface State {
    user: {
        profile: {
            settings: {
                theme: string;
            }
        }
    }
}
```

### 2. 拆分状态
```typescript
// 按功能拆分
const useAuthStore = create(...);
const useCartStore = create(...);
const useUIStore = create(...);

// 而不是
const useGlobalStore = create(...); // 包含所有状态
```

### 3. 避免prop drilling
```jsx
// ❌ Prop drilling
<Parent>
    <Child1 theme={theme}>
        <Child2 theme={theme}>
            <Child3 theme={theme} />
        </Child2>
    </Child1>
</Parent>

// ✅ 使用Context/状态管理
<ThemeProvider>
    <Parent>
        <Child1>
            <Child2>
                <Child3 />
            </Child2>
        </Child1>
    </Parent>
</ThemeProvider>
```

### 4. 性能优化
```jsx
// Zustand选择性订阅
const count = useStore(state => state.count); // 只订阅count

// Redux使用Reselect
import {createSelector} from '@reduxjs/toolkit';

const selectTodos = (state) => state.todos;
const selectFilter = (state) => state.filter;

const selectFilteredTodos = createSelector(
    [selectTodos, selectFilter],
    (todos, filter) => todos.filter(todo => {
        if (filter === 'all') return true;
        if (filter === 'active') return !todo.done;
        if (filter === 'completed') return todo.done;
    })
);
```

## 📚 实践练习

### 练习1：Todo应用
使用Zustand实现：
- 添加、删除、切换Todo
- 过滤Todo（全部、已完成、未完成）
- 持久化到localStorage

### 练习2：购物车
使用Redux Toolkit实现：
- 添加商品到购物车
- 修改数量
- 计算总价
- 异步获取商品列表

### 练习3：多主题系统
使用Context实现：
- 切换主题
- 保存用户偏好
- 支持自定义主题

## 📚 参考资料
- [Redux Toolkit官方文档](https://redux-toolkit.js.org/)
- [Zustand文档](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [React Context文档](https://react.dev/reference/react/createContext)


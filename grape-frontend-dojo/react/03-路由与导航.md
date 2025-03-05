# 03-React Router路由与导航

## 📋 学习目标
- 掌握React Router v6核心概念
- 学习路由配置和导航
- 理解路由守卫和权限控制
- 掌握代码分割和懒加载

## 🛣️ React Router基础

### 安装
```bash
pnpm add react-router-dom
```

### 基本配置
```jsx
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/">首页</Link>
                <Link to="/about">关于</Link>
                <Link to="/users">用户</Link>
            </nav>
            
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/users" element={<Users />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
```

### 路由模式
```jsx
// BrowserRouter - HTML5 History API
import {BrowserRouter} from 'react-router-dom';
// URL: /about

// HashRouter - Hash模式
import {HashRouter} from 'react-router-dom';
// URL: /#/about

// MemoryRouter - 内存模式（测试用）
import {MemoryRouter} from 'react-router-dom';
```

## 🔗 导航

### Link组件
```jsx
import {Link, NavLink} from 'react-router-dom';

function Navigation() {
    return (
        <nav>
            {/* 基本链接 */}
            <Link to="/home">首页</Link>
            
            {/* 带state的链接 */}
            <Link to="/profile" state={{from: 'home'}}>
                个人资料
            </Link>
            
            {/* NavLink - 支持active样式 */}
            <NavLink 
                to="/about"
                className={({isActive}) => 
                    isActive ? 'active' : undefined
                }
            >
                关于
            </NavLink>
            
            {/* 自定义active样式 */}
            <NavLink
                to="/users"
                style={({isActive}) => ({
                    color: isActive ? 'red' : 'black',
                    fontWeight: isActive ? 'bold' : 'normal'
                })}
            >
                用户
            </NavLink>
        </nav>
    );
}
```

### 编程式导航
```jsx
import {useNavigate} from 'react-router-dom';

function LoginForm() {
    const navigate = useNavigate();
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        await login();
        
        // 导航到首页
        navigate('/');
        
        // 带参数导航
        navigate('/profile', {state: {from: 'login'}});
        
        // 替换当前历史记录
        navigate('/home', {replace: true});
        
        // 后退
        navigate(-1);
        
        // 前进
        navigate(1);
    };
    
    return <form onSubmit={handleSubmit}>...</form>;
}
```

## 📍 动态路由

### 路径参数
```jsx
// 路由配置
<Route path="/users/:id" element={<UserDetail />} />
<Route path="/posts/:postId/comments/:commentId" element={<Comment />} />

// 组件中获取参数
import {useParams} from 'react-router-dom';

function UserDetail() {
    const {id} = useParams();
    
    return <div>User ID: {id}</div>;
}

function Comment() {
    const {postId, commentId} = useParams();
    
    return (
        <div>
            Post: {postId}, Comment: {commentId}
        </div>
    );
}
```

### 查询参数
```jsx
import {useSearchParams} from 'react-router-dom';

function SearchPage() {
    const [searchParams, setSearchParams] = useSearchParams();
    
    // 获取参数
    const query = searchParams.get('q');
    const page = searchParams.get('page') || '1';
    
    // 设置参数
    const handleSearch = (newQuery) => {
        setSearchParams({q: newQuery, page: '1'});
    };
    
    const nextPage = () => {
        setSearchParams({
            q: query,
            page: String(Number(page) + 1)
        });
    };
    
    return (
        <div>
            <p>Search: {query}, Page: {page}</p>
            <button onClick={nextPage}>Next Page</button>
        </div>
    );
}

// URL: /search?q=react&page=2
```

## 🗂️ 嵌套路由

### 基本嵌套
```jsx
<Routes>
    <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="users" element={<Users />}>
            <Route index element={<UserList />} />
            <Route path=":id" element={<UserDetail />} />
            <Route path="new" element={<NewUser />} />
        </Route>
    </Route>
</Routes>

// Layout组件
import {Outlet} from 'react-router-dom';

function Layout() {
    return (
        <div>
            <header>Header</header>
            <main>
                <Outlet /> {/* 子路由渲染位置 */}
            </main>
            <footer>Footer</footer>
        </div>
    );
}

// Users组件
function Users() {
    return (
        <div>
            <h1>Users</h1>
            <Outlet /> {/* UserList或UserDetail渲染这里 */}
        </div>
    );
}
```

### 相对路径
```jsx
function Users() {
    return (
        <div>
            <nav>
                {/* 相对路径 */}
                <Link to="">All Users</Link>
                <Link to="new">New User</Link>
                
                {/* 绝对路径 */}
                <Link to="/users">Users</Link>
            </nav>
            <Outlet />
        </div>
    );
}
```

## 🔐 路由守卫

### 受保护路由
```jsx
import {Navigate, useLocation} from 'react-router-dom';

function PrivateRoute({children}) {
    const isAuthenticated = useAuth();
    const location = useLocation();
    
    if (!isAuthenticated) {
        // 跳转到登录，保存当前位置
        return <Navigate to="/login" state={{from: location}} replace />;
    }
    
    return children;
}

// 使用
<Routes>
    <Route path="/login" element={<Login />} />
    <Route 
        path="/dashboard" 
        element={
            <PrivateRoute>
                <Dashboard />
            </PrivateRoute>
        } 
    />
</Routes>

// 或者使用Layout包裹
<Route element={<PrivateRoute><Layout /></PrivateRoute>}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/profile" element={<Profile />} />
</Route>
```

### 角色权限控制
```jsx
function RoleRoute({children, allowedRoles}) {
    const {user} = useAuth();
    const location = useLocation();
    
    if (!user) {
        return <Navigate to="/login" state={{from: location}} />;
    }
    
    if (!allowedRoles.includes(user.role)) {
        return <Navigate to="/unauthorized" />;
    }
    
    return children;
}

// 使用
<Route 
    path="/admin" 
    element={
        <RoleRoute allowedRoles={['admin']}>
            <AdminPanel />
        </RoleRoute>
    } 
/>
```

## ⚡ 代码分割

### 路由级懒加载
```jsx
import {lazy, Suspense} from 'react';
import {Routes, Route} from 'react-router-dom';

// 懒加载组件
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Users = lazy(() => import('./pages/Users'));

function App() {
    return (
        <Suspense fallback={<Loading />}>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/users/*" element={<Users />} />
            </Routes>
        </Suspense>
    );
}

// Loading组件
function Loading() {
    return <div>Loading...</div>;
}
```

### 预加载
```jsx
import {lazy} from 'react';

const About = lazy(() => import('./pages/About'));

function Navigation() {
    // 鼠标悬停时预加载
    const handleMouseEnter = () => {
        import('./pages/About');
    };
    
    return (
        <Link 
            to="/about" 
            onMouseEnter={handleMouseEnter}
        >
            About
        </Link>
    );
}
```

## 🔄 数据加载

### Loader（React Router v6.4+）
```jsx
import {createBrowserRouter, RouterProvider, useLoaderData} from 'react-router-dom';

// 定义loader
async function userLoader({params}) {
    const response = await fetch(`/api/users/${params.id}`);
    if (!response.ok) {
        throw new Response('Not Found', {status: 404});
    }
    return response.json();
}

// 创建路由
const router = createBrowserRouter([
    {
        path: '/users/:id',
        element: <UserDetail />,
        loader: userLoader,
        errorElement: <ErrorPage />
    }
]);

// 组件中使用
function UserDetail() {
    const user = useLoaderData();
    
    return <div>{user.name}</div>;
}

// App
function App() {
    return <RouterProvider router={router} />;
}
```

### Action（表单处理）
```jsx
async function createUserAction({request}) {
    const formData = await request.formData();
    const user = {
        name: formData.get('name'),
        email: formData.get('email')
    };
    
    const response = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(user)
    });
    
    return redirect('/users');
}

const router = createBrowserRouter([
    {
        path: '/users/new',
        element: <NewUser />,
        action: createUserAction
    }
]);

// 组件中使用
import {Form} from 'react-router-dom';

function NewUser() {
    return (
        <Form method="post">
            <input name="name" />
            <input name="email" type="email" />
            <button type="submit">Create</button>
        </Form>
    );
}
```

## 🎯 实战案例

### 完整的路由配置
```jsx
import {createBrowserRouter, RouterProvider} from 'react-router-dom';

const router = createBrowserRouter([
    {
        path: '/',
        element: <Layout />,
        errorElement: <ErrorPage />,
        children: [
            {
                index: true,
                element: <Home />
            },
            {
                path: 'about',
                element: <About />
            },
            {
                path: 'users',
                children: [
                    {
                        index: true,
                        element: <UserList />,
                        loader: usersLoader
                    },
                    {
                        path: ':id',
                        element: <UserDetail />,
                        loader: userLoader
                    },
                    {
                        path: 'new',
                        element: <NewUser />,
                        action: createUserAction
                    },
                    {
                        path: ':id/edit',
                        element: <EditUser />,
                        loader: userLoader,
                        action: updateUserAction
                    }
                ]
            },
            {
                path: 'dashboard',
                element: (
                    <PrivateRoute>
                        <Dashboard />
                    </PrivateRoute>
                )
            }
        ]
    }
]);

function App() {
    return <RouterProvider router={router} />;
}
```

## 💡 最佳实践

### 1. 路由配置集中管理
```jsx
// routes.jsx
export const routes = [
    {path: '/', element: <Home />},
    {path: '/about', element: <About />},
    {path: '/users/:id', element: <UserDetail />}
];

// App.jsx
import {routes} from './routes';

function App() {
    return (
        <Routes>
            {routes.map(route => (
                <Route key={route.path} {...route} />
            ))}
        </Routes>
    );
}
```

### 2. 404处理
```jsx
<Routes>
    <Route path="/" element={<Home />} />
    <Route path="/about" element={<About />} />
    <Route path="*" element={<NotFound />} />
</Routes>
```

### 3. 面包屑导航
```jsx
import {useMatches} from 'react-router-dom';

function Breadcrumbs() {
    const matches = useMatches();
    
    return (
        <nav>
            {matches.map((match, index) => (
                <span key={match.pathname}>
                    <Link to={match.pathname}>
                        {match.handle?.crumb || match.pathname}
                    </Link>
                    {index < matches.length - 1 && ' > '}
                </span>
            ))}
        </nav>
    );
}
```

## 📚 实践练习

### 练习1：博客系统路由
实现以下路由：
- 文章列表：`/posts`
- 文章详情：`/posts/:id`
- 新建文章：`/posts/new`
- 编辑文章：`/posts/:id/edit`

### 练习2：权限管理
实现：
- 登录保护
- 角色权限控制
- 未授权页面

### 练习3：嵌套布局
实现：
- 多层嵌套路由
- 共享布局
- 面包屑导航

## 📚 参考资料
- [React Router官方文档](https://reactrouter.com/)
- [React Router v6迁移指南](https://reactrouter.com/en/main/upgrading/v5)


# 03-Vue 路由与状态管理

## 📋 学习目标
- 掌握Vue Router v4的使用
- 理解路由配置和导航守卫
- 学习Pinia状态管理
- 掌握路由懒加载和代码分割
- 了解状态持久化

## 🛣️ Vue Router 基础

### 安装和配置
```bash
npm install vue-router@4
```

```javascript
// router/index.js
import {createRouter, createWebHistory} from 'vue-router';
import Home from '../views/Home.vue';
import About from '../views/About.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
```

```javascript
// main.js
import {createApp} from 'vue';
import App from './App.vue';
import router from './router';

const app = createApp(App);
app.use(router);
app.mount('#app');
```

### 路由视图和链接
```vue
<!-- App.vue -->
<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
    
    <router-view />
  </div>
</template>
```

### 编程式导航
```vue
<script setup>
import {useRouter, useRoute} from 'vue-router';

const router = useRouter();
const route = useRoute();

// 导航到指定路由
function goToAbout() {
  router.push('/about');
  // 或
  router.push({name: 'About'});
  // 或带参数
  router.push({
    name: 'User',
    params: {id: 123}
  });
}

// 替换当前路由
function replaceRoute() {
  router.replace('/about');
}

// 前进/后退
function goBack() {
  router.go(-1);
}

function goForward() {
  router.go(1);
}

// 获取当前路由信息
console.log(route.path);
console.log(route.params);
console.log(route.query);
</script>
```

## 📍 路由配置

### 动态路由
```javascript
// router/index.js
const routes = [
  {
    path: '/user/:id',
    name: 'User',
    component: () => import('../views/User.vue')
  },
  {
    path: '/post/:id(\\d+)', // 只匹配数字
    name: 'Post',
    component: () => import('../views/Post.vue')
  },
  {
    path: '/files/:path(.*)', // 匹配所有路径
    name: 'Files',
    component: () => import('../views/Files.vue')
  }
];
```

```vue
<!-- User.vue -->
<template>
  <div>
    <h1>User ID: {{ $route.params.id }}</h1>
  </div>
</template>

<script setup>
import {useRoute} from 'vue-router';

const route = useRoute();
console.log(route.params.id);
</script>
```

### 嵌套路由
```javascript
// router/index.js
const routes = [
  {
    path: '/user/:id',
    component: () => import('../views/User.vue'),
    children: [
      {
        path: '',
        name: 'UserProfile',
        component: () => import('../views/UserProfile.vue')
      },
      {
        path: 'posts',
        name: 'UserPosts',
        component: () => import('../views/UserPosts.vue')
      },
      {
        path: 'settings',
        name: 'UserSettings',
        component: () => import('../views/UserSettings.vue')
      }
    ]
  }
];
```

```vue
<!-- User.vue -->
<template>
  <div class="user">
    <nav>
      <router-link :to="{name: 'UserProfile'}">Profile</router-link>
      <router-link :to="{name: 'UserPosts'}">Posts</router-link>
      <router-link :to="{name: 'UserSettings'}">Settings</router-link>
    </nav>
    
    <router-view />
  </div>
</template>
```

### 命名视图
```javascript
// router/index.js
const routes = [
  {
    path: '/',
    components: {
      default: Home,
      sidebar: Sidebar,
      header: Header
    }
  }
];
```

```vue
<template>
  <router-view />
  <router-view name="sidebar" />
  <router-view name="header" />
</template>
```

### 路由元信息
```javascript
// router/index.js
const routes = [
  {
    path: '/admin',
    component: () => import('../views/Admin.vue'),
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Admin Panel'
    }
  }
];
```

```vue
<script setup>
import {useRoute} from 'vue-router';

const route = useRoute();
console.log(route.meta.requiresAuth);
</script>
```

## 🛡️ 导航守卫

### 全局前置守卫
```javascript
// router/index.js
router.beforeEach((to, from, next) => {
  // 检查是否需要认证
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next({
      name: 'Login',
      query: {redirect: to.fullPath}
    });
  } else {
    next();
  }
});
```

### 全局解析守卫
```javascript
router.beforeResolve(async (to, from, next) => {
  // 在导航被确认之前，同时解析完所有异步组件
  if (to.meta.requiresData) {
    await fetchData();
  }
  next();
});
```

### 全局后置钩子
```javascript
router.afterEach((to, from) => {
  // 设置页面标题
  document.title = to.meta.title || 'My App';
  
  // 发送页面浏览统计
  analytics.track('page_view', {
    path: to.path,
    name: to.name
  });
});
```

### 路由独享守卫
```javascript
// router/index.js
const routes = [
  {
    path: '/admin',
    component: () => import('../views/Admin.vue'),
    beforeEnter: (to, from, next) => {
      if (hasPermission('admin')) {
        next();
      } else {
        next({name: 'Forbidden'});
      }
    }
  }
];
```

### 组件内守卫
```vue
<script setup>
import {onBeforeRouteLeave, onBeforeRouteUpdate} from 'vue-router';

// 离开守卫
onBeforeRouteLeave((to, from) => {
  const answer = window.confirm('确定要离开吗？');
  if (!answer) {
    return false; // 取消导航
  }
});

// 更新守卫
onBeforeRouteUpdate(async (to, from) => {
  // 路由参数变化时重新获取数据
  await fetchUserData(to.params.id);
});
</script>
```

## 🔄 路由懒加载

### 基础懒加载
```javascript
// router/index.js
const routes = [
  {
    path: '/home',
    component: () => import('../views/Home.vue')
  }
];
```

### 分组和预加载
```javascript
// router/index.js
const routes = [
  {
    path: '/admin',
    component: () => import(
      /* webpackChunkName: "admin" */
      '../views/Admin.vue'
    )
  },
  {
    path: '/user',
    component: () => import(
      /* webpackChunkName: "user" */
      '../views/User.vue'
    )
  }
];
```

### 条件加载
```javascript
// router/index.js
function lazyLoad(view) {
  return () => import(`../views/${view}.vue`);
}

const routes = [
  {
    path: '/home',
    component: lazyLoad('Home')
  }
];
```

## 🗄️ Pinia 状态管理

### 安装和配置
```bash
npm install pinia
```

```javascript
// main.js
import {createApp} from 'vue';
import {createPinia} from 'pinia';
import App from './App.vue';

const app = createApp(App);
app.use(createPinia());
app.mount('#app');
```

### 定义Store
```javascript
// stores/user.js
import {defineStore} from 'pinia';
import {ref, computed} from 'vue';

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null);
  const token = ref('');
  
  // Getters
  const isAuthenticated = computed(() => !!token.value);
  const userName = computed(() => user.value?.name || 'Guest');
  
  // Actions
  function login(credentials) {
    return api.login(credentials).then(response => {
      token.value = response.token;
      user.value = response.user;
    });
  }
  
  function logout() {
    token.value = '';
    user.value = null;
  }
  
  return {
    user,
    token,
    isAuthenticated,
    userName,
    login,
    logout
  };
});
```

### 使用Store
```vue
<script setup>
import {useUserStore} from '@/stores/user';
import {storeToRefs} from 'pinia';

const userStore = useUserStore();

// 直接解构会失去响应式
// const {user, token} = userStore; // ❌

// 使用storeToRefs保持响应式
const {user, token, isAuthenticated} = storeToRefs(userStore);

// Actions可以直接解构
const {login, logout} = userStore;

async function handleLogin() {
  await login({
    username: 'admin',
    password: '123456'
  });
}
</script>

<template>
  <div>
    <p v-if="isAuthenticated">Welcome, {{ user.name }}</p>
    <button @click="handleLogin">Login</button>
    <button @click="logout">Logout</button>
  </div>
</template>
```

### Options API风格
```javascript
// stores/counter.js
import {defineStore} from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter'
  }),
  
  getters: {
    doubleCount: (state) => state.count * 2,
    doubleCountPlusOne() {
      return this.doubleCount + 1;
    }
  },
  
  actions: {
    increment() {
      this.count++;
    },
    
    async fetchData() {
      const data = await api.getData();
      this.count = data.count;
    }
  }
});
```

### Store组合
```javascript
// stores/cart.js
import {defineStore} from 'pinia';
import {useUserStore} from './user';

export const useCartStore = defineStore('cart', () => {
  const userStore = useUserStore();
  
  const items = ref([]);
  
  function addItem(product) {
    if (!userStore.isAuthenticated) {
      throw new Error('Please login first');
    }
    items.value.push(product);
  }
  
  return {
    items,
    addItem
  };
});
```

## 💾 状态持久化

### 使用pinia-plugin-persistedstate
```bash
npm install pinia-plugin-persistedstate
```

```javascript
// main.js
import {createPinia} from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
```

```javascript
// stores/user.js
export const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const token = ref('');
  
  return {
    user,
    token
  };
}, {
  persist: {
    key: 'user-store',
    storage: localStorage,
    paths: ['token'] // 只持久化token
  }
});
```

### 手动持久化
```javascript
// stores/user.js
export const useUserStore = defineStore('user', () => {
  const user = ref(
    JSON.parse(localStorage.getItem('user') || 'null')
  );
  const token = ref(
    localStorage.getItem('token') || ''
  );
  
  function saveToStorage() {
    localStorage.setItem('user', JSON.stringify(user.value));
    localStorage.setItem('token', token.value);
  }
  
  function login(credentials) {
    return api.login(credentials).then(response => {
      token.value = response.token;
      user.value = response.user;
      saveToStorage();
    });
  }
  
  return {
    user,
    token,
    login
  };
});
```

## 🔐 路由权限控制

### 权限守卫
```javascript
// router/index.js
import {useUserStore} from '@/stores/user';

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  
  // 检查认证
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({
      name: 'Login',
      query: {redirect: to.fullPath}
    });
    return;
  }
  
  // 检查角色
  if (to.meta.roles && !to.meta.roles.includes(userStore.user?.role)) {
    next({name: 'Forbidden'});
    return;
  }
  
  next();
});
```

### 动态路由
```javascript
// router/index.js
export function setupRouter() {
  const userStore = useUserStore();
  
  // 根据权限动态添加路由
  if (userStore.hasPermission('admin')) {
    router.addRoute({
      path: '/admin',
      component: () => import('../views/Admin.vue')
    });
  }
}
```

## 📝 实战示例

### 完整的用户认证流程
```javascript
// stores/auth.js
import {defineStore} from 'pinia';
import {ref} from 'vue';
import router from '@/router';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const token = ref(localStorage.getItem('token') || '');
  
  async function login(credentials) {
    try {
      const response = await api.login(credentials);
      token.value = response.token;
      user.value = response.user;
      localStorage.setItem('token', token.value);
      
      // 重定向到原页面或首页
      const redirect = router.currentRoute.value.query.redirect || '/';
      router.push(redirect);
    } catch (error) {
      throw error;
    }
  }
  
  function logout() {
    token.value = '';
    user.value = null;
    localStorage.removeItem('token');
    router.push('/login');
  }
  
  async function checkAuth() {
    if (!token.value) return false;
    
    try {
      const response = await api.getUser();
      user.value = response.user;
      return true;
    } catch (error) {
      logout();
      return false;
    }
  }
  
  return {
    user,
    token,
    login,
    logout,
    checkAuth
  };
});
```

### 购物车Store
```javascript
// stores/cart.js
import {defineStore} from 'pinia';
import {ref, computed} from 'vue';

export const useCartStore = defineStore('cart', () => {
  const items = ref([]);
  
  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => {
      return sum + item.price * item.quantity;
    }, 0);
  });
  
  const itemCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0);
  });
  
  function addItem(product) {
    const existingItem = items.value.find(item => item.id === product.id);
    
    if (existingItem) {
      existingItem.quantity++;
    } else {
      items.value.push({
        ...product,
        quantity: 1
      });
    }
  }
  
  function removeItem(productId) {
    const index = items.value.findIndex(item => item.id === productId);
    if (index > -1) {
      items.value.splice(index, 1);
    }
  }
  
  function updateQuantity(productId, quantity) {
    const item = items.value.find(item => item.id === productId);
    if (item) {
      item.quantity = quantity;
    }
  }
  
  function clearCart() {
    items.value = [];
  }
  
  return {
    items,
    totalPrice,
    itemCount,
    addItem,
    removeItem,
    updateQuantity,
    clearCart
  };
}, {
  persist: true
});
```

## 🎯 最佳实践

1. **路由懒加载**：使用动态导入减少初始包大小
2. **路由守卫**：统一处理权限和认证逻辑
3. **状态管理**：复杂状态使用Pinia，简单状态使用组件内状态
4. **状态持久化**：敏感数据加密存储，非敏感数据使用localStorage
5. **类型安全**：使用TypeScript定义路由和Store类型


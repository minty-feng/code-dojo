# 02-Vue 组件系统与通信

## 📋 学习目标
- 掌握Vue组件注册和使用
- 理解Props和Emit组件通信
- 学习插槽Slots的使用
- 掌握Provide/Inject跨层级通信
- 了解动态组件和异步组件

## 🧩 组件注册

### 全局注册
```javascript
// main.js
import {createApp} from 'vue';
import MyComponent from './MyComponent.vue';

const app = createApp({});
app.component('MyComponent', MyComponent);
app.mount('#app');
```

### 局部注册
```vue
<script setup>
import MyComponent from './MyComponent.vue';
import AnotherComponent from './AnotherComponent.vue';
</script>

<template>
  <MyComponent />
  <AnotherComponent />
</template>
```

### 自动导入组件
```javascript
// vite.config.js
import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';
import Components from 'unplugin-vue-components/vite';

export default defineConfig({
  plugins: [
    vue(),
    Components({
      dirs: ['src/components'],
      extensions: ['vue'],
      deep: true
    })
  ]
});
```

## 📤 Props 传递数据

### 基本用法
```vue
<!-- Parent.vue -->
<template>
  <ChildComponent 
    :title="title" 
    :count="count"
    :user="user"
  />
</template>

<script setup>
import {ref, reactive} from 'vue';
import ChildComponent from './ChildComponent.vue';

const title = ref('Hello Vue');
const count = ref(0);
const user = reactive({
  name: 'John',
  age: 30
});
</script>
```

```vue
<!-- ChildComponent.vue -->
<template>
  <div>
    <h2>{{ title }}</h2>
    <p>Count: {{ count }}</p>
    <p>User: {{ user.name }}, {{ user.age }}</p>
  </div>
</template>

<script setup>
// 定义Props
const props = defineProps({
  title: {
    type: String,
    required: true,
    default: 'Default Title'
  },
  count: {
    type: Number,
    default: 0
  },
  user: {
    type: Object,
    required: true
  }
});
</script>
```

### TypeScript类型定义
```vue
<script setup lang="ts">
interface User {
  name: string;
  age: number;
}

interface Props {
  title: string;
  count?: number;
  user: User;
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
});
</script>
```

### Props验证
```vue
<script setup>
defineProps({
  // 基础类型检查
  title: String,
  
  // 多种类型
  id: [String, Number],
  
  // 必填
  name: {
    type: String,
    required: true
  },
  
  // 默认值
  count: {
    type: Number,
    default: 0
  },
  
  // 对象/数组默认值
  user: {
    type: Object,
    default: () => ({name: 'Guest'})
  },
  
  // 自定义验证
  age: {
    type: Number,
    validator: (value) => {
      return value >= 0 && value <= 150;
    }
  }
});
</script>
```

## 📥 Emit 事件通信

### 基本用法
```vue
<!-- ChildComponent.vue -->
<template>
  <button @click="handleClick">Click Me</button>
  <input 
    v-model="inputValue" 
    @input="handleInput"
  />
</template>

<script setup>
import {ref} from 'vue';

const emit = defineEmits(['click', 'update', 'custom-event']);

const inputValue = ref('');

function handleClick() {
  emit('click', 'button clicked');
}

function handleInput() {
  emit('update', inputValue.value);
  emit('custom-event', {
    type: 'input',
    value: inputValue.value
  });
}
</script>
```

```vue
<!-- Parent.vue -->
<template>
  <ChildComponent 
    @click="handleChildClick"
    @update="handleUpdate"
    @custom-event="handleCustom"
  />
</template>

<script setup>
function handleChildClick(message) {
  console.log(message);
}

function handleUpdate(value) {
  console.log('Updated:', value);
}

function handleCustom(event) {
  console.log('Custom event:', event);
}
</script>
```

### TypeScript类型定义
```vue
<script setup lang="ts">
interface Emits {
  (e: 'click', message: string): void;
  (e: 'update', value: string): void;
  (e: 'custom-event', payload: {type: string; value: string}): void;
}

const emit = defineEmits<Emits>();
</script>
```

### v-model双向绑定
```vue
<!-- CustomInput.vue -->
<template>
  <input 
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script setup>
defineProps({
  modelValue: String
});

defineEmits(['update:modelValue']);
</script>
```

```vue
<!-- 使用 -->
<template>
  <CustomInput v-model="text" />
</template>

<script setup>
import {ref} from 'vue';
const text = ref('');
</script>
```

### 多个v-model
```vue
<!-- CustomForm.vue -->
<template>
  <input 
    :value="firstName"
    @input="$emit('update:firstName', $event.target.value)"
  />
  <input 
    :value="lastName"
    @input="$emit('update:lastName', $event.target.value)"
  />
</template>

<script setup>
defineProps({
  firstName: String,
  lastName: String
});

defineEmits(['update:firstName', 'update:lastName']);
</script>
```

```vue
<!-- 使用 -->
<template>
  <CustomForm 
    v-model:firstName="firstName"
    v-model:lastName="lastName"
  />
</template>
```

## 🎰 插槽 Slots

### 默认插槽
```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <div class="card-header">
      <slot name="header">Default Header</slot>
    </div>
    <div class="card-body">
      <slot>Default Content</slot>
    </div>
    <div class="card-footer">
      <slot name="footer">Default Footer</slot>
    </div>
  </div>
</template>
```

```vue
<!-- 使用 -->
<template>
  <Card>
    <template v-slot:header>
      <h2>Custom Header</h2>
    </template>
    
    <p>This is the main content</p>
    
    <template v-slot:footer>
      <button>Action</button>
    </template>
  </Card>
</template>
```

### 作用域插槽
```vue
<!-- List.vue -->
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      <slot :item="item" :index="index">
        {{ item.name }}
      </slot>
    </li>
  </ul>
</template>

<script setup>
defineProps({
  items: Array
});
</script>
```

```vue
<!-- 使用 -->
<template>
  <List :items="users">
    <template v-slot:default="{item, index}">
      <div>
        <strong>{{ index + 1 }}. {{ item.name }}</strong>
        <span>{{ item.email }}</span>
      </div>
    </template>
  </List>
</template>
```

### 具名作用域插槽
```vue
<!-- Table.vue -->
<template>
  <table>
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key">
          <slot name="header" :column="col">
            {{ col.label }}
          </slot>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in data" :key="row.id">
        <td v-for="col in columns" :key="col.key">
          <slot name="cell" :row="row" :column="col">
            {{ row[col.key] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
</template>
```

```vue
<!-- 使用 -->
<template>
  <Table :columns="columns" :data="users">
    <template v-slot:header="{column}">
      <span class="custom-header">{{ column.label }}</span>
    </template>
    
    <template v-slot:cell="{row, column}">
      <span v-if="column.key === 'status'">
        <Badge :type="row.status">{{ row.status }}</Badge>
      </span>
      <span v-else>{{ row[column.key] }}</span>
    </template>
  </Table>
</template>
```

## 🔄 Provide/Inject 跨层级通信

### 基本用法
```vue
<!-- App.vue -->
<template>
  <ParentComponent />
</template>

<script setup>
import {provide, ref} from 'vue';
import ParentComponent from './ParentComponent.vue';

const theme = ref('dark');
const user = ref({
  name: 'John',
  role: 'admin'
});

// 提供数据
provide('theme', theme);
provide('user', user);
provide('updateTheme', (newTheme) => {
  theme.value = newTheme;
});
</script>
```

```vue
<!-- DeepChild.vue -->
<template>
  <div :class="theme">
    <p>User: {{ user.name }}</p>
    <button @click="updateTheme('light')">Change Theme</button>
  </div>
</template>

<script setup>
import {inject} from 'vue';

// 注入数据
const theme = inject('theme', 'light'); // 默认值
const user = inject('user');
const updateTheme = inject('updateTheme');
</script>
```

### TypeScript类型定义
```vue
<script setup lang="ts">
interface User {
  name: string;
  role: string;
}

// 提供
const theme = ref<string>('dark');
const user = ref<User>({
  name: 'John',
  role: 'admin'
});

provide<string>('theme', theme);
provide<User>('user', user);
</script>
```

```vue
<script setup lang="ts">
// 注入
const theme = inject<string>('theme', 'light');
const user = inject<User>('user');
</script>
```

### 响应式Provide
```vue
<script setup>
import {provide, ref, computed, readonly} from 'vue';

const count = ref(0);
const doubleCount = computed(() => count.value * 2);

// 只读，防止子组件修改
provide('count', readonly(count));
provide('doubleCount', doubleCount);
provide('increment', () => {
  count.value++;
});
</script>
```

## 🔀 动态组件

### component动态组件
```vue
<template>
  <div>
    <button 
      v-for="tab in tabs" 
      :key="tab"
      @click="currentTab = tab"
    >
      {{ tab }}
    </button>
    
    <component :is="currentTab" />
  </div>
</template>

<script setup>
import {ref, shallowRef} from 'vue';
import Home from './Home.vue';
import About from './About.vue';
import Contact from './Contact.vue';

const tabs = ['Home', 'About', 'Contact'];
const currentTab = ref('Home');

// 使用shallowRef优化性能
const components = shallowRef({
  Home,
  About,
  Contact
});
</script>
```

### keep-alive缓存组件
```vue
<template>
  <keep-alive :include="['Home', 'About']">
    <component :is="currentTab" />
  </keep-alive>
</template>
```

```vue
<script setup>
import {onActivated, onDeactivated} from 'vue';

// 组件激活时调用
onActivated(() => {
  console.log('Component activated');
  // 恢复数据、重新请求等
});

// 组件失活时调用
onDeactivated(() => {
  console.log('Component deactivated');
  // 保存数据、清理定时器等
});
</script>
```

## ⚡ 异步组件

### defineAsyncComponent
```vue
<script setup>
import {defineAsyncComponent} from 'vue';

// 基础用法
const AsyncComponent = defineAsyncComponent(() => 
  import('./HeavyComponent.vue')
);

// 带加载状态
const AsyncComponentWithLoading = defineAsyncComponent({
  loader: () => import('./HeavyComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorComponent,
  delay: 200, // 延迟显示加载组件
  timeout: 3000 // 超时时间
});
</script>

<template>
  <Suspense>
    <template v-slot:default>
      <AsyncComponent />
    </template>
    <template v-slot:fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>
```

### 路由懒加载
```javascript
// router/index.js
import {createRouter, createWebHistory} from 'vue-router';

const routes = [
  {
    path: '/home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/about',
    component: () => import('../views/About.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});
```

## 🎯 组件通信总结

### 通信方式对比

| 方式 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| Props | 父子组件 | 简单直接、类型安全 | 只能向下传递 |
| Emit | 父子组件 | 事件驱动、解耦 | 只能向上传递 |
| Provide/Inject | 跨层级 | 避免逐层传递 | 难以追踪数据流 |
| EventBus | 任意组件 | 灵活 | 难以维护、不推荐 |
| Vuex/Pinia | 全局状态 | 集中管理、可追踪 | 增加复杂度 |

### 最佳实践

1. **优先使用Props和Emit**：简单场景使用父子组件通信
2. **跨层级使用Provide/Inject**：避免Props逐层传递
3. **全局状态使用Pinia**：复杂应用使用状态管理
4. **组件解耦**：使用事件和插槽提高组件复用性
5. **类型安全**：使用TypeScript定义Props和Emit类型

## 📝 实战示例

### 表单组件封装
```vue
<!-- FormField.vue -->
<template>
  <div class="form-field">
    <label v-if="label">{{ label }}</label>
    <input 
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="$emit('blur')"
    />
    <span v-if="error" class="error">{{ error }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  type: {
    type: String,
    default: 'text'
  },
  placeholder: String,
  modelValue: String,
  error: String
});

defineEmits(['update:modelValue', 'blur']);
</script>
```

```vue
<!-- 使用 -->
<template>
  <FormField
    v-model="username"
    label="用户名"
    placeholder="请输入用户名"
    :error="errors.username"
    @blur="validateUsername"
  />
</template>
```

### 列表组件封装
```vue
<!-- VirtualList.vue -->
<template>
  <div class="virtual-list" ref="containerRef">
    <div :style="{height: totalHeight + 'px'}">
      <div 
        v-for="item in visibleItems" 
        :key="item.id"
        :style="{transform: `translateY(${item.top}px)`}"
      >
        <slot :item="item.data" :index="item.index" />
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, onUnmounted} from 'vue';

const props = defineProps({
  items: Array,
  itemHeight: Number
});

const containerRef = ref(null);
const scrollTop = ref(0);

const visibleItems = computed(() => {
  const start = Math.floor(scrollTop.value / props.itemHeight);
  const end = start + Math.ceil(containerRef.value?.clientHeight / props.itemHeight);
  
  return props.items.slice(start, end).map((item, index) => ({
    ...item,
    index: start + index,
    top: (start + index) * props.itemHeight
  }));
});

const totalHeight = computed(() => props.items.length * props.itemHeight);

function handleScroll() {
  scrollTop.value = containerRef.value?.scrollTop || 0;
}

onMounted(() => {
  containerRef.value?.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  containerRef.value?.removeEventListener('scroll', handleScroll);
});
</script>
```


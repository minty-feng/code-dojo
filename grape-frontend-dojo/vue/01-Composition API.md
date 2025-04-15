# 01-Vue Composition API

## 📋 学习目标
- 掌握Composition API核心函数
- 理解响应式系统原理
- 学习组合式函数开发
- 掌握生命周期和副作用

## 🎯 setup函数

### 基本用法
```vue
<script>
import {ref, reactive} from 'vue';

export default {
    setup() {
        const count = ref(0);
        const user = reactive({
            name: 'John',
            age: 30
        });
        
        function increment() {
            count.value++;
        }
        
        return {
            count,
            user,
            increment
        };
    }
};
</script>

<template>
    <div>
        <p>Count: {{ count }}</p>
        <p>User: {{ user.name }}, {{ user.age }}</p>
        <button @click="increment">+1</button>
    </div>
</template>
```

### setup语法糖
```vue
<script setup>
import {ref, reactive} from 'vue';

const count = ref(0);
const user = reactive({
    name: 'John',
    age: 30
});

function increment() {
    count.value++;
}
</script>

<template>
    <div>
        <p>Count: {{ count }}</p>
        <button @click="increment">+1</button>
    </div>
</template>
```

## 📦 响应式核心

### ref
```javascript
import {ref} from 'vue';

// 基本类型
const count = ref(0);
console.log(count.value); // 0
count.value++;

// 对象（会自动转为reactive）
const user = ref({name: 'John'});
user.value.name = 'Jane';

// 数组
const list = ref([1, 2, 3]);
list.value.push(4);

// 模板中自动解包
// <p>{{ count }}</p>  不需要.value
```

### reactive
```javascript
import {reactive} from 'vue';

// 响应式对象
const state = reactive({
    count: 0,
    user: {
        name: 'John',
        age: 30
    }
});

state.count++; // 直接修改，不需要.value

// 响应式数组
const list = reactive([1, 2, 3]);
list.push(4);

// 响应式Map/Set
const map = reactive(new Map());
const set = reactive(new Set());
```

### ref vs reactive
```javascript
// ref：适合基本类型和单一值
const count = ref(0);
const name = ref('John');

// reactive：适合对象和复杂结构
const state = reactive({
    count: 0,
    name: 'John'
});

// 解构会失去响应性
const {count, name} = reactive({count: 0, name: 'John'}); // ❌
count++; // 不会触发更新

// 使用toRefs保持响应性
import {toRefs} from 'vue';
const state = reactive({count: 0, name: 'John'});
const {count, name} = toRefs(state); // ✅
count.value++; // 会触发更新
```

## 🔄 computed

### 基本用法
```vue
<script setup>
import {ref, computed} from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

// 只读computed
const fullName = computed(() => {
    return `${firstName.value} ${lastName.value}`;
});

// 可写computed
const fullName = computed({
    get() {
        return `${firstName.value} ${lastName.value}`;
    },
    set(value) {
        const parts = value.split(' ');
        firstName.value = parts[0];
        lastName.value = parts[1];
    }
});
</script>

<template>
    <div>
        <input v-model="firstName" />
        <input v-model="lastName" />
        <p>{{ fullName }}</p>
        <input v-model="fullName" />
    </div>
</template>
```

## 👁️ watch与watchEffect

### watch
```javascript
import {ref, watch} from 'vue';

const count = ref(0);

// 监听单个ref
watch(count, (newVal, oldVal) => {
    console.log(`Count: ${oldVal} -> ${newVal}`);
});

// 监听多个源
const name = ref('John');
const age = ref(30);

watch([name, age], ([newName, newAge], [oldName, oldAge]) => {
    console.log(`Name: ${oldName} -> ${newName}`);
    console.log(`Age: ${oldAge} -> ${newAge}`);
});

// 监听reactive对象
const state = reactive({count: 0});

watch(() => state.count, (newVal, oldVal) => {
    console.log(`Count: ${oldVal} -> ${newVal}`);
});

// 深度监听
watch(state, (newVal) => {
    console.log('State changed:', newVal);
}, {deep: true});

// 立即执行
watch(count, (val) => {
    console.log('Count:', val);
}, {immediate: true});
```

### watchEffect
```javascript
import {ref, watchEffect} from 'vue';

const count = ref(0);
const double = ref(0);

// 自动追踪依赖
watchEffect(() => {
    double.value = count.value * 2;
    console.log(`Count: ${count.value}, Double: ${double.value}`);
});

// 清理副作用
watchEffect((onCleanup) => {
    const timer = setInterval(() => {
        console.log('Tick');
    }, 1000);
    
    onCleanup(() => {
        clearInterval(timer);
    });
});

// 停止监听
const stop = watchEffect(() => {
    console.log(count.value);
});

// 手动停止
stop();
```

## 🔁 生命周期

### Composition API生命周期
```vue
<script setup>
import {
    onBeforeMount,
    onMounted,
    onBeforeUpdate,
    onUpdated,
    onBeforeUnmount,
    onUnmounted
} from 'vue';

onBeforeMount(() => {
    console.log('组件挂载前');
});

onMounted(() => {
    console.log('组件挂载后');
    // DOM已渲染，可以访问DOM
});

onBeforeUpdate(() => {
    console.log('组件更新前');
});

onUpdated(() => {
    console.log('组件更新后');
});

onBeforeUnmount(() => {
    console.log('组件卸载前');
});

onUnmounted(() => {
    console.log('组件卸载后');
    // 清理定时器、事件监听等
});
</script>
```

## 🎁 Provide/Inject

### 基本用法
```vue
<!-- 父组件 -->
<script setup>
import {provide, ref} from 'vue';

const theme = ref('dark');
const updateTheme = (newTheme) => {
    theme.value = newTheme;
};

provide('theme', theme);
provide('updateTheme', updateTheme);
</script>

<!-- 子组件 -->
<script setup>
import {inject} from 'vue';

const theme = inject('theme');
const updateTheme = inject('updateTheme');
</script>

<template>
    <div :class="theme">
        <button @click="updateTheme('light')">Light</button>
        <button @click="updateTheme('dark')">Dark</button>
    </div>
</template>
```

### 类型化Provide/Inject
```typescript
import {InjectionKey, provide, inject} from 'vue';

interface Theme {
    primary: string;
    secondary: string;
}

const themeKey: InjectionKey<Theme> = Symbol('theme');

// 提供
provide(themeKey, {
    primary: '#007bff',
    secondary: '#6c757d'
});

// 注入
const theme = inject(themeKey);
// theme的类型为Theme | undefined
```

## 🛠️ 组合式函数

### 基本组合式函数
```javascript
// useCounter.js
import {ref} from 'vue';

export function useCounter(initialValue = 0) {
    const count = ref(initialValue);
    
    function increment() {
        count.value++;
    }
    
    function decrement() {
        count.value--;
    }
    
    function reset() {
        count.value = initialValue;
    }
    
    return {
        count,
        increment,
        decrement,
        reset
    };
}

// 使用
<script setup>
import {useCounter} from './useCounter';

const {count, increment, decrement, reset} = useCounter(10);
</script>

<template>
    <div>
        <p>{{ count }}</p>
        <button @click="increment">+</button>
        <button @click="decrement">-</button>
        <button @click="reset">Reset</button>
    </div>
</template>
```

### 实用组合式函数
```javascript
// useFetch.js
import {ref} from 'vue';

export function useFetch(url) {
    const data = ref(null);
    const error = ref(null);
    const loading = ref(true);
    
    async function fetchData() {
        loading.value = true;
        try {
            const response = await fetch(url);
            data.value = await response.json();
            error.value = null;
        } catch (err) {
            error.value = err;
        } finally {
            loading.value = false;
        }
    }
    
    fetchData();
    
    return {data, error, loading, refetch: fetchData};
}

// useLocalStorage.js
import {ref, watch} from 'vue';

export function useLocalStorage(key, defaultValue) {
    const value = ref(defaultValue);
    
    // 初始化
    const stored = localStorage.getItem(key);
    if (stored) {
        value.value = JSON.parse(stored);
    }
    
    // 监听变化
    watch(value, (newVal) => {
        localStorage.setItem(key, JSON.stringify(newVal));
    }, {deep: true});
    
    return value;
}

// useDebounce.js
import {ref, watch} from 'vue';

export function useDebounce(value, delay = 500) {
    const debouncedValue = ref(value.value);
    
    watch(value, (newVal) => {
        const timer = setTimeout(() => {
            debouncedValue.value = newVal;
        }, delay);
        
        return () => clearTimeout(timer);
    });
    
    return debouncedValue;
}
```

## 📱 Props和Emits

### defineProps
```vue
<script setup>
// 基本用法
const props = defineProps({
    title: String,
    count: {
        type: Number,
        default: 0
    },
    user: {
        type: Object,
        required: true
    }
});

// TypeScript类型
interface Props {
    title: string;
    count?: number;
    user: {
        name: string;
        age: number;
    };
}

const props = defineProps<Props>();

// 默认值（TypeScript）
const props = withDefaults(defineProps<Props>(), {
    count: 0
});
</script>
```

### defineEmits
```vue
<script setup>
// 基本用法
const emit = defineEmits(['update', 'delete']);

function handleClick() {
    emit('update', {id: 1});
}

// TypeScript类型
const emit = defineEmits<{
    update: [id: number];
    delete: [id: number, confirmed: boolean];
}>();

emit('update', 123);
emit('delete', 456, true);
</script>

<template>
    <button @click="handleClick">Update</button>
</template>
```

## 🎯 defineExpose

### 暴露组件方法
```vue
<script setup>
import {ref} from 'vue';

const count = ref(0);
const internalValue = ref('secret');

function increment() {
    count.value++;
}

// 只暴露特定属性和方法
defineExpose({
    count,
    increment
});
// internalValue不会暴露
</script>

<!-- 父组件 -->
<script setup>
import {ref} from 'vue';
import ChildComponent from './ChildComponent.vue';

const childRef = ref();

function callChild() {
    childRef.value.increment();
    console.log(childRef.value.count);
}
</script>

<template>
    <ChildComponent ref="childRef" />
    <button @click="callChild">Call Child</button>
</template>
```

## 📚 实践练习

### 练习1：组合式函数
实现以下组合式函数：
- useToggle：布尔值切换
- useArray：数组操作
- useMouse：鼠标位置追踪

### 练习2：表单管理
使用Composition API实现：
- 表单验证
- 错误提示
- 提交处理

### 练习3：数据获取
创建可复用的数据获取Hook：
- 加载状态
- 错误处理
- 重新请求
- 缓存

## 📚 参考资料
- [Vue 3官方文档](https://cn.vuejs.org/)
- [Composition API RFC](https://github.com/vuejs/rfcs/blob/master/active-rfcs/0013-composition-api.md)
- [VueUse](https://vueuse.org/) - 组合式函数集合


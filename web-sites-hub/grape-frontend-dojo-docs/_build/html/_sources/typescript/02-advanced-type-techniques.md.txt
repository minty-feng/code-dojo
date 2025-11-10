# 02-TypeScript高级类型技巧

## 📋 学习目标
- 掌握高级类型操作
- 理解类型体操技巧
- 学习实用工具类型
- 掌握类型编程模式

## 🎯 条件类型

### 基本条件类型
```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false

// 实际应用：提取数组元素类型
type Flatten<T> = T extends Array<infer U> ? U : T;

type Str = Flatten<string[]>;   // string
type Num = Flatten<number>;     // number

// 提取Promise类型
type Awaited<T> = T extends Promise<infer U> ? U : T;

type Result = Awaited<Promise<string>>;  // string
```

### 分布式条件类型
```typescript
type ToArray<T> = T extends any ? T[] : never;

type StrOrNumArray = ToArray<string | number>;
// string[] | number[]

// 实际应用：过滤类型
type Filter<T, U> = T extends U ? T : never;

type Numbers = Filter<string | number | boolean, number>;
// number

// 排除类型
type Exclude<T, U> = T extends U ? never : T;

type NonString = Exclude<string | number | boolean, string>;
// number | boolean
```

### 递归条件类型
```typescript
// 深度只读
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object
        ? DeepReadonly<T[P]>
        : T[P];
};

interface Nested {
    a: {
        b: {
            c: number;
        };
    };
}

type ReadonlyNested = DeepReadonly<Nested>;
// 所有层级都是readonly

// 深度可选
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object
        ? DeepPartial<T[P]>
        : T[P];
};
```

## 🔧 映射类型

### 基本映射
```typescript
// Readonly
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

// Partial
type Partial<T> = {
    [P in keyof T]?: T[P];
};

// Required
type Required<T> = {
    [P in keyof T]-?: T[P];  // -?移除可选
};

// Pick
type Pick<T, K extends keyof T> = {
    [P in K]: T[P];
};

// Omit
type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
```

### 键重映射
```typescript
// 添加前缀
type Getters<T> = {
    [P in keyof T as `get${Capitalize<string & P>}`]: () => T[P];
};

interface Person {
    name: string;
    age: number;
}

type PersonGetters = Getters<Person>;
// {
//     getName: () => string;
//     getAge: () => number;
// }

// 过滤键
type RemoveId<T> = {
    [P in keyof T as P extends 'id' ? never : P]: T[P];
};

interface User {
    id: number;
    name: string;
    email: string;
}

type UserWithoutId = RemoveId<User>;
// {
//     name: string;
//     email: string;
// }
```

### 条件映射
```typescript
// 将函数类型转为Promise类型
type Promisify<T> = {
    [P in keyof T]: T[P] extends (...args: any[]) => any
        ? (...args: Parameters<T[P]>) => Promise<ReturnType<T[P]>>
        : T[P];
};

interface API {
    getUser(id: number): User;
    saveUser(user: User): void;
}

type AsyncAPI = Promisify<API>;
// {
//     getUser: (id: number) => Promise<User>;
//     saveUser: (user: User) => Promise<void>;
// }
```

## 🎨 模板字面量类型

### 基本用法
```typescript
type World = "world";
type Greeting = `hello ${World}`;  // "hello world"

// 联合类型
type Color = "red" | "blue" | "green";
type Quantity = "one" | "two";
type ColoredQuantity = `${Quantity} ${Color}`;
// "one red" | "one blue" | "one green" | "two red" | "two blue" | "two green"
```

### 内置字符串操作
```typescript
type Uppercase<S extends string> = intrinsic;
type Lowercase<S extends string> = intrinsic;
type Capitalize<S extends string> = intrinsic;
type Uncapitalize<S extends string> = intrinsic;

type Upper = Uppercase<"hello">;      // "HELLO"
type Lower = Lowercase<"HELLO">;      // "hello"
type Cap = Capitalize<"hello">;       // "Hello"
type Uncap = Uncapitalize<"Hello">;   // "hello"
```

### 实际应用
```typescript
// CSS属性类型
type CSSProperties = {
    [P in keyof CSSStyleDeclaration as `--${string & P}`]?: string;
};

// 事件处理器
type EventHandlers<T> = {
    [P in keyof T as `on${Capitalize<string & P>}`]?: (value: T[P]) => void;
};

interface FormData {
    username: string;
    password: string;
}

type FormHandlers = EventHandlers<FormData>;
// {
//     onUsername?: (value: string) => void;
//     onPassword?: (value: string) => void;
// }

// 路径类型
type Path<T> = {
    [K in keyof T]: T[K] extends object
        ? `${string & K}` | `${string & K}.${Path<T[K]>}`
        : `${string & K}`;
}[keyof T];

interface Config {
    server: {
        host: string;
        port: number;
    };
    database: {
        url: string;
    };
}

type ConfigPath = Path<Config>;
// "server" | "server.host" | "server.port" | "database" | "database.url"
```

## 🔍 infer关键字

### 提取类型
```typescript
// 提取函数参数类型
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

function add(a: number, b: number): number {
    return a + b;
}

type AddParams = Parameters<typeof add>;  // [number, number]

// 提取函数返回类型
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type AddReturn = ReturnType<typeof add>;  // number

// 提取Promise类型
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type User = UnwrapPromise<Promise<{name: string}>>;  // {name: string}

// 提取数组元素类型
type ElementType<T> = T extends (infer U)[] ? U : never;

type Numbers = ElementType<number[]>;  // number
```

### 复杂提取
```typescript
// 提取构造函数参数
type ConstructorParameters<T> = T extends new (...args: infer P) => any ? P : never;

class MyClass {
    constructor(name: string, age: number) {}
}

type MyClassParams = ConstructorParameters<typeof MyClass>;  // [string, number]

// 提取实例类型
type InstanceType<T> = T extends new (...args: any[]) => infer R ? R : never;

type MyInstance = InstanceType<typeof MyClass>;  // MyClass
```

## 🎯 实用工具类型

### Record和Extract
```typescript
// Record：创建对象类型
type Record<K extends keyof any, T> = {
    [P in K]: T;
};

type PageInfo = Record<'home' | 'about' | 'contact', {title: string; url: string}>;
// {
//     home: {title: string; url: string};
//     about: {title: string; url: string};
//     contact: {title: string; url: string};
// }

// Extract：提取匹配的类型
type Extract<T, U> = T extends U ? T : never;

type T0 = Extract<"a" | "b" | "c", "a" | "f">;  // "a"
type T1 = Extract<string | number | (() => void), Function>;  // () => void
```

### NonNullable和Required
```typescript
// NonNullable：移除null和undefined
type NonNullable<T> = T extends null | undefined ? never : T;

type T0 = NonNullable<string | null | undefined>;  // string

// Required：移除可选
type Required<T> = {
    [P in keyof T]-?: T[P];
};

interface Props {
    name?: string;
    age?: number;
}

type RequiredProps = Required<Props>;
// {
//     name: string;
//     age: number;
// }
```

### 自定义工具类型
```typescript
// Nullable：添加null
type Nullable<T> = T | null;

// Mutable：移除readonly
type Mutable<T> = {
    -readonly [P in keyof T]: T[P];
};

// ValueOf：获取对象值类型
type ValueOf<T> = T[keyof T];

interface User {
    id: number;
    name: string;
    active: boolean;
}

type UserValue = ValueOf<User>;  // number | string | boolean

// DeepMutable：深度移除readonly
type DeepMutable<T> = {
    -readonly [P in keyof T]: T[P] extends object
        ? DeepMutable<T[P]>
        : T[P];
};

// Prettify：展开类型
type Prettify<T> = {
    [K in keyof T]: T[K];
} & {};

type Merged = Prettify<{a: number} & {b: string}>;
// {
//     a: number;
//     b: string;
// }
```

## 🚀 高级模式

### 函数重载
```typescript
function createLabel(id: number): IdLabel;
function createLabel(name: string): NameLabel;
function createLabel(nameOrId: string | number): IdLabel | NameLabel {
    if (typeof nameOrId === "number") {
        return {id: nameOrId};
    } else {
        return {name: nameOrId};
    }
}

// 类型安全的重载
type CreateLabel = {
    (id: number): IdLabel;
    (name: string): NameLabel;
};

const createLabel: CreateLabel = (nameOrId: string | number) => {
    // 实现
};
```

### 类型断言函数
```typescript
function isString(value: unknown): value is string {
    return typeof value === 'string';
}

function process(value: unknown) {
    if (isString(value)) {
        // 这里value的类型是string
        value.toUpperCase();
    }
}

// 断言函数
function assertIsString(value: unknown): asserts value is string {
    if (typeof value !== 'string') {
        throw new Error('Not a string');
    }
}

function processString(value: unknown) {
    assertIsString(value);
    // 这里value的类型是string
    return value.toUpperCase();
}
```

### 品牌类型
```typescript
// 名义类型（Nominal Typing）
type Brand<K, T> = K & {__brand: T};

type USD = Brand<number, 'USD'>;
type EUR = Brand<number, 'EUR'>;

function createUSD(amount: number): USD {
    return amount as USD;
}

function createEUR(amount: number): EUR {
    return amount as EUR;
}

const usd = createUSD(100);
const eur = createEUR(100);

// 类型错误：不能将EUR赋值给USD
// const mixed: USD = eur;

// 实际应用：ID类型
type UserId = Brand<string, 'UserId'>;
type ProductId = Brand<string, 'ProductId'>;

function getUser(id: UserId) {}
function getProduct(id: ProductId) {}

const userId = 'user-123' as UserId;
const productId = 'product-456' as ProductId;

getUser(userId);  // ✅
// getUser(productId);  // ❌ 类型错误
```

## 📚 实践练习

### 练习1：实现工具类型
实现以下工具类型：
- `DeepPick<T, K>` - 深度选择
- `DeepOmit<T, K>` - 深度排除
- `Merge<A, B>` - 合并类型

### 练习2：类型体操
实现：
- 元组转联合类型
- 联合类型转交叉类型
- 字符串反转类型

### 练习3：实际应用
为React组件创建：
- Props类型推导
- 事件处理器类型
- 样式Props类型

## 💡 最佳实践

1. **合理使用泛型约束**
```typescript
// ❌ 过于宽松
function merge<T, U>(a: T, b: U) {
    return {...a, ...b};
}

// ✅ 添加约束
function merge<T extends object, U extends object>(a: T, b: U) {
    return {...a, ...b};
}
```

2. **避免any**
```typescript
// ❌ 使用any
function log(value: any) {
    console.log(value);
}

// ✅ 使用unknown
function log(value: unknown) {
    console.log(value);
}
```

3. **使用类型推断**
```typescript
// ❌ 重复声明
const numbers: number[] = [1, 2, 3];

// ✅ 类型推断
const numbers = [1, 2, 3];  // number[]
```

## 📚 参考资料
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Type Challenges](https://github.com/type-challenges/type-challenges)
- [TypeScript深度指南](https://basarat.gitbook.io/typescript/)


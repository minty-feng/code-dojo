# 01-TypeScript类型系统

## 📋 学习目标
- 掌握TypeScript基本类型
- 理解类型推断和类型注解
- 学习高级类型特性
- 掌握类型守卫和类型断言

## 🔢 基本类型

### 原始类型
```typescript
// 数字
let age: number = 30;
let price: number = 99.99;
let hex: number = 0xf00d;

// 字符串
let name: string = 'John';
let message: string = `Hello, ${name}`;

// 布尔
let isDone: boolean = false;

// null和undefined
let u: undefined = undefined;
let n: null = null;

// 可选链
type User = {
    name: string;
    age?: number;  // 可选属性
};
```

### 数组和元组
```typescript
// 数组
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ['a', 'b', 'c'];

// 元组
let tuple: [string, number] = ['hello', 10];
let rgb: [number, number, number] = [255, 0, 0];

// 只读数组
let readonly: ReadonlyArray<number> = [1, 2, 3];
// readonly.push(4); // 报错

// 只读元组
let point: readonly [number, number] = [10, 20];
```

### any、unknown、never
```typescript
// any：任意类型（失去类型检查）
let anything: any = 'hello';
anything = 123;
anything.foo(); // 不报错，但可能运行时出错

// unknown：类型安全的any
let value: unknown = 'hello';
// value.toUpperCase(); // 报错
if (typeof value === 'string') {
    value.toUpperCase(); // 正确
}

// never：永不存在的值
function error(message: string): never {
    throw new Error(message);
}

function infiniteLoop(): never {
    while (true) {}
}

// void：没有返回值
function log(message: string): void {
    console.log(message);
}
```

### 枚举
```typescript
// 数字枚举
enum Direction {
    Up,      // 0
    Down,    // 1
    Left,    // 2
    Right    // 3
}

let dir: Direction = Direction.Up;

// 字符串枚举
enum Color {
    Red = 'RED',
    Green = 'GREEN',
    Blue = 'BLUE'
}

// 常量枚举（编译时内联）
const enum Size {
    Small,
    Medium,
    Large
}

let size: Size = Size.Medium;
```

## 📦 接口与类型别名

### 接口定义
```typescript
// 基本接口
interface User {
    name: string;
    age: number;
    email?: string;  // 可选
    readonly id: number;  // 只读
}

const user: User = {
    id: 1,
    name: 'John',
    age: 30
};

// user.id = 2; // 报错：只读属性

// 索引签名
interface StringMap {
    [key: string]: string;
}

const map: StringMap = {
    name: 'John',
    city: 'Beijing'
};

// 函数类型
interface SearchFunc {
    (source: string, sub: string): boolean;
}

const search: SearchFunc = (src, sub) => {
    return src.includes(sub);
};

// 类接口
interface ClockInterface {
    currentTime: Date;
    setTime(d: Date): void;
}

class Clock implements ClockInterface {
    currentTime: Date = new Date();
    setTime(d: Date) {
        this.currentTime = d;
    }
}
```

### 类型别名
```typescript
// 基本类型别名
type ID = string | number;
type Point = {
    x: number;
    y: number;
};

// 联合类型
type Status = 'pending' | 'success' | 'error';

// 交叉类型
type Name = {name: string};
type Age = {age: number};
type Person = Name & Age;

const person: Person = {
    name: 'John',
    age: 30
};

// 函数类型
type AddFn = (a: number, b: number) => number;

const add: AddFn = (a, b) => a + b;
```

### Interface vs Type
```typescript
// interface可以扩展
interface Animal {
    name: string;
}

interface Dog extends Animal {
    bark(): void;
}

// interface可以合并
interface Window {
    title: string;
}

interface Window {
    width: number;
}

// type可以使用联合类型
type StringOrNumber = string | number;

// type可以使用映射类型
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};
```

## 🎯 泛型

### 泛型函数
```typescript
// 基本泛型
function identity<T>(arg: T): T {
    return arg;
}

let output1 = identity<string>('hello');
let output2 = identity(123); // 类型推断

// 泛型数组
function getFirst<T>(arr: T[]): T | undefined {
    return arr[0];
}

const first = getFirst([1, 2, 3]); // number | undefined

// 多个类型参数
function pair<T, U>(first: T, second: U): [T, U] {
    return [first, second];
}

const p = pair('hello', 123); // [string, number]
```

### 泛型接口
```typescript
interface GenericIdentity<T> {
    (arg: T): T;
}

function identity<T>(arg: T): T {
    return arg;
}

let myIdentity: GenericIdentity<number> = identity;

// 泛型类
class GenericNumber<T> {
    zeroValue: T;
    add: (x: T, y: T) => T;
    
    constructor(zero: T, addFn: (x: T, y: T) => T) {
        this.zeroValue = zero;
        this.add = addFn;
    }
}

const myNumber = new GenericNumber<number>(0, (x, y) => x + y);
```

### 泛型约束
```typescript
// 约束泛型
interface Lengthwise {
    length: number;
}

function logLength<T extends Lengthwise>(arg: T): T {
    console.log(arg.length);
    return arg;
}

logLength('hello');  // 正确
logLength([1, 2, 3]); // 正确
// logLength(123); // 报错：number没有length属性

// keyof约束
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const obj = {a: 1, b: 2, c: 3};
getProperty(obj, 'a'); // 正确
// getProperty(obj, 'd'); // 报错
```

## 🔍 类型守卫

### typeof
```typescript
function padLeft(value: string, padding: string | number) {
    if (typeof padding === 'number') {
        return ' '.repeat(padding) + value;
    }
    return padding + value;
}
```

### instanceof
```typescript
class Bird {
    fly() {
        console.log('flying');
    }
}

class Fish {
    swim() {
        console.log('swimming');
    }
}

function move(pet: Bird | Fish) {
    if (pet instanceof Bird) {
        pet.fly();
    } else {
        pet.swim();
    }
}
```

### 自定义类型守卫
```typescript
interface Cat {
    meow(): void;
}

interface Dog {
    bark(): void;
}

function isCat(pet: Cat | Dog): pet is Cat {
    return (pet as Cat).meow !== undefined;
}

function makeSound(pet: Cat | Dog) {
    if (isCat(pet)) {
        pet.meow();
    } else {
        pet.bark();
    }
}
```

## 🎨 高级类型

### 联合类型
```typescript
type StringOrNumber = string | number;

function format(value: StringOrNumber): string {
    if (typeof value === 'string') {
        return value.toUpperCase();
    }
    return value.toString();
}
```

### 交叉类型
```typescript
interface Colorful {
    color: string;
}

interface Circle {
    radius: number;
}

type ColorfulCircle = Colorful & Circle;

const cc: ColorfulCircle = {
    color: 'red',
    radius: 10
};
```

### 条件类型
```typescript
type IsString<T> = T extends string ? 'yes' : 'no';

type A = IsString<string>; // 'yes'
type B = IsString<number>; // 'no'

// 实际应用
type Flatten<T> = T extends Array<infer U> ? U : T;

type Str = Flatten<string[]>; // string
type Num = Flatten<number>;   // number
```

### 映射类型
```typescript
// 基本映射
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

type Optional<T> = {
    [P in keyof T]?: T[P];
};

// 使用
interface Todo {
    title: string;
    completed: boolean;
}

type ReadonlyTodo = Readonly<Todo>;
type PartialTodo = Optional<Todo>;
```

### 工具类型
```typescript
// Partial：所有属性可选
type PartialUser = Partial<User>;

// Required：所有属性必填
type RequiredUser = Required<User>;

// Readonly：所有属性只读
type ReadonlyUser = Readonly<User>;

// Pick：选择部分属性
type UserPreview = Pick<User, 'name' | 'email'>;

// Omit：排除部分属性
type UserWithoutId = Omit<User, 'id'>;

// Record：构造对象类型
type PageInfo = Record<'home' | 'about' | 'contact', {title: string}>;

// Exclude：排除联合类型
type T0 = Exclude<'a' | 'b' | 'c', 'a'>; // 'b' | 'c'

// Extract：提取联合类型
type T1 = Extract<'a' | 'b' | 'c', 'a' | 'f'>; // 'a'

// NonNullable：排除null和undefined
type T2 = NonNullable<string | null | undefined>; // string

// ReturnType：获取函数返回类型
type T3 = ReturnType<() => string>; // string
```

## 💡 实践技巧

### 类型断言
```typescript
// as语法
const input = document.getElementById('input') as HTMLInputElement;
input.value = 'hello';

// 双重断言
const value = 'hello' as unknown as number; // 不推荐

// 非空断言
function getName(user?: User) {
    return user!.name; // 断言user不为null/undefined
}
```

### 类型收窄
```typescript
function process(value: string | null) {
    // 类型守卫
    if (value !== null) {
        console.log(value.toUpperCase());
    }
    
    // 短路运算
    value && console.log(value.length);
    
    // 空值合并
    const name = value ?? 'Guest';
}
```

## 📚 实践练习

### 练习1：类型定义
为以下场景定义类型：
- API响应数据
- 表单配置
- 路由配置

### 练习2：泛型工具
实现工具类型：
- DeepPartial：深度可选
- DeepReadonly：深度只读
- ValueOf：获取对象值类型

### 练习3：类型守卫
实现类型守卫函数：
- isArray
- isObject
- isPromise

## 📚 参考资料
- [TypeScript官方文档](https://www.typescriptlang.org/docs/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)


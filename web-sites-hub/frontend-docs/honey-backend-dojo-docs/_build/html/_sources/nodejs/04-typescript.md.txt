# 04-TypeScript集成

TypeScript是JavaScript的超集，添加静态类型系统。编译期错误检查，提升代码质量和开发效率。

## TypeScript基础

### 安装配置

```bash
npm install -D typescript @types/node @types/express
npx tsc --init
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 基本类型

```typescript
// 基础类型
let name: string = 'Alice';
let age: number = 25;
let isActive: boolean = true;

// 数组
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ['Alice', 'Bob'];

// 元组
let tuple: [string, number] = ['Alice', 25];

// 枚举
enum Role {
    Admin = 'ADMIN',
    User = 'USER',
    Guest = 'GUEST'
}

let role: Role = Role.Admin;

// any（避免使用）
let anything: any = 'string';
anything = 123;

// unknown（更安全）
let uncertain: unknown = 'string';
// uncertain.toUpperCase();  // 错误
if (typeof uncertain === 'string') {
    uncertain.toUpperCase();  // OK
}

// void
function log(message: string): void {
    console.log(message);
}

// never（永不返回）
function throwError(message: string): never {
    throw new Error(message);
}

// null和undefined
let nullable: string | null = null;
let optional: string | undefined = undefined;
```

### 接口和类型别名

```typescript
// 接口
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;  // 可选
    readonly createdAt: Date;  // 只读
}

const user: User = {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    createdAt: new Date()
};

// 类型别名
type ID = string | number;
type UserRole = 'admin' | 'user' | 'guest';  // 联合类型

type Point = {
    x: number;
    y: number;
};

// 交叉类型
type Admin = User & {
    permissions: string[];
};

// 泛型
interface Response<T> {
    data: T;
    status: number;
    message: string;
}

const response: Response<User> = {
    data: user,
    status: 200,
    message: 'Success'
};
```

## Express + TypeScript

### 类型定义

```typescript
import express, { Request, Response, NextFunction } from 'express';

const app = express();

// 基本路由
app.get('/users', (req: Request, res: Response) => {
    res.json({ users: [] });
});

// 自定义Request类型
interface AuthRequest extends Request {
    user?: {
        id: number;
        email: string;
    };
}

app.get('/profile', (req: AuthRequest, res: Response) => {
    res.json({ user: req.user });
});

// 泛型参数
app.get<{ id: string }>('/users/:id', (req, res) => {
    const { id } = req.params;  // 类型：string
    res.json({ id });
});

// 中间件类型
const authMiddleware = (
    req: AuthRequest,
    res: Response,
    next: NextFunction
): void => {
    const token = req.headers.authorization;
    if (!token) {
        res.status(401).json({ error: 'Unauthorized' });
        return;
    }
    next();
};
```

### 控制器

```typescript
// controllers/userController.ts
import { Request, Response, NextFunction } from 'express';
import { User, IUser } from '../models/User';

export const getUsers = async (
    req: Request,
    res: Response,
    next: NextFunction
): Promise<void> => {
    try {
        const users = await User.find();
        res.json(users);
    } catch (err) {
        next(err);
    }
};

export const createUser = async (
    req: Request,
    res: Response,
    next: NextFunction
): Promise<void> => {
    try {
        const user: IUser = await User.create(req.body);
        res.status(201).json(user);
    } catch (err) {
        next(err);
    }
};
```

### 模型定义

```typescript
// models/User.ts
import mongoose, { Document, Schema } from 'mongoose';

export interface IUser extends Document {
    name: string;
    email: string;
    age: number;
    createdAt: Date;
}

const userSchema = new Schema<IUser>({
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    age: { type: Number, default: 0 },
    createdAt: { type: Date, default: Date.now }
});

export const User = mongoose.model<IUser>('User', userSchema);
```

## 类型守卫

### 类型断言

```typescript
// as断言
const value: unknown = 'hello';
const strLength = (value as string).length;

// 非空断言
function getValue(id?: number): number {
    return id!;  // 断言id非undefined
}

// 类型守卫函数
function isString(value: unknown): value is string {
    return typeof value === 'string';
}

if (isString(value)) {
    console.log(value.toUpperCase());  // value确定是string
}

// 自定义类型守卫
interface User {
    type: 'user';
    name: string;
}

interface Admin {
    type: 'admin';
    name: string;
    permissions: string[];
}

type Person = User | Admin;

function isAdmin(person: Person): person is Admin {
    return person.type === 'admin';
}

function printPerson(person: Person) {
    if (isAdmin(person)) {
        console.log(person.permissions);  // person是Admin
    } else {
        console.log(person.name);  // person是User
    }
}
```

## 装饰器

### 启用装饰器

```json
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

### 常用装饰器

```typescript
// 类装饰器
function Controller(path: string) {
    return function<T extends { new(...args: any[]): {} }>(constructor: T) {
        return class extends constructor {
            basePath = path;
        };
    };
}

@Controller('/api/users')
class UserController {
    // ...
}

// 方法装饰器
function Log(target: any, key: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = function(...args: any[]) {
        console.log(`调用 ${key}，参数:`, args);
        const result = originalMethod.apply(this, args);
        console.log(`${key} 返回:`, result);
        return result;
    };
    
    return descriptor;
}

class Calculator {
    @Log
    add(a: number, b: number): number {
        return a + b;
    }
}

// 参数装饰器
function Required(target: any, key: string, index: number) {
    // 标记必需参数
}

class Service {
    method(@Required param: string) {
        // ...
    }
}
```

## 常用工具类型

```typescript
// Partial：所有属性可选
interface User {
    id: number;
    name: string;
    email: string;
}

type PartialUser = Partial<User>;
// { id?: number; name?: string; email?: string; }

// Required：所有属性必需
type RequiredUser = Required<PartialUser>;

// Readonly：所有属性只读
type ReadonlyUser = Readonly<User>;

// Pick：选择部分属性
type UserPreview = Pick<User, 'id' | 'name'>;
// { id: number; name: string; }

// Omit：排除部分属性
type UserWithoutId = Omit<User, 'id'>;
// { name: string; email: string; }

// Record：键值对类型
type UserMap = Record<number, User>;
// { [key: number]: User }

// Exclude：排除类型
type T1 = Exclude<'a' | 'b' | 'c', 'a'>;  // 'b' | 'c'

// Extract：提取类型
type T2 = Extract<'a' | 'b' | 'c', 'a' | 'b'>;  // 'a' | 'b'

// NonNullable：排除null和undefined
type T3 = NonNullable<string | null | undefined>;  // string

// ReturnType：获取函数返回类型
function getUser() {
    return { id: 1, name: 'Alice' };
}

type User = ReturnType<typeof getUser>;
// { id: number; name: string; }
```

## 配置开发环境

### ts-node开发

```bash
npm install -D ts-node nodemon

# nodemon.json
{
  "watch": ["src"],
  "ext": "ts",
  "exec": "ts-node src/index.ts"
}

# package.json
{
  "scripts": {
    "dev": "nodemon",
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

### ESLint + TypeScript

```bash
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

```json
// .eslintrc.json
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

## 最佳实践

### 类型定义

```typescript
// ✓ 明确类型
function add(a: number, b: number): number {
    return a + b;
}

// ❌ 避免any
function process(data: any) {  // 丧失类型检查
    return data.value;
}

// ✓ 使用泛型
function process<T>(data: T): T {
    return data;
}

// ✓ 使用unknown替代any
function process(data: unknown) {
    if (typeof data === 'object' && data !== null) {
        // 类型收窄
    }
}
```

### 类型收窄

```typescript
function printValue(value: string | number) {
    if (typeof value === 'string') {
        console.log(value.toUpperCase());  // value是string
    } else {
        console.log(value.toFixed(2));  // value是number
    }
}

// in操作符
interface Cat {
    meow: () => void;
}

interface Dog {
    bark: () => void;
}

function makeSound(animal: Cat | Dog) {
    if ('meow' in animal) {
        animal.meow();  // animal是Cat
    } else {
        animal.bark();  // animal是Dog
    }
}
```

### 严格模式

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,  // 启用所有严格检查
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

**核心：** TypeScript通过静态类型系统在编译期发现错误，提升代码质量和可维护性。合理使用类型定义和泛型是关键。


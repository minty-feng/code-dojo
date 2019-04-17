# C++ 基础语法

## 数据类型

C++ 是强类型语言，每个变量必须声明类型。类型决定了内存占用、取值范围和支持的操作。

### 整型

整型用于存储整数。根据内存大小和是否支持负数选择合适的类型。

```cpp
char        // 1字节, -128 ~ 127
short       // 2字节, -32768 ~ 32767
int         // 4字节, -2147483648 ~ 2147483647（常用）
long        // 4/8字节（平台相关）
long long   // 8字节（大整数）
unsigned    // 无符号修饰符，范围翻倍但只能表示非负数
```

**类型选择建议**：优先使用 `int`，需要大范围时用 `long long`，明确非负时用 `unsigned`。

### 浮点型

浮点型用于存储小数。精度和内存成正比。

```cpp
float       // 4字节, 7位精度（节省内存）
double      // 8字节, 15位精度（默认选择）
long double // 更高精度（科学计算）
```

**注意**：浮点数存在精度误差，避免用 `==` 比较，改用误差范围判断。

### 其他类型

```cpp
bool        // true/false，逻辑值
char        // 单字符，ASCII 编码
void        // 无类型，用于函数返回值
```

### 类型大小查询

`sizeof` 运算符返回类型或变量占用的字节数，编译期计算。

```cpp
sizeof(int)      // 通常为 4
sizeof(double)   // 通常为 8
sizeof(variable) // 变量占用的字节数
```

## 变量和常量

### 变量声明

变量是存储数据的命名内存空间。声明变量时应初始化，避免未定义行为。

```cpp
int age = 25;           // 声明并初始化
int height;             // 仅声明（值未定义，危险）
auto x = 10;            // 自动类型推导（C++11）
int a{5};              // 列表初始化（推荐，防止窄化转换）
```

**命名规范**：使用有意义的名称（`studentAge` 而非 `a`），驼峰命名法，避免关键字。

### 常量

常量的值不可修改，编译器会强制检查。使用常量可提高代码可读性和安全性。

```cpp
const int MAX = 100;    // 运行时常量，可用变量初始化
constexpr int SIZE = 10; // 编译时常量，必须编译期可计算
#define PI 3.14159      // 宏常量（不推荐，无类型检查）
```

**最佳实践**：优先使用 `constexpr`，其次 `const`，避免 `#define`。

### 作用域

作用域决定变量的可见范围和生命周期。内层作用域可访问外层变量，但反之不行。

```cpp
int global = 1;         // 全局作用域，程序结束时销毁

void func() {
    int local = 2;      // 局部作用域，函数结束时销毁
    {
        int block = 3;  // 块作用域，出块时销毁
        // 可访问 global, local, block
    }
    // 可访问 global, local，但不可访问 block
}
```

**原则**：尽量缩小变量作用域，减少命名冲突和意外修改。

## 运算符

运算符是执行特定操作的符号。掌握运算符优先级和结合性是编写正确表达式的基础。

### 算术运算符

基本数学运算。注意整数除法会截断小数部分。

```cpp
+  -  *  /  %          // 加减乘除取模（%仅用于整数）
++  --                 // 自增自减（前置：先改后用，后置：先用后改）
+=  -=  *=  /=  %=     // 复合赋值（x += 5 等价于 x = x + 5）
```

**示例**：`5 / 2` 结果为 `2`（整数除法），`5.0 / 2` 结果为 `2.5`（浮点除法）。

### 关系运算符

比较运算，返回布尔值。

```cpp
==  !=  >  <  >=  <=   // 相等、不等、大于、小于、大于等于、小于等于
```

**注意**：赋值是 `=`，比较是 `==`，初学者易混淆。

### 逻辑运算符

组合条件判断，支持短路求值。

```cpp
&&  ||  !              // 与（都为真）、或（至少一个为真）、非（取反）
```

**短路求值**：`a && b` 中若 `a` 为假则不计算 `b`；`a || b` 中若 `a` 为真则不计算 `b`。

### 位运算符

直接操作二进制位，常用于底层编程、标志位管理和性能优化。

```cpp
&   |   ^   ~          // 按位与、或、异或、取反
<<  >>                 // 左移（乘2^n）、右移（除2^n）
```

**应用**：`x & 1` 判断奇偶，`x << 1` 快速乘2，`x | (1 << n)` 设置第n位。

### 运算符优先级（高到低）

优先级决定运算顺序，不确定时用括号明确。

1. `()` - 括号
2. `!  ~  ++  --` - 一元运算符
3. `*  /  %` - 乘除取模
4. `+  -` - 加减
5. `<<  >>` - 移位
6. `<  <=  >  >=` - 关系
7. `==  !=` - 相等
8. `&` - 按位与
9. `^` - 按位异或
10. `|` - 按位或
11. `&&` - 逻辑与
12. `||` - 逻辑或
13. `=  +=  -=` - 赋值

**建议**：复杂表达式加括号，提高可读性。

## 控制结构

控制结构决定程序执行流程。合理使用可提高代码可读性和效率。

### 条件语句

根据条件执行不同代码分支。

```cpp
// if-else：基本条件判断
if (condition) {
    // condition为真时执行
} else if (condition2) {
    // condition为假且condition2为真时执行
} else {
    // 以上都为假时执行
}

// switch：多分支选择（值必须是整型或枚举）
switch (value) {
    case 1:
        // value == 1
        break;      // 必须break，否则继续执行下一case
    case 2:
        // value == 2
        break;
    default:
        // 其他情况
}

// 三元运算符：简洁的条件表达式
result = (condition) ? value1 : value2;  // condition真取value1，假取value2
```

**技巧**：`switch` 比多个 `if-else` 更高效；三元运算符适合简单赋值。

### 循环语句

重复执行代码块，直到条件不满足。

```cpp
// for循环：次数确定时使用
for (int i = 0; i < n; ++i) {  // 初始化; 条件; 更新
    // 循环体
}

// while循环：次数不确定时使用
while (condition) {
    // 先判断条件，再执行
}

// do-while循环：至少执行一次
do {
    // 先执行，再判断条件
} while (condition);

// 范围for（C++11）：遍历容器
for (auto& item : container) {  // auto自动推导类型，&避免拷贝
    // 处理item
}
```

**选择**：已知次数用 `for`，未知次数用 `while`，需要先执行用 `do-while`。

### 跳转语句

改变正常的顺序执行流程。

```cpp
break;      // 跳出当前循环或switch
continue;   // 跳过本次循环剩余部分，进入下次迭代
return;     // 结束函数并返回值
goto label; // 跳转到标签（破坏结构化，强烈不推荐）
```

**最佳实践**：能用 `break/continue` 就不用 `goto`；多层循环跳出可用标志变量。

## 函数

函数是可重用的代码块，封装特定功能。良好的函数设计可提高代码复用性和可维护性。

### 函数定义

函数由返回类型、名称、参数列表和函数体组成。

```cpp
// 声明（告诉编译器函数存在）
int add(int a, int b);

// 定义（实现函数功能）
int add(int a, int b) {
    return a + b;
}

// 内联函数：建议编译器在调用处展开，减少函数调用开销
inline int square(int x) {
    return x * x;  // 适合短小、频繁调用的函数
}

// 默认参数：调用时可省略
void print(int value, int base = 10);  // 默认十进制
print(100);      // 使用默认参数
print(100, 16);  // 使用十六进制

// 函数重载：同名函数，不同参数
int max(int a, int b);
double max(double a, double b);  // 根据参数类型选择
```

**注意**：默认参数只能在声明中指定，且从右往左连续。

### 参数传递

不同传递方式影响性能和语义。

```cpp
// 值传递：复制参数，函数内修改不影响原变量
void func1(int x);  // 小对象适用

// 引用传递：直接操作原变量，无拷贝开销
void func2(int& x);  // x的修改会影响实参

// 指针传递：传递地址，可传NULL表示可选
void func3(int* x);  // 需判空：if (x) {...}

// const引用：只读访问，避免拷贝（推荐）
void func4(const int& x);  // 大对象传参的最佳选择
```

**选择建议**：小对象（如int）值传递，大对象（如string）const引用，需修改用非const引用。

### Lambda表达式（C++11）

匿名函数，常用于算法和回调。语法：`[捕获] (参数) { 函数体 }`

```cpp
// 基本Lambda
auto add = [](int a, int b) { return a + b; };
int result = add(3, 4);  // 7

// 捕获外部变量
int x = 10;
auto lambda1 = [x](int y) { return x + y; };     // 值捕获（只读）
auto lambda2 = [&x](int y) { x += y; };          // 引用捕获（可修改）
auto lambda3 = [=](int y) { return x + y; };     // 捕获所有（值）
auto lambda4 = [&](int y) { x += y; };           // 捕获所有（引用）
```

**应用**：`std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });`

## 数组

数组是固定大小的连续内存块，存储相同类型的元素。索引从0开始。

### 静态数组

编译期确定大小，分配在栈上，访问快但大小固定。

```cpp
int arr[5] = {1, 2, 3, 4, 5};   // 完整初始化
int arr2[] = {1, 2, 3};          // 自动推导大小为3
int arr3[5] = {};                // 全部初始化为0
int arr4[5] = {1, 2};            // {1, 2, 0, 0, 0}，未指定的元素为0

// 多维数组：本质是数组的数组
int matrix[3][4];                // 3行4列，matrix[i][j]访问
int cube[2][3][4];               // 三维数组
```

**注意**：C++不检查数组越界，`arr[100]` 可能导致段错误或未定义行为。

### 数组操作

```cpp
arr[0] = 10;                     // 访问/修改第0个元素
int size = sizeof(arr) / sizeof(arr[0]); // 计算元素个数

// 遍历数组
for (int i = 0; i < size; ++i) {
    cout << arr[i] << " ";
}

// C++11范围for（更简洁）
for (int val : arr) {
    cout << val << " ";
}
```

**限制**：数组传参会退化为指针，丢失大小信息。推荐使用 `std::array`（C++11）或 `std::vector`。

## 字符串

C++提供两种字符串：C风格（字符数组）和C++风格（string类），推荐使用后者。

### C风格字符串

以空字符 `'\0'` 结尾的字符数组，操作需小心缓冲区溢出。

```cpp
char str[] = "Hello";            // 自动添加'\0'，实际占6字节
char* ptr = "World";             // 字符串字面量，不可修改

// 常用函数（#include <cstring>）
strlen(str);                     // 长度（不含'\0'）
strcpy(dest, src);               // 复制（需确保dest足够大）
strcat(dest, src);               // 连接（需确保dest足够大）
strcmp(str1, str2);              // 比较（0相等，<0小于，>0大于）
```

**风险**：不检查长度，易溢出。现代C++避免使用。

### C++字符串（推荐）

`std::string` 类自动管理内存，提供丰富操作，安全便捷。

```cpp
#include <string>

string s1 = "Hello";
string s2 = s1 + " World";       // 连接（运算符重载）
s1.length();                     // 长度（size()等价）
s1.empty();                      // 是否为空
s1.substr(0, 5);                 // 提取子串[0,5)
s1.find("llo");                  // 查找位置（未找到返回string::npos）
s1.replace(0, 2, "He");          // 替换[0,2)为"He"
s1[0] = 'h';                     // 索引访问
s1.c_str();                      // 转C风格字符串
```

**优势**：自动扩容、安全、支持运算符、STL兼容。

## 指针和引用

指针和引用是C++中操作内存地址的机制，是C++强大但也易出错的特性。

### 指针

指针存储变量的内存地址，通过地址间接访问变量。

```cpp
int value = 42;
int* ptr = &value;               // &取地址运算符
int deref = *ptr;                // *解引用运算符，获取指针指向的值

// 空指针：不指向任何对象
int* p = nullptr;                // C++11推荐，类型安全
int* p2 = NULL;                  // 传统方式，实际是0
int* p3 = 0;                     // 更古老的方式

// 指针运算：适用于数组
int arr[5];
int* p = arr;                    // 数组名自动转换为指向首元素的指针
p++;                             // 移动到下一个元素（+sizeof(int)字节）
p += 2;                          // 跳过2个元素
int diff = p - arr;              // 指针差=元素个数
```

**危险**：野指针（未初始化）、悬空指针（对象已销毁）、内存泄漏（忘记释放）。

### 引用

引用是变量的别名，必须初始化且不可重新绑定，比指针安全。

```cpp
int value = 42;
int& ref = value;                // 引用必须初始化，之后ref就是value的别名
ref = 100;                       // 修改ref等同于修改value

// const引用：只读引用，常用于函数参数
const int& cref = value;         // 不能通过cref修改value
cref = 200;                      // 错误！const引用不可修改
```

**区别**：指针可空可重新赋值，引用非空不可重新绑定；引用更安全，指针更灵活。

### 动态内存

运行时分配内存，用于不确定大小或需要长生命周期的数据。

```cpp
// 分配
int* p = new int(42);            // 分配单个int并初始化为42
int* arr = new int[10];          // 分配10个int的数组

// 释放（必须与分配配对）
delete p;                        // 释放单个对象
delete[] arr;                    // 释放数组（必须用delete[]）

// 智能指针（C++11，强烈推荐）：自动管理内存，避免泄漏
#include <memory>
unique_ptr<int> up(new int(42));     // 独占所有权
shared_ptr<int> sp = make_shared<int>(42);  // 共享所有权（引用计数）
weak_ptr<int> wp = sp;               // 弱引用，不增加引用计数
```

**原则**：优先使用智能指针，避免手动 `new/delete`；RAII（资源获取即初始化）模式。

## 结构体和联合体

### 结构体

结构体将不同类型的数据组合成一个自定义类型，是面向对象的基础。

```cpp
struct Point {
    int x;      // 成员变量
    int y;
};

Point p = {10, 20};  // 初始化
p.x = 30;            // 访问成员
Point p2 = p;        // 结构体可直接赋值（浅拷贝）
```

**用途**：表示复合数据，如坐标、日期、学生信息等。C++中 `struct` 和 `class` 几乎相同，仅默认访问权限不同。

### 联合体

联合体的所有成员共享同一块内存，同一时刻只能使用一个成员，节省空间。

```cpp
union Data {
    int i;      // 所有成员共享内存
    float f;    // 修改一个会影响其他
    char c;
};

Data d;
d.i = 10;       // 使用int成员
d.f = 3.14;     // 现在int成员的值无效
```

**注意**：联合体大小等于最大成员的大小。常用于类型转换或节省内存。

### 枚举

枚举定义一组命名的整数常量，提高代码可读性。

```cpp
enum Color { RED, GREEN, BLUE };  // 默认值：0, 1, 2
Color c = RED;
int val = c;                      // 可隐式转换为int

// 强类型枚举（C++11，推荐）：类型安全，不可隐式转换
enum class Status { OK, ERROR, PENDING };
Status s = Status::OK;            // 必须加作用域
// int x = s;                     // 错误！不可隐式转换
int x = static_cast<int>(s);     // 必须显式转换
```

**优势**：增强可读性，避免魔法数字；强类型枚举防止命名冲突和隐式转换。

## 类型转换

类型转换将一种类型的值转换为另一种类型。C++提供隐式和显式两种方式。

### 隐式转换

编译器自动执行的转换，通常是安全的（小转大、整数转浮点）。

```cpp
int i = 10;
double d = i;                    // int自动转double，无精度损失
char c = 'A';
int x = c;                       // char转int，值为ASCII码
```

**风险**：大转小（如 `int` 转 `char`）可能丢失数据，编译器可能警告。

### 显式转换

程序员明确指定的转换，用于不安全或非标准的转换。

```cpp
// C风格（不推荐，无类型检查）
int i = (int)3.14;               // 截断为3
char* p = (char*)&i;             // 危险的类型双关

// C++风格（推荐，明确意图，编译器检查）
static_cast<int>(3.14);          // 标准类型转换，编译期检查
const_cast<int&>(constVar);      // 移除const属性（谨慎使用）
dynamic_cast<Derived*>(basePtr); // 运行时多态类型转换（需RTTI）
reinterpret_cast<int*>(&f);      // 重新解释位模式（底层操作）
```

**选择**：优先 `static_cast`，需要运行时检查用 `dynamic_cast`，避免 `reinterpret_cast`。

## 预处理器

预处理器在编译前处理源代码，进行文本替换和条件编译。

### 宏定义

宏是文本替换，不进行类型检查，现代C++推荐用 `const` 和 `inline` 函数代替。

```cpp
#define PI 3.14159               // 常量宏（推荐用const）
#define MAX(a, b) ((a) > (b) ? (a) : (b))  // 函数宏（推荐用inline或模板）
#define SQUARE(x) ((x) * (x))    // 注意加括号，防止优先级问题
```

**陷阱**：`SQUARE(x+1)` 展开为 `((x+1) * (x+1))`，可能导致副作用重复计算。

### 条件编译

根据条件选择性地编译代码，常用于平台差异、调试代码、头文件保护。

```cpp
// 调试代码
#ifdef DEBUG
    cout << "Debug info" << endl;
#endif

// 头文件保护（防止重复包含）
#ifndef HEADER_H
#define HEADER_H
    // 头文件内容
#endif

// 平台相关代码
#if defined(WIN32)
    // Windows特定代码
#elif defined(__linux__)
    // Linux特定代码
#else
    // 其他平台
#endif
```

### 预定义宏

编译器提供的内置宏，用于调试和诊断。

```cpp
__FILE__    // 当前文件名（字符串）
__LINE__    // 当前行号（整数）
__DATE__    // 编译日期（字符串："Mmm dd yyyy"）
__TIME__    // 编译时间（字符串："hh:mm:ss"）
__func__    // 当前函数名（C++11，字符串）
```

**示例**：`cerr << "Error at " << __FILE__ << ":" << __LINE__ << endl;`

## 命名空间

命名空间解决命名冲突问题，将代码逻辑分组。标准库在 `std` 命名空间中。

```cpp
// 定义命名空间
namespace MySpace {
    int value = 10;
    void func() { /* ... */ }
}

// 使用（需要完全限定名）
MySpace::value;
MySpace::func();

// using声明：引入特定名称
using MySpace::value;
value = 20;  // 现在可直接使用

// using指令：引入整个命名空间（不推荐，污染全局）
using namespace MySpace;
value = 30;
func();

// 嵌套命名空间（C++17简化语法）
namespace A::B::C {  // 等价于 namespace A { namespace B { namespace C { }}}
    int x;
}
```

**建议**：头文件避免 `using namespace`；实现文件可局部使用；明确指定 `std::` 提高可读性。

## 输入输出

C++提供流式输入输出，类型安全且可扩展。

### 标准输入输出

`cin`/`cout` 分别用于输入输出，位于 `<iostream>` 头文件。

```cpp
#include <iostream>
using namespace std;

// 输出
cout << "Hello" << endl;         // endl刷新缓冲区并换行
cout << "Value: " << x << '\n';  // '\n'仅换行，更高效
cout << x << " " << y << '\n';   // 链式输出

// 输入
int n;
cin >> n;                        // 跳过空白字符读取
cin >> x >> y >> z;              // 链式输入

// 格式化输出
#include <iomanip>
cout << fixed << setprecision(2) << 3.14159;  // 3.14（保留两位小数）
cout << setw(10) << x;           // 设置宽度为10
cout << hex << 255;              // 十六进制：ff
```

**技巧**：输入失败时 `cin` 进入错误状态，用 `cin.clear()` 恢复。

### 文件输入输出

文件流继承标准流，用法类似。位于 `<fstream>` 头文件。

```cpp
#include <fstream>

// 写文件
ofstream out("file.txt");        // 打开文件写入
if (out.is_open()) {             // 检查是否成功
    out << "Hello\n";
    out.close();                 // 关闭文件（可省略，析构自动关闭）
}

// 读文件
ifstream in("file.txt");
if (in.is_open()) {
    string line;
    while (getline(in, line)) {  // 按行读取
        cout << line << '\n';
    }
    in.close();
}

// 追加写入
ofstream out("file.txt", ios::app);

// 二进制读写
ofstream binOut("data.bin", ios::binary);
```

**注意**：文件流对象作用域结束时自动关闭；检查 `is_open()` 确保操作成功。

## 常见陷阱

初学者和经验丰富的程序员都可能遇到的典型错误。

```cpp
// 1. 整数除法截断
int a = 5 / 2;      // 结果是2（不是2.5），小数部分被截断
double b = 5 / 2;   // 仍是2.0（先算5/2=2，再转double）
double c = 5.0 / 2; // 正确：2.5（至少一个操作数是浮点）

// 2. 数组越界
int arr[5];
arr[5] = 10;        // 未定义行为！合法索引是0-4
arr[-1] = 10;       // 未定义行为！负索引

// 3. 悬空指针（野指针）
int* p = new int(10);
delete p;           // 释放内存
*p = 20;            // 未定义行为！访问已释放内存
p = nullptr;        // 良好习惯：释放后置空

// 4. 内存泄漏
void leak() {
    int* p = new int(10);
    return;         // 忘记delete，内存泄漏！
}

// 5. 未初始化变量
int x;              // 包含垃圾值（未定义）
cout << x;          // 输出不可预测
int y = 0;          // 正确：初始化为0

// 6. switch缺少break
switch (x) {
    case 1:
        cout << "One";
        // 没有break，会"穿透"到case 2！
    case 2:
        cout << "Two";
        break;
}

// 7. 赋值与比较混淆
if (x = 5) {        // 赋值！x变为5，条件永远为真
    // ...
}
if (x == 5) {       // 正确：比较
```

**防范**：开启编译器警告（`-Wall -Wextra`），使用静态分析工具，养成良好习惯。

## 编码规范

一致的编码风格提高代码可读性和可维护性。

### 命名规范

清晰的命名是自文档化的第一步。

```cpp
// 变量/函数：小驼峰（camelCase）
int studentAge;
string firstName;
void calculateSum();

// 常量：全大写+下划线
const int MAX_SIZE = 100;
const double PI = 3.14159;

// 类/结构体：大驼峰（PascalCase）
class StudentInfo;
struct Point2D;

// 宏：全大写+下划线
#define MAX_BUFFER_SIZE 1024

// 私有成员：前缀下划线（可选）
class MyClass {
    int _privateVar;
};
```

### 代码风格

```cpp
// 缩进：4空格（或2空格/Tab，团队统一即可）
if (condition) {
    statement;
}

// 括号风格：K&R（开括号同行）或Allman（开括号另起一行）
// K&R（推荐，节省行数）
if (condition) {
    // ...
}

// Allman
if (condition)
{
    // ...
}

// 一行一条语句
int a = 1;
int b = 2;

// 避免魔法数字（用命名常量）
const int MAX_STUDENTS = 100;
if (count > MAX_STUDENTS) {  // 清晰明了
    // ...
}

// 适当的空行分隔逻辑块
void func() {
    // 初始化
    int x = 0;
    
    // 处理逻辑
    for (...) {
        // ...
    }
    
    // 清理
    cleanup();
}
```

## 最佳实践

编写高质量C++代码的核心原则。

1. **优先使用 const**：不变的值用 `const` 或 `constexpr`，防止意外修改
2. **优先使用引用传参**：大对象用 `const&`，避免拷贝；小对象可值传递
3. **避免全局变量**：减少耦合和副作用，改用参数传递或单例模式
4. **RAII原则**：资源获取即初始化，利用析构函数自动释放资源
5. **避免裸指针**：用智能指针（`unique_ptr`/`shared_ptr`）管理动态内存
6. **初始化所有变量**：声明时立即初始化，优先用列表初始化 `{}`
7. **使用范围for**：遍历容器用 `for (auto& item : container)`，简洁安全
8. **善用auto**：复杂类型用 `auto`，但不滥用（简单类型明确写出）
9. **异常安全**：使用RAII和智能指针，确保异常时资源不泄漏
10. **代码可读性优先**：清晰的代码胜过聪明的技巧，他人能快速理解最重要

**核心思想**：写安全、清晰、高效的代码，按这个优先级排序。

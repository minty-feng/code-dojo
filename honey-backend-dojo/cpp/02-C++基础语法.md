# 02-C++基础语法

## 学习目标

本章学习目标如下：

- **理解C++的基本数据类型**：知道什么时候使用什么类型
- **掌握变量和常量的使用**：能够正确声明和使用变量
- **熟练运用各种运算符**：进行数学运算和逻辑判断
- **编写基本的控制结构**：实现条件判断和循环
- **理解函数的基本概念**：能够定义和调用函数
- **掌握数组和字符串**：处理多个数据
- **了解指针和引用的基础**：为后续学习做准备

## 数据类型

数据类型是编程的基础，就像生活中的容器一样，不同的容器适合装不同的东西。在C++中，不同的数据类型适合存储不同类型的数据。

### 为什么需要数据类型？

C++的数据类型系统具有以下作用：

1. **节省内存**：选择合适大小的类型
2. **提高性能**：不同类型有不同的处理速度
3. **避免错误**：编译器会检查类型匹配
4. **提高可读性**：代码更容易理解

### 基本数据类型

C++的基本数据类型可以分为几个主要类别，每个类别都有其特定的用途和内存占用。

#### 整型数据类型
整型用于存储整数，就像数学中的整数一样。

**int类型（最常用）：**
- 占用4字节内存
- 范围：-2,147,483,648 到 2,147,483,647
- 适用于：年龄、数量、计数器等
- 示例：`int age = 25;`

**short类型（节省内存）：**
- 占用2字节内存
- 范围：-32,768 到 32,767
- 适用于：小范围的数值，如月份、星期
- 示例：`short month = 12;`

**long类型（大范围）：**
- 占用4或8字节（取决于系统）
- 适用于：需要更大范围的整数
- 示例：`long population = 1000000;`

**long long类型（超大范围）：**
- 占用8字节内存
- 范围：-9,223,372,036,854,775,808 到 9,223,372,036,854,775,807
- 适用于：天文数字、科学计算
- 示例：`long long distance = 150000000000;`

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int studentAge = 20;           // 学生年龄
    short examScore = 95;          // 考试分数
    long studentID = 2023001234;   // 学号
    long long nationalID = 123456789012345; // 身份证号
    
    cout << "年龄: " << studentAge << endl;
    cout << "分数: " << examScore << endl;
    cout << "学号: " << studentID << endl;
    cout << "身份证: " << nationalID << endl;
    
    return 0;
}
```

#### 浮点型数据类型
浮点型用于存储小数，就像数学中的实数一样。

**float类型（单精度）：**
- 占用4字节内存
- 精度：约7位小数
- 适用于：一般计算，如价格、温度
- 示例：`float price = 19.99f;`

**double类型（双精度，推荐）：**
- 占用8字节内存
- 精度：约15位小数
- 适用于：科学计算、工程计算
- 示例：`double pi = 3.14159265359;`

**long double类型（高精度）：**
- 占用更多内存
- 精度：更高
- 适用于：高精度科学计算
- 示例：`long double preciseValue = 3.14159265358979323846L;`

**实际应用示例：**
```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    float temperature = 36.5f;        // 体温
    double salary = 8500.50;           // 工资
    long double interestRate = 0.035L; // 利率
    
    cout << fixed << setprecision(2);
    cout << "体温: " << temperature << "°C" << endl;
    cout << "工资: ¥" << salary << endl;
    cout << "利率: " << interestRate << "%" << endl;
    
    return 0;
}
```

#### 字符型数据类型
字符型用于存储单个字符。

**char类型（基本字符）：**
- 占用1字节内存
- 存储ASCII字符
- 适用于：单个字符，如字母、数字、符号
- 示例：`char grade = 'A';`

**字符编码说明：**
- ASCII：英文字符，0-127
- 扩展ASCII：128-255
- Unicode：国际字符

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    char firstLetter = 'A';
    char operatorSymbol = '+';
    char digit = '5';
    
    cout << "首字母: " << firstLetter << endl;
    cout << "运算符: " << operatorSymbol << endl;
    cout << "数字: " << digit << endl;
    
    // 字符的ASCII值
    cout << "A的ASCII值: " << (int)firstLetter << endl;
    
    return 0;
}
```

#### 布尔型数据类型
布尔型用于存储逻辑值，只有两个值。

**bool类型：**
- 占用1字节内存
- 只有两个值：`true`（真）和`false`（假）
- 适用于：条件判断、开关状态
- 示例：`bool isStudent = true;`

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    bool isStudent = true;
    bool hasLicense = false;
    bool isWeekend = false;
    
    cout << "是学生: " << (isStudent ? "是" : "否") << endl;
    cout << "有驾照: " << (hasLicense ? "有" : "无") << endl;
    cout << "是周末: " << (isWeekend ? "是" : "否") << endl;
    
    return 0;
}
```

### 类型修饰符
类型修饰符可以改变数据类型的行为，就像给容器贴上标签一样。

#### 符号修饰符
决定数据类型是否可以表示负数。

**signed（有符号，默认）：**
- 可以表示正数和负数
- 范围是对称的
- 示例：`signed int temperature = -10;`

**unsigned（无符号）：**
- 只能表示正数和零
- 范围更大
- 适用于：年龄、数量、索引
- 示例：`unsigned int age = 25;`

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    signed int temperature = -5;      // 温度可以是负数
    unsigned int age = 25;           // 年龄不能是负数
    unsigned int studentCount = 100; // 学生数量不能是负数
    
    cout << "温度: " << temperature << "°C" << endl;
    cout << "年龄: " << age << "岁" << endl;
    cout << "学生数: " << studentCount << "人" << endl;
    
    return 0;
}
```

#### 存储修饰符
控制数据的存储方式和访问权限。

**const（常量）：**
- 值不可修改
- 提供编译时保护
- 示例：`const double PI = 3.14159;`

**volatile（易变）：**
- 值可能被外部因素改变
- 防止编译器优化
- 适用于：硬件寄存器、多线程变量
- 示例：`volatile int sensorValue = 0;`

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    const double PI = 3.14159;        // 数学常数
    const int MAX_STUDENTS = 100;     // 最大学生数
    volatile int sensorReading = 0;    // 传感器读数
    
    cout << "圆周率: " << PI << endl;
    cout << "最大学生数: " << MAX_STUDENTS << endl;
    cout << "传感器读数: " << sensorReading << endl;
    
    // PI = 3.14;  // 错误！不能修改常量
    
    return 0;
}
```

### 类型大小
了解数据类型的大小对于内存管理和性能优化很重要。

**常见类型大小（64位系统）：**
```cpp
sizeof(char)        // 1字节
sizeof(int)         // 4字节（通常）
sizeof(long)        // 8字节（64位系统）
sizeof(float)       // 4字节
sizeof(double)      // 8字节
sizeof(bool)        // 1字节
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "数据类型大小（字节）:" << endl;
    cout << "char: " << sizeof(char) << endl;
    cout << "int: " << sizeof(int) << endl;
    cout << "long: " << sizeof(long) << endl;
    cout << "float: " << sizeof(float) << endl;
    cout << "double: " << sizeof(double) << endl;
    cout << "bool: " << sizeof(bool) << endl;
    
    return 0;
}
```

**类型选择建议：**
- **整数**：优先使用`int`，需要大范围时使用`long long`
- **小数**：优先使用`double`，需要节省内存时使用`float`
- **字符**：使用`char`
- **逻辑值**：使用`bool`
- **常量**：使用`const`修饰

## 变量和常量

变量和常量是程序中存储数据的基本方式，就像生活中的盒子一样，可以存放不同的东西。

### 变量声明
变量是存储数据的容器，必须先声明后使用。

#### 基本声明方式
```cpp
int age = 25;           // 声明并初始化
int height;             // 仅声明，值未定义
height = 180;           // 后续赋值
auto name = "Alice";    // 自动类型推导（C++11）
```

#### 变量命名规则
良好的变量命名是编程的重要技能：

**基本规则：**
- 必须以字母或下划线开头
- 只能包含字母、数字和下划线
- 区分大小写
- 不能使用C++关键字

**命名建议：**
- 使用有意义的名称：`studentAge`而不是`a`
- 使用驼峰命名：`firstName`、`lastName`
- 常量使用大写：`MAX_SIZE`
- 避免缩写：`numberOfStudents`而不是`numStud`

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    // 好的命名示例
    int studentAge = 20;
    string studentName = "张三";
    double averageScore = 85.5;
    bool isGraduated = false;
    
    // 不好的命名示例（避免这样做）
    int a = 20;           // 没有意义
    string n = "张三";    // 缩写不清楚
    double s = 85.5;      // 含义不明
    
    cout << "学生姓名: " << studentName << endl;
    cout << "年龄: " << studentAge << endl;
    cout << "平均分: " << averageScore << endl;
    cout << "是否毕业: " << (isGraduated ? "是" : "否") << endl;
    
    return 0;
}
```

#### 初始化的重要性
未初始化的变量包含垃圾值，可能导致程序行为不可预测。

**初始化方法：**
```cpp
int x = 10;        // 传统初始化
int y(20);         // 构造函数初始化
int z{30};         // 列表初始化（推荐）
int w = {40};      // 列表初始化
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    // 不同的初始化方式
    int traditional = 10;     // 传统方式
    int constructor(20);      // 构造函数方式
    int list{30};            // 列表初始化（推荐）
    int mixed = {40};        // 混合方式
    
    cout << "传统初始化: " << traditional << endl;
    cout << "构造函数初始化: " << constructor << endl;
    cout << "列表初始化: " << list << endl;
    cout << "混合初始化: " << mixed << endl;
    
    return 0;
}
```

### 常量定义
常量是值不可改变的变量，就像数学中的常数一样。

#### const关键字
```cpp
const int MAX_SIZE = 100;           // 编译时常量
const double PI = 3.14159;         // 浮点常量
const char* MESSAGE = "Hello";     // 字符串常量
```

#### constexpr关键字（C++11）
```cpp
constexpr int BUFFER_SIZE = 1024;   // 编译时计算
constexpr int factorial(int n) {    // 编译时函数
    return (n <= 1) ? 1 : n * factorial(n - 1);
}
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    const int MAX_STUDENTS = 50;        // 最大学生数
    const double PI = 3.14159;          // 圆周率
    const string SCHOOL_NAME = "北京大学"; // 学校名称
    
    constexpr int BUFFER_SIZE = 1024;   // 缓冲区大小
    constexpr int ARRAY_SIZE = 10;      // 数组大小
    
    cout << "最大学生数: " << MAX_STUDENTS << endl;
    cout << "圆周率: " << PI << endl;
    cout << "学校名称: " << SCHOOL_NAME << endl;
    cout << "缓冲区大小: " << BUFFER_SIZE << endl;
    cout << "数组大小: " << ARRAY_SIZE << endl;
    
    return 0;
}
```

### 作用域
作用域决定了变量的可见性和生命周期，就像房间的门一样，决定了谁能看到里面的东西。

#### 局部作用域
函数内部的作用域，是最常用的作用域。

**特点：**
- 只在函数内部可见
- 函数结束时销毁
- 不同函数中的同名变量互不影响

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

void function1() {
    int localVar = 100;  // 局部变量
    cout << "函数1中的变量: " << localVar << endl;
}

void function2() {
    int localVar = 200;  // 同名局部变量
    cout << "函数2中的变量: " << localVar << endl;
}

int main() {
    function1();
    function2();
    // cout << localVar;  // 错误！局部变量不可见
    return 0;
}
```

#### 全局作用域
文件级别的作用域，在整个文件中可见。

**特点：**
- 在整个文件中可见
- 程序结束时销毁
- 可能造成命名冲突

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

// 全局变量
int globalCounter = 0;
const string APP_NAME = "学生管理系统";

void incrementCounter() {
    globalCounter++;
    cout << "计数器: " << globalCounter << endl;
}

int main() {
    cout << "应用名称: " << APP_NAME << endl;
    incrementCounter();
    incrementCounter();
    cout << "最终计数: " << globalCounter << endl;
    return 0;
}
```

#### 块作用域
{}块内的作用域，支持嵌套。

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int outerVar = 10;
    cout << "外层变量: " << outerVar << endl;
    
    {
        int innerVar = 20;
        cout << "内层变量: " << innerVar << endl;
        cout << "外层变量在内层: " << outerVar << endl;
    }
    
    // cout << innerVar;  // 错误！内层变量不可见
    cout << "外层变量在外层: " << outerVar << endl;
    
    return 0;
}
```

## 运算符

运算符是C++中用于执行各种操作的符号，就像数学中的加减乘除一样。

### 算术运算符
算术运算符用于执行基本的数学运算。

#### 基本算术运算符
```cpp
int a = 10, b = 3;
int sum = a + b;        // 加法：13
int diff = a - b;       // 减法：7
int product = a * b;    // 乘法：30
int quotient = a / b;   // 除法：3
int remainder = a % b;  // 取模：1
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int num1, num2;
    cout << "请输入两个整数: ";
    cin >> num1 >> num2;
    
    cout << "加法: " << num1 << " + " << num2 << " = " << (num1 + num2) << endl;
    cout << "减法: " << num1 << " - " << num2 << " = " << (num1 - num2) << endl;
    cout << "乘法: " << num1 << " * " << num2 << " = " << (num1 * num2) << endl;
    cout << "除法: " << num1 << " / " << num2 << " = " << (num1 / num2) << endl;
    cout << "取模: " << num1 << " % " << num2 << " = " << (num1 % num2) << endl;
    
    return 0;
}
```

#### 自增自减运算符
自增自减运算符是C++特有的运算符。

**前置和后置的区别：**
```cpp
int x = 5;
int y = ++x;    // 前置：x=6, y=6
int z = x++;    // 后置：x=7, z=6
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int counter = 0;
    
    cout << "初始值: " << counter << endl;
    
    cout << "前置自增: " << ++counter << endl;  // 先自增再使用
    cout << "当前值: " << counter << endl;
    
    cout << "后置自增: " << counter++ << endl;  // 先使用再自增
    cout << "当前值: " << counter << endl;
    
    return 0;
}
```

### 关系运算符
关系运算符用于比较两个值的大小关系，返回布尔值。

```cpp
int a = 10, b = 20;
bool equal = (a == b);      // false
bool notEqual = (a != b);   // true
bool less = (a < b);        // true
bool greater = (a > b);     // false
bool lessEqual = (a <= b);  // true
bool greaterEqual = (a >= b); // false
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int score;
    cout << "请输入分数: ";
    cin >> score;
    
    if (score >= 90) {
        cout << "优秀" << endl;
    } else if (score >= 80) {
        cout << "良好" << endl;
    } else if (score >= 70) {
        cout << "中等" << endl;
    } else if (score >= 60) {
        cout << "及格" << endl;
    } else {
        cout << "不及格" << endl;
    }
    
    return 0;
}
```

### 逻辑运算符
逻辑运算符用于组合多个条件，实现复杂的逻辑判断。逻辑运算是程序控制流的基础，掌握逻辑运算符对于编写条件判断和循环控制至关重要。

#### 基本逻辑运算符
C++提供了三种基本逻辑运算符，每种都有其特定的用途和优先级。

**逻辑与运算符 (&&)：**
- 当且仅当两个操作数都为true时，结果才为true
- 具有短路求值特性：如果第一个操作数为false，不会计算第二个操作数
- 优先级高于逻辑或运算符

**逻辑或运算符 (||)：**
- 当至少有一个操作数为true时，结果就为true
- 具有短路求值特性：如果第一个操作数为true，不会计算第二个操作数
- 优先级低于逻辑与运算符

**逻辑非运算符 (!)：**
- 对操作数进行逻辑取反
- 一元运算符，优先级最高
- 将true变为false，将false变为true

```cpp
bool condition1 = true;
bool condition2 = false;
bool result1 = condition1 && condition2;  // 逻辑与：false
bool result2 = condition1 || condition2;   // 逻辑或：true
bool result3 = !condition1;                // 逻辑非：false
```

#### 逻辑运算符的优先级和结合性
理解运算符的优先级对于编写正确的逻辑表达式非常重要。

**优先级顺序（从高到低）：**
1. `!` (逻辑非) - 一元运算符，右结合
2. `&&` (逻辑与) - 二元运算符，左结合
3. `||` (逻辑或) - 二元运算符，左结合

**复杂逻辑表达式示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int age = 25;
    bool hasLicense = true;
    bool hasInsurance = false;
    bool isWeekend = true;
    
    // 复杂逻辑表达式
    bool canDrive = (age >= 18) && hasLicense && hasInsurance;
    bool canDriveWeekend = (age >= 18) && hasLicense && (hasInsurance || isWeekend);
    
    cout << "工作日可以开车: " << canDrive << endl;
    cout << "周末可以开车: " << canDriveWeekend << endl;
    
    // 使用括号明确优先级
    bool complexCondition = (age >= 18 && hasLicense) || (age >= 16 && isWeekend);
    cout << "复杂条件: " << complexCondition << endl;
    
    return 0;
}
```

#### 短路求值详解
短路求值是逻辑运算符的重要特性，可以提高程序效率并实现条件执行。

**短路求值的工作原理：**
- 逻辑与(&&)：如果左操作数为false，右操作数不会被计算
- 逻辑或(||)：如果左操作数为true，右操作数不会被计算

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

bool checkAge(int age) {
    cout << "检查年龄: " << age << endl;
    return age >= 18;
}

bool checkLicense(bool hasLicense) {
    cout << "检查驾照" << endl;
    return hasLicense;
}

bool checkInsurance(bool hasInsurance) {
    cout << "检查保险" << endl;
    return hasInsurance;
}

int main() {
    int age = 16;
    bool hasLicense = true;
    bool hasInsurance = true;
    
    cout << "=== 短路求值示例 ===" << endl;
    
    // 逻辑与短路求值：age < 18，不会检查驾照
    if (checkAge(age) && checkLicense(hasLicense)) {
        cout << "可以开车" << endl;
    } else {
        cout << "不能开车" << endl;
    }
    
    cout << "\n=== 逻辑或短路求值 ===" << endl;
    
    // 逻辑或短路求值：第一个条件为true，不会检查保险
    if (checkAge(25) || checkInsurance(hasInsurance)) {
        cout << "满足条件" << endl;
    }
    
    return 0;
}
```

#### 逻辑运算符的实际应用场景
逻辑运算符在实际编程中有广泛的应用，特别是在条件判断和循环控制中。

**用户权限验证：**
```cpp
#include <iostream>
using namespace std;

int main() {
    string username = "admin";
    string password = "123456";
    bool isLoggedIn = false;
    bool hasPermission = true;
    
    // 用户登录验证
    if (username == "admin" && password == "123456") {
        isLoggedIn = true;
        cout << "登录成功" << endl;
    }
    
    // 权限检查
    if (isLoggedIn && hasPermission) {
        cout << "可以访问管理功能" << endl;
    } else {
        cout << "权限不足" << endl;
    }
    
    return 0;
}
```

**数据验证：**
```cpp
#include <iostream>
using namespace std;

bool isValidAge(int age) {
    return age >= 0 && age <= 150;
}

bool isValidScore(int score) {
    return score >= 0 && score <= 100;
}

int main() {
    int age = 25;
    int score = 85;
    
    // 数据验证
    if (isValidAge(age) && isValidScore(score)) {
        cout << "数据有效" << endl;
        
        // 成绩等级判断
        if (score >= 90) {
            cout << "优秀" << endl;
        } else if (score >= 80) {
            cout << "良好" << endl;
        } else if (score >= 70) {
            cout << "中等" << endl;
        } else if (score >= 60) {
            cout << "及格" << endl;
        } else {
            cout << "不及格" << endl;
        }
    } else {
        cout << "数据无效" << endl;
    }
    
    return 0;
}
```

**条件组合：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int temperature = 25;
    bool isSunny = true;
    bool isWeekend = false;
    bool hasUmbrella = false;
    
    // 复杂的天气判断逻辑
    if (isSunny && temperature > 20) {
        cout << "适合户外活动" << endl;
    } else if (!isSunny && hasUmbrella) {
        cout << "可以出门，记得带伞" << endl;
    } else if (isWeekend && temperature > 15) {
        cout << "周末可以出门" << endl;
    } else {
        cout << "建议待在家里" << endl;
    }
    
    return 0;
}
```

### 数学运算符
数学运算符是编程中最基础也是最重要的运算符，包括基本算术运算和高级数学函数。

#### 基本算术运算符
C++提供了五种基本算术运算符，用于执行基本的数学运算。

**加法运算符 (+)：**
- 用于两个数值相加
- 也可以用于字符串连接（重载）
- 支持整数和浮点数运算

**减法运算符 (-)：**
- 用于两个数值相减
- 也可以用作一元运算符表示负数
- 支持整数和浮点数运算

**乘法运算符 (*)：**
- 用于两个数值相乘
- 支持整数和浮点数运算
- 注意整数乘法的溢出问题

**除法运算符 (/)：**
- 用于两个数值相除
- 整数除法会截断小数部分
- 浮点数除法保留小数部分

**取模运算符 (%)：**
- 用于计算两个整数相除的余数
- 只适用于整数类型
- 常用于判断奇偶性、周期性计算

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 10, b = 3;
    double x = 10.0, y = 3.0;
    
    // 基本算术运算
    cout << "整数运算:" << endl;
    cout << "a + b = " << (a + b) << endl;  // 13
    cout << "a - b = " << (a - b) << endl;  // 7
    cout << "a * b = " << (a * b) << endl;  // 30
    cout << "a / b = " << (a / b) << endl;  // 3 (整数除法)
    cout << "a % b = " << (a % b) << endl;  // 1
    
    cout << "\n浮点数运算:" << endl;
    cout << "x + y = " << (x + y) << endl;  // 13.0
    cout << "x - y = " << (x - y) << endl;  // 7.0
    cout << "x * y = " << (x * y) << endl;  // 30.0
    cout << "x / y = " << (x / y) << endl;  // 3.33333
    
    return 0;
}
```

#### 高级数学函数
C++标准库提供了丰富的数学函数，需要包含`<cmath>`头文件。

**幂运算函数：**
- `pow(base, exponent)`：计算base的exponent次幂
- `sqrt(x)`：计算x的平方根
- `cbrt(x)`：计算x的立方根（C++11）

**三角函数：**
- `sin(x)`：正弦函数，x为弧度
- `cos(x)`：余弦函数，x为弧度
- `tan(x)`：正切函数，x为弧度
- `asin(x)`：反正弦函数
- `acos(x)`：反余弦函数
- `atan(x)`：反正切函数

**对数函数：**
- `log(x)`：自然对数（以e为底）
- `log10(x)`：常用对数（以10为底）
- `log2(x)`：以2为底的对数（C++11）

**其他数学函数：**
- `abs(x)`：绝对值
- `fabs(x)`：浮点数绝对值
- `ceil(x)`：向上取整
- `floor(x)`：向下取整
- `round(x)`：四舍五入
- `fmod(x, y)`：浮点数取模

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double x = 2.0;
    double y = 3.0;
    double angle = 45.0; // 角度
    
    cout << "=== 幂运算 ===" << endl;
    cout << "pow(2, 3) = " << pow(x, y) << endl;        // 8.0
    cout << "sqrt(16) = " << sqrt(16.0) << endl;        // 4.0
    cout << "cbrt(27) = " << cbrt(27.0) << endl;        // 3.0
    
    cout << "\n=== 三角函数 ===" << endl;
    double radians = angle * M_PI / 180.0; // 转换为弧度
    cout << "sin(45°) = " << sin(radians) << endl;      // 0.707107
    cout << "cos(45°) = " << cos(radians) << endl;      // 0.707107
    cout << "tan(45°) = " << tan(radians) << endl;      // 1.0
    
    cout << "\n=== 对数函数 ===" << endl;
    cout << "log(e) = " << log(M_E) << endl;            // 1.0
    cout << "log10(100) = " << log10(100.0) << endl;    // 2.0
    cout << "log2(8) = " << log2(8.0) << endl;          // 3.0
    
    cout << "\n=== 其他函数 ===" << endl;
    cout << "abs(-5) = " << abs(-5) << endl;            // 5
    cout << "ceil(3.2) = " << ceil(3.2) << endl;        // 4.0
    cout << "floor(3.8) = " << floor(3.8) << endl;      // 3.0
    cout << "round(3.6) = " << round(3.6) << endl;      // 4.0
    cout << "fmod(10.5, 3.0) = " << fmod(10.5, 3.0) << endl; // 1.5
    
    return 0;
}
```

#### 数学运算的实际应用
数学运算在实际编程中有广泛的应用，特别是在科学计算、图形处理和游戏开发中。

**几何计算：**
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    // 计算圆的面积和周长
    double radius = 5.0;
    double area = M_PI * pow(radius, 2);
    double circumference = 2 * M_PI * radius;
    
    cout << "半径: " << radius << endl;
    cout << "面积: " << area << endl;
    cout << "周长: " << circumference << endl;
    
    // 计算两点间距离
    double x1 = 0, y1 = 0;
    double x2 = 3, y2 = 4;
    double distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
    cout << "两点间距离: " << distance << endl;
    
    return 0;
}
```

**科学计算：**
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    // 物理计算：自由落体运动
    double g = 9.81;  // 重力加速度
    double t = 2.0;   // 时间
    double height = 0.5 * g * pow(t, 2);
    double velocity = g * t;
    
    cout << "自由落体运动计算:" << endl;
    cout << "时间: " << t << " 秒" << endl;
    cout << "下落高度: " << height << " 米" << endl;
    cout << "瞬时速度: " << velocity << " 米/秒" << endl;
    
    // 复利计算
    double principal = 1000.0;  // 本金
    double rate = 0.05;         // 年利率
    int years = 10;             // 年数
    double amount = principal * pow(1 + rate, years);
    
    cout << "\n复利计算:" << endl;
    cout << "本金: " << principal << " 元" << endl;
    cout << "年利率: " << rate * 100 << "%" << endl;
    cout << "年数: " << years << " 年" << endl;
    cout << "最终金额: " << amount << " 元" << endl;
    
    return 0;
}
```

**统计计算：**
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    // 计算平均值和标准差
    double data[] = {85, 90, 78, 92, 88, 76, 95, 82, 89, 91};
    int n = sizeof(data) / sizeof(data[0]);
    
    // 计算平均值
    double sum = 0;
    for (int i = 0; i < n; i++) {
        sum += data[i];
    }
    double mean = sum / n;
    
    // 计算标准差
    double variance = 0;
    for (int i = 0; i < n; i++) {
        variance += pow(data[i] - mean, 2);
    }
    double stdDev = sqrt(variance / n);
    
    cout << "数据统计:" << endl;
    cout << "平均值: " << mean << endl;
    cout << "标准差: " << stdDev << endl;
    
    return 0;
}
```

### 赋值运算符
赋值运算符用于给变量赋值，C++提供了多种复合赋值运算符。

**基本赋值运算符 (=)：**
- 将右操作数的值赋给左操作数
- 左操作数必须是可修改的左值

**复合赋值运算符：**
- `+=`：加法赋值
- `-=`：减法赋值
- `*=`：乘法赋值
- `/=`：除法赋值
- `%=`：取模赋值

```cpp
int x = 10;
x += 5;     // x = 15
x -= 3;     // x = 12
x *= 2;     // x = 24
x /= 4;     // x = 6
x %= 5;     // x = 1
```

**实际应用示例：**
```cpp
#include <iostream>
using namespace std;

int main() {
    int balance = 1000;
    cout << "初始余额: " << balance << endl;
    
    balance += 500;  // 存款
    cout << "存款后: " << balance << endl;
    
    balance -= 200;  // 取款
    cout << "取款后: " << balance << endl;
    
    balance *= 2;    // 翻倍
    cout << "翻倍后: " << balance << endl;
    
    return 0;
}
```

## 学习建议

### 初学者学习路径
1. **理解概念**：先理解每个概念的含义再编写代码
2. **动手实践**：每个概念都需要代码验证
3. **注意细节**：C++对细节要求很严格
4. **循序渐进**：按顺序掌握知识点

### 常见错误和避免方法
1. **未初始化变量**：总是初始化变量
2. **类型不匹配**：注意数据类型的选择
3. **命名不规范**：使用有意义的变量名
4. **忽略警告**：认真对待编译器的警告

### 练习建议
1. **编写小程序**：每个概念都编写一个小程序
2. **修改示例**：修改书中的示例代码
3. **解决问题**：运用学到的知识解决实际问题
4. **代码审查**：检查自己的代码是否有问题

## 控制结构

### 条件语句
```cpp
// if-else
if (condition) {
    // 代码块
} else if (condition2) {
    // 代码块
} else {
    // 代码块
}

// 三元运算符
result = (condition) ? value1 : value2;
```

### 循环语句
```cpp
// for循环
for (int i = 0; i < 10; ++i) {
    // 代码块
}

// while循环
while (condition) {
    // 代码块
}

// do-while循环
do {
    // 代码块
} while (condition);

// 范围for循环（C++11）
for (auto item : container) {
    // 代码块
}
```

### 跳转语句
- **break**：跳出循环
- **continue**：跳过本次循环
- **return**：返回函数
- **goto**：跳转到标签（不推荐）

## 函数

### 函数定义
```cpp
// 函数声明
int add(int a, int b);

// 函数定义
int add(int a, int b) {
    return a + b;
}

// 默认参数
void print(int value, int base = 10);

// 函数重载
int multiply(int a, int b);
double multiply(double a, double b);
```

### 函数参数传递
- **值传递**：复制参数值
- **引用传递**：传递引用
- **指针传递**：传递地址
- **const引用**：只读引用

### 内联函数
```cpp
inline int square(int x) {
    return x * x;
}
```

## 数组和字符串

### 数组
```cpp
int arr[5] = {1, 2, 3, 4, 5};    // 静态数组
int arr2[] = {1, 2, 3};          // 自动大小
int arr3[5] = {};                // 初始化为0
```

### 字符串
```cpp
char str1[] = "Hello";           // C风格字符串
char str2[10] = "World";
std::string str3 = "C++";        // C++字符串
```

### 多维数组
```cpp
int matrix[3][4];                // 3行4列
int cube[2][3][4];               // 三维数组
```

## 指针和引用

### 指针基础
```cpp
int value = 42;
int* ptr = &value;               // 指针指向value
int deref = *ptr;                // 解引用
```

### 指针运算
```cpp
int arr[5] = {1, 2, 3, 4, 5};
int* ptr = arr;                  // 指向第一个元素
ptr++;                           // 指向下一个元素
int diff = ptr - arr;            // 指针差值
```

### 引用
```cpp
int value = 42;
int& ref = value;                // 引用
ref = 100;                       // 修改原值
```

### 动态内存
```cpp
int* ptr = new int(42);          // 动态分配
delete ptr;                      // 释放内存

int* arr = new int[10];          // 动态数组
delete[] arr;                    // 释放数组
```

## 预处理器

### 宏定义
```cpp
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define PI 3.14159
```

### 条件编译
```cpp
#ifdef DEBUG
    // 调试代码
#endif

#ifndef HEADER_H
#define HEADER_H
    // 头文件内容
#endif
```

### 文件包含
```cpp
#include <iostream>              // 系统头文件
#include "myheader.h"            // 用户头文件
```

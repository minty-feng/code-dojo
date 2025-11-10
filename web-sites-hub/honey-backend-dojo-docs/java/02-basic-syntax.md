# 02-Java基础语法

Java是强类型、面向对象的语言。语法简洁，自动内存管理，跨平台运行。

## 数据类型

### 基本数据类型

Java有8种基本类型，存储在栈上，传值。

```java
// 整型
byte b = 127;           // 1字节，-128~127
short s = 32767;        // 2字节，-32768~32767
int i = 2147483647;     // 4字节（常用）
long l = 9223372036854775807L;  // 8字节，数字后加L

// 浮点型
float f = 3.14f;        // 4字节，7位精度，数字后加f
double d = 3.14159;     // 8字节，15位精度（默认）

// 字符型
char c = 'A';           // 2字节，Unicode字符

// 布尔型
boolean flag = true;    // true或false
```

**常用类型：**
- 整数：`int`，大数：`long`
- 小数：`double`
- 字符：`char`，字符串：`String`

### 引用类型

引用类型存储对象引用（类似指针），包括类、接口、数组。

```java
String str = "Hello";           // 字符串（不可变）
int[] arr = {1, 2, 3};          // 数组
Object obj = new Object();      // 对象
Integer num = 10;               // 包装类（自动装箱）
```

### 包装类

基本类型的对象封装，提供实用方法。

```java
Byte, Short, Integer, Long      // 整型包装
Float, Double                    // 浮点包装
Character                        // 字符包装
Boolean                          // 布尔包装

// 自动装箱/拆箱（Java 5+）
Integer num = 10;                // 装箱：int -> Integer
int val = num;                   // 拆箱：Integer -> int

// 包装类方法
Integer.parseInt("123");         // 字符串转整数
Integer.toString(123);           // 整数转字符串
Integer.MAX_VALUE;               // 最大值
Double.isNaN(d);                 // 判断NaN
```

**注意：** 包装类是对象，可能为null；比较用 `equals()` 而非 `==`。

## 变量和常量

### 变量声明

```java
int age = 25;                    // 声明并初始化
int height;                      // 仅声明
height = 180;                    // 后续赋值

var x = 10;                      // 类型推断（Java 10+）
var list = new ArrayList<String>();
```

### 常量

```java
final int MAX = 100;             // final常量，不可修改
static final double PI = 3.14159; // 类常量

// 空白final（构造函数中初始化）
class Circle {
    private final double radius;
    
    public Circle(double r) {
        this.radius = r;  // 只能赋值一次
    }
}
```

## 运算符

### 算术运算符

```java
+  -  *  /  %           // 加减乘除取模
++  --                  // 自增自减
+=  -=  *=  /=  %=      // 复合赋值

// 注意整数除法
int a = 5 / 2;          // 2（截断）
double b = 5.0 / 2;     // 2.5
```

### 比较运算符

```java
==  !=  >  <  >=  <=    // 比较

// 注意：引用类型比较
String s1 = "hello";
String s2 = "hello";
s1 == s2;               // true（字符串常量池）
s1.equals(s2);          // true（内容相等，推荐）

String s3 = new String("hello");
s1 == s3;               // false（不同对象）
s1.equals(s3);          // true（内容相等）
```

### 逻辑运算符

```java
&&  ||  !               // 与或非（短路）
&   |                   // 与或（不短路）
```

### 位运算符

```java
&   |   ^   ~           // 按位与或异或取反
<<  >>  >>>             // 左移、算术右移、逻辑右移
```

**特殊：** Java的 `>>>` 是无符号右移，高位补0。

## 控制结构

### 条件语句

```java
// if-else
if (condition) {
    // ...
} else if (condition2) {
    // ...
} else {
    // ...
}

// switch（支持String）
switch (value) {
    case "A":
        // ...
        break;
    case "B":
        // ...
        break;
    default:
        // ...
}

// switch表达式（Java 12+）
String result = switch (day) {
    case "MON", "TUE", "WED", "THU", "FRI" -> "Workday";
    case "SAT", "SUN" -> "Weekend";
    default -> "Invalid";
};

// 三元运算符
int max = (a > b) ? a : b;
```

### 循环语句

```java
// for循环
for (int i = 0; i < n; i++) {
    // ...
}

// 增强for（foreach）
for (String item : list) {
    // ...
}

// while循环
while (condition) {
    // ...
}

// do-while循环
do {
    // ...
} while (condition);
```

### 跳转语句

```java
break;              // 跳出循环
continue;           // 跳过本次迭代
return;             // 返回
// Java无goto
```

## 数组

### 一维数组

```java
// 声明
int[] arr1;                      // 推荐写法
int arr2[];                      // C风格

// 创建
int[] arr = new int[5];          // 默认值0
int[] arr2 = {1, 2, 3, 4, 5};    // 初始化列表
int[] arr3 = new int[]{1, 2, 3}; // 显式创建

// 访问
arr[0] = 10;
int len = arr.length;            // 注意：length是属性，不是方法

// 遍历
for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}

for (int val : arr) {
    System.out.println(val);
}
```

### 多维数组

```java
// 二维数组
int[][] matrix = new int[3][4];
int[][] matrix2 = {{1, 2}, {3, 4}, {5, 6}};

// 不规则数组
int[][] irregular = new int[3][];
irregular[0] = new int[2];
irregular[1] = new int[3];
irregular[2] = new int[1];
```

### 数组工具类

```java
import java.util.Arrays;

int[] arr = {3, 1, 4, 1, 5};

// 排序
Arrays.sort(arr);                // {1, 1, 3, 4, 5}

// 二分查找（需要有序）
int index = Arrays.binarySearch(arr, 3);

// 填充
Arrays.fill(arr, 0);             // 全部填充为0

// 复制
int[] copy = Arrays.copyOf(arr, arr.length);

// 比较
boolean equal = Arrays.equals(arr1, arr2);

// 转字符串
String str = Arrays.toString(arr);  // [1, 1, 3, 4, 5]
```

## 字符串

### String类

String是不可变对象，线程安全但每次修改创建新对象。

```java
String s1 = "Hello";             // 字符串字面量（常量池）
String s2 = new String("Hello"); // 堆上创建新对象

// 常用方法
s1.length();                     // 长度
s1.charAt(0);                    // 获取字符
s1.substring(0, 3);              // 子串[0, 3)
s1.indexOf("ll");                // 查找位置
s1.contains("ell");              // 是否包含
s1.startsWith("He");             // 前缀
s1.endsWith("lo");               // 后缀
s1.toUpperCase();                // 转大写
s1.toLowerCase();                // 转小写
s1.trim();                       // 去空格
s1.replace("l", "L");            // 替换
s1.split(",");                   // 分割

// 拼接
String result = s1 + " " + s2;   // +运算符
String.join(", ", "a", "b", "c"); // join方法
```

### StringBuilder

可变字符串，适合频繁修改，非线程安全。

```java
StringBuilder sb = new StringBuilder();
sb.append("Hello");
sb.append(" ");
sb.append("World");
sb.insert(5, ",");               // 插入
sb.delete(5, 6);                 // 删除
sb.reverse();                    // 反转
String result = sb.toString();

// 性能对比
// String拼接1000次：~500ms（每次创建新对象）
// StringBuilder：~1ms（可变）
```

### StringBuffer

线程安全的StringBuilder，性能略低。

```java
StringBuffer sbf = new StringBuffer();
sbf.append("Thread-safe");
```

## 方法

### 方法定义

```java
// 访问修饰符 返回类型 方法名(参数列表)
public int add(int a, int b) {
    return a + b;
}

// 无返回值
public void print(String msg) {
    System.out.println(msg);
}

// 可变参数
public int sum(int... numbers) {
    int total = 0;
    for (int num : numbers) {
        total += num;
    }
    return total;
}
sum(1, 2, 3, 4, 5);  // 可传任意个参数
```

### 方法重载

同名方法，不同参数。

```java
public int max(int a, int b) {
    return a > b ? a : b;
}

public double max(double a, double b) {
    return a > b ? a : b;
}

public int max(int a, int b, int c) {
    return max(max(a, b), c);
}
```

**注意：** 返回值不同不构成重载，仅参数列表不同才行。

## 面向对象基础

### 类和对象

```java
public class Person {
    // 成员变量（字段）
    private String name;
    private int age;
    
    // 构造函数
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Getter
    public String getName() {
        return name;
    }
    
    // Setter
    public void setName(String name) {
        this.name = name;
    }
    
    // 方法
    public void introduce() {
        System.out.println("I'm " + name + ", " + age + " years old.");
    }
}

// 创建对象
Person p = new Person("Alice", 25);
p.introduce();
```

### 访问修饰符

```java
public      // 所有类可访问
protected   // 同包+子类可访问
默认(无)     // 同包可访问
private     // 仅本类可访问
```

### static关键字

```java
public class Counter {
    private static int count = 0;  // 静态变量（类变量）
    
    public Counter() {
        count++;
    }
    
    public static int getCount() {  // 静态方法
        return count;
    }
}

// 使用
Counter c1 = new Counter();
Counter c2 = new Counter();
System.out.println(Counter.getCount());  // 2
```

## 常见陷阱

```java
// 1. == vs equals
String s1 = "hello";
String s2 = new String("hello");
s1 == s2;               // false（引用不同）
s1.equals(s2);          // true（内容相同）

// 2. 数组越界
int[] arr = new int[5];
arr[5] = 10;            // ArrayIndexOutOfBoundsException

// 3. 空指针
String s = null;
s.length();             // NullPointerException

// 4. 整数除法
int a = 5 / 2;          // 2（不是2.5）

// 5. switch缺少break
switch (x) {
    case 1:
        System.out.println("One");
        // 没有break，会穿透到case 2
    case 2:
        System.out.println("Two");
        break;
}
```

## 输入输出

### 控制台输入输出

```java
import java.util.Scanner;

// 输出
System.out.println("Hello");     // 带换行
System.out.print("World");       // 不换行
System.out.printf("Age: %d\n", 25);  // 格式化

// 输入
Scanner scanner = new Scanner(System.in);
int num = scanner.nextInt();     // 读整数
double d = scanner.nextDouble(); // 读浮点数
String line = scanner.nextLine(); // 读一行
scanner.close();
```

### 文件输入输出

```java
import java.io.*;

// 写文件
try (PrintWriter writer = new PrintWriter("output.txt")) {
    writer.println("Hello, File!");
} catch (IOException e) {
    e.printStackTrace();
}

// 读文件
try (BufferedReader reader = new BufferedReader(new FileReader("input.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

## 异常处理

### try-catch-finally

```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Division by zero: " + e.getMessage());
} catch (Exception e) {
    System.out.println("General exception: " + e.getMessage());
} finally {
    // 总是执行（清理资源）
    System.out.println("Cleanup");
}
```

### try-with-resources（推荐）

自动关闭资源，适用于实现 `AutoCloseable` 的类。

```java
// Java 7+
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
} catch (IOException e) {
    e.printStackTrace();
}
// 自动调用close()，无需finally
```

### 抛出异常

```java
public void divide(int a, int b) {
    if (b == 0) {
        throw new IllegalArgumentException("Divisor cannot be zero");
    }
    return a / b;
}

// 声明抛出
public void readFile() throws IOException {
    FileReader fr = new FileReader("file.txt");
    // ...
}
```

## 最佳实践

1. **使用final**：不变的变量用final
2. **优先局部变量**：缩小作用域
3. **避免魔法数字**：用常量代替
4. **null检查**：访问对象前判空
5. **关闭资源**：用try-with-resources
6. **StringBuilder拼接**：循环中拼接字符串
7. **equals比较对象**：引用类型用equals
8. **包装类慎用==**：可能缓存失效
9. **异常分类**：可恢复用检查异常，不可恢复用运行时异常
10. **遵循命名规范**：提高可读性

**核心：** Java强调安全性和可维护性，利用语言特性写清晰健壮的代码。


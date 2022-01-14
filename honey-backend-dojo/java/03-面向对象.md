# 03-Java面向对象

Java是纯面向对象语言（除基本类型外）。封装、继承、多态是三大核心特性。

## 类和对象

### 完整类定义

```java
public class Student {
    // 成员变量
    private String name;
    private int age;
    private static int count = 0;  // 静态变量
    
    // 静态代码块（类加载时执行一次）
    static {
        System.out.println("Static block executed");
    }
    
    // 实例代码块（每次创建对象时执行）
    {
        count++;
        System.out.println("Instance block executed");
    }
    
    // 构造函数
    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // 重载构造函数
    public Student(String name) {
        this(name, 18);  // 调用另一个构造函数
    }
    
    // Getter/Setter
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    
    // 静态方法
    public static int getCount() {
        return count;
    }
    
    // toString
    @Override
    public String toString() {
        return "Student{name='" + name + "', age=" + age + "}";
    }
    
    // equals
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Student student = (Student) obj;
        return age == student.age && name.equals(student.name);
    }
    
    // hashCode
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

## 继承

### 单继承

Java只支持单继承，用 `extends` 关键字。

```java
// 父类
public class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public void eat() {
        System.out.println(name + " is eating");
    }
}

// 子类
public class Dog extends Animal {
    private String breed;
    
    public Dog(String name, String breed) {
        super(name);  // 调用父类构造函数
        this.breed = breed;
    }
    
    @Override
    public void eat() {
        System.out.println(name + " is eating dog food");
    }
    
    public void bark() {
        System.out.println("Woof!");
    }
}
```

### 方法重写规则

```java
// 1. 方法签名必须相同
// 2. 返回类型相同或为子类（协变返回类型）
// 3. 访问权限不能更严格
// 4. 不能抛出新的检查异常或更广的异常

class Parent {
    protected Number getValue() {  // 返回Number
        return 0;
    }
}

class Child extends Parent {
    @Override
    public Integer getValue() {    // 返回Integer（Number子类）
        return 42;
    }
}
```

## 多态

### 向上转型

子类对象赋给父类引用，自动转换。

```java
Animal animal = new Dog("Buddy", "Labrador");  // 向上转型
animal.eat();              // 调用Dog的eat()（动态绑定）
// animal.bark();          // 编译错误！Animal没有bark方法
```

### 向下转型

父类引用转为子类引用，需显式转换，可能失败。

```java
Animal animal = new Dog("Buddy", "Labrador");

// 不安全的转换
Dog dog = (Dog) animal;    // OK
dog.bark();

// 安全转换：先判断类型
if (animal instanceof Dog) {
    Dog dog = (Dog) animal;
    dog.bark();
}

// Java 14+ 模式匹配
if (animal instanceof Dog dog) {  // 自动转换并声明变量
    dog.bark();
}
```

### 动态绑定

方法调用在运行时根据实际对象类型决定，而非引用类型。

```java
class Shape {
    public void draw() {
        System.out.println("Drawing shape");
    }
}

class Circle extends Shape {
    @Override
    public void draw() {
        System.out.println("Drawing circle");
    }
}

Shape shape = new Circle();
shape.draw();  // 输出：Drawing circle（运行时绑定）
```

**注意：** 静态方法、final方法、private方法不支持动态绑定。

## 抽象类

抽象类不能实例化，可包含抽象方法和具体方法。

```java
public abstract class Shape {
    private String color;
    
    public Shape(String color) {
        this.color = color;
    }
    
    // 抽象方法（无实现）
    public abstract double area();
    public abstract double perimeter();
    
    // 具体方法
    public String getColor() {
        return color;
    }
}

public class Circle extends Shape {
    private double radius;
    
    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }
    
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public double perimeter() {
        return 2 * Math.PI * radius;
    }
}
```

## 接口

接口定义契约，类可实现多个接口。

### 接口定义

```java
public interface Flyable {
    // 抽象方法（默认public abstract）
    void fly();
    
    // 默认方法（Java 8+）
    default void land() {
        System.out.println("Landing...");
    }
    
    // 静态方法（Java 8+）
    static void checkAltitude(int altitude) {
        if (altitude < 0) {
            throw new IllegalArgumentException("Invalid altitude");
        }
    }
    
    // 常量（默认public static final）
    int MAX_ALTITUDE = 10000;
}

public class Bird implements Flyable {
    @Override
    public void fly() {
        System.out.println("Bird is flying");
    }
}
```

### 接口多实现

```java
interface Swimmable {
    void swim();
}

interface Runnable {
    void run();
}

// 一个类可实现多个接口
class Duck implements Flyable, Swimmable, Runnable {
    @Override
    public void fly() { /* ... */ }
    
    @Override
    public void swim() { /* ... */ }
    
    @Override
    public void run() { /* ... */ }
}
```

## 枚举

类型安全的常量集合。

```java
// 简单枚举
public enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

Day today = Day.MONDAY;

// 带属性和方法的枚举
public enum Planet {
    EARTH(5.976e+24, 6.37814e6),
    MARS(6.421e+23, 3.3972e6);
    
    private final double mass;
    private final double radius;
    
    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }
    
    public double getMass() { return mass; }
    public double getRadius() { return radius; }
    
    public double surfaceGravity() {
        return 6.67300E-11 * mass / (radius * radius);
    }
}

// 使用
for (Planet p : Planet.values()) {
    System.out.println(p + ": " + p.surfaceGravity());
}
```

## 内部类

### 成员内部类

```java
public class Outer {
    private int outerField = 10;
    
    public class Inner {
        public void accessOuter() {
            System.out.println(outerField);  // 可访问外部类成员
        }
    }
    
    public void createInner() {
        Inner inner = new Inner();
        inner.accessOuter();
    }
}

// 外部创建内部类对象
Outer outer = new Outer();
Outer.Inner inner = outer.new Inner();
```

### 静态内部类

不依赖外部类实例，类似独立类。

```java
public class Outer {
    private static int staticField = 10;
    
    public static class StaticInner {
        public void print() {
            System.out.println(staticField);  // 只能访问静态成员
        }
    }
}

// 创建静态内部类对象
Outer.StaticInner inner = new Outer.StaticInner();
```

### 局部内部类

方法内定义的类。

```java
public void method() {
    class LocalClass {
        public void print() {
            System.out.println("Local class");
        }
    }
    
    LocalClass local = new LocalClass();
    local.print();
}
```

### 匿名内部类

无名称的一次性类，常用于接口实现。

```java
// 实现接口
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Running...");
    }
};

// Lambda表达式（Java 8+，更简洁）
Runnable r2 = () -> System.out.println("Running...");
```

## Lambda表达式（Java 8+）

函数式编程特性，简化匿名类。

```java
// 语法：(参数) -> 表达式
// 或：(参数) -> { 语句块 }

// 无参数
Runnable r = () -> System.out.println("Hello");

// 一个参数
Consumer<String> print = s -> System.out.println(s);
Consumer<String> print2 = (String s) -> System.out.println(s);

// 多个参数
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

// 多条语句
Comparator<String> cmp = (s1, s2) -> {
    int len1 = s1.length();
    int len2 = s2.length();
    return Integer.compare(len1, len2);
};

// 使用
List<String> list = Arrays.asList("apple", "banana", "cherry");
list.forEach(s -> System.out.println(s));      // 遍历
list.sort((s1, s2) -> s1.compareTo(s2));       // 排序
list.stream().filter(s -> s.startsWith("a"))   // Stream API
    .forEach(System.out::println);
```

## Stream API（Java 8+）

函数式风格的集合处理，链式操作，延迟计算。

```java
import java.util.stream.*;

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 过滤、映射、收集
List<Integer> evenSquares = numbers.stream()
    .filter(n -> n % 2 == 0)         // 过滤偶数
    .map(n -> n * n)                 // 平方
    .collect(Collectors.toList());   // 收集为List

// 查找
Optional<Integer> first = numbers.stream()
    .filter(n -> n > 5)
    .findFirst();

// 聚合
int sum = numbers.stream()
    .reduce(0, (a, b) -> a + b);     // 求和

// 统计
IntSummaryStatistics stats = numbers.stream()
    .mapToInt(Integer::intValue)
    .summaryStatistics();
System.out.println("Average: " + stats.getAverage());

// 并行Stream
long count = numbers.parallelStream()
    .filter(n -> n % 2 == 0)
    .count();
```

**常用操作：**
- 中间操作（返回Stream）：`filter`、`map`、`flatMap`、`sorted`、`distinct`
- 终端操作（返回结果）：`forEach`、`collect`、`reduce`、`count`、`findFirst`

## 方法引用（Java 8+）

Lambda的简化写法。

```java
List<String> list = Arrays.asList("a", "b", "c");

// Lambda
list.forEach(s -> System.out.println(s));

// 方法引用（更简洁）
list.forEach(System.out::println);

// 四种方法引用
// 1. 静态方法引用
Function<String, Integer> parser = Integer::parseInt;

// 2. 实例方法引用
String str = "hello";
Supplier<Integer> lengthGetter = str::length;

// 3. 类型方法引用
BiPredicate<String, String> equals = String::equals;

// 4. 构造函数引用
Supplier<List<String>> listFactory = ArrayList::new;
```

## Optional（Java 8+）

处理null的优雅方式，避免NullPointerException。

```java
// 创建Optional
Optional<String> opt1 = Optional.of("value");      // 不能为null
Optional<String> opt2 = Optional.ofNullable(null); // 可以为null
Optional<String> opt3 = Optional.empty();          // 空Optional

// 判断是否有值
if (opt1.isPresent()) {
    String value = opt1.get();
}

// 更优雅的写法
opt1.ifPresent(s -> System.out.println(s));

// 默认值
String value = opt2.orElse("default");
String value2 = opt2.orElseGet(() -> "computed default");
String value3 = opt2.orElseThrow(() -> new RuntimeException());

// 链式调用
String result = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");

// flatMap（处理嵌套Optional）
Optional<Address> address = Optional.ofNullable(user)
    .flatMap(User::getAddressOptional);
```

**使用原则：**
- 方法返回值用Optional表示可能为空
- Optional不作为字段或参数
- `Optional.get()` 前必须检查

## 注解

元数据，用于编译器检查、代码生成、运行时处理。

### 内置注解

```java
// 1. @Override：检查方法重写
@Override
public String toString() {
    return "...";
}

// 2. @Deprecated：标记过时
@Deprecated
public void oldMethod() {
    // ...
}

// 3. @SuppressWarnings：抑制警告
@SuppressWarnings("unchecked")
public void method() {
    List list = new ArrayList();
}

// 4. @FunctionalInterface：函数式接口
@FunctionalInterface
public interface MyFunction {
    void apply();  // 只能有一个抽象方法
}

// 5. @SafeVarargs：抑制泛型可变参数警告
@SafeVarargs
public static <T> void print(T... items) {
    // ...
}
```

### 自定义注解

```java
// 定义注解
@Retention(RetentionPolicy.RUNTIME)  // 运行时可见
@Target(ElementType.METHOD)          // 用于方法
public @interface MyAnnotation {
    String value() default "";
    int priority() default 0;
}

// 使用注解
public class Example {
    @MyAnnotation(value = "test", priority = 1)
    public void method() {
        // ...
    }
}

// 运行时读取注解
Method method = Example.class.getMethod("method");
if (method.isAnnotationPresent(MyAnnotation.class)) {
    MyAnnotation ann = method.getAnnotation(MyAnnotation.class);
    System.out.println(ann.value());
}
```

## 反射

运行时检查和操作类、方法、字段。强大但性能低，谨慎使用。

### 基本反射操作

```java
// 获取Class对象
Class<?> clazz1 = String.class;
Class<?> clazz2 = "hello".getClass();
Class<?> clazz3 = Class.forName("java.lang.String");

// 创建对象
Constructor<?> constructor = clazz.getConstructor(String.class);
Object obj = constructor.newInstance("value");

// 调用方法
Method method = clazz.getMethod("substring", int.class, int.class);
Object result = method.invoke(obj, 0, 5);

// 访问字段
Field field = clazz.getDeclaredField("value");
field.setAccessible(true);  // 访问私有字段
Object fieldValue = field.get(obj);
```

### 反射应用场景

```java
// 1. 框架开发（Spring IOC容器）
// 2. 动态代理
// 3. 注解处理
// 4. 测试框架（JUnit）
// 5. ORM框架（Hibernate）
```

**注意：** 反射破坏封装，性能差，仅在必要时使用。

## 泛型

类型参数化，提供编译期类型安全。

### 泛型类

```java
public class Box<T> {
    private T value;
    
    public void set(T value) {
        this.value = value;
    }
    
    public T get() {
        return value;
    }
}

// 使用
Box<String> stringBox = new Box<>();  // 菱形语法（Java 7+）
stringBox.set("Hello");
String value = stringBox.get();       // 无需强制转换
```

### 泛型方法

```java
public class Utils {
    // 泛型方法
    public static <T> void swap(T[] array, int i, int j) {
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    
    // 有界类型参数
    public static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }
}

// 使用
Integer[] arr = {1, 2, 3};
Utils.swap(arr, 0, 1);
Integer max = Utils.max(10, 20);
```

### 通配符

```java
// ? 表示未知类型

// 无界通配符
public void printList(List<?> list) {
    for (Object obj : list) {
        System.out.println(obj);
    }
}

// 上界通配符（extends）
public double sumNumbers(List<? extends Number> list) {
    double sum = 0;
    for (Number num : list) {
        sum += num.doubleValue();
    }
    return sum;
}

// 下界通配符（super）
public void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}
```

**PECS原则：** Producer Extends, Consumer Super
- 读取用 `<? extends T>`
- 写入用 `<? super T>`

## 设计模式基础

### 单例模式

```java
// 饿汉式（线程安全，类加载时初始化）
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        return INSTANCE;
    }
}

// 懒汉式（双重检查锁）
public class LazySingleton {
    private static volatile LazySingleton instance;
    
    private LazySingleton() {}
    
    public static LazySingleton getInstance() {
        if (instance == null) {
            synchronized (LazySingleton.class) {
                if (instance == null) {
                    instance = new LazySingleton();
                }
            }
        }
        return instance;
    }
}

// 枚举单例（推荐，最简洁）
public enum SingletonEnum {
    INSTANCE;
    
    public void doSomething() {
        // ...
    }
}
```

### 工厂模式

```java
// 简单工厂
public class ShapeFactory {
    public static Shape createShape(String type) {
        switch (type) {
            case "circle":
                return new Circle();
            case "rectangle":
                return new Rectangle();
            default:
                throw new IllegalArgumentException("Unknown type");
        }
    }
}

// 使用
Shape shape = ShapeFactory.createShape("circle");
```

## 最佳实践

1. **优先接口而非抽象类**：更灵活
2. **使用泛型**：类型安全，避免强制转换
3. **重写equals必须重写hashCode**：HashMap/HashSet要求
4. **不可变类用final**：String、包装类都是final
5. **组合优于继承**：降低耦合
6. **面向接口编程**：依赖抽象而非具体实现
7. **遵循SOLID原则**：单一职责、开闭原则等
8. **使用Lambda和Stream**：代码更简洁
9. **合理使用Optional**：避免null检查
10. **反射仅必要时用**：性能开销大

**核心：** Java注重类型安全和面向对象设计，充分利用语言特性。


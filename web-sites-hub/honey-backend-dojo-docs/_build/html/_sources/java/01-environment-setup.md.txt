# 01-Java环境搭建

## JDK安装

### JDK版本选择

LTS（长期支持）版本：

- **Java 8（LTS）**：2014年发布，企业广泛使用
- **Java 11（LTS）**：2018年发布，模块化系统
- **Java 17（LTS）**：2021年发布，密封类、记录类

学习环境：Java 17，生产环境：Java 11或Java 17。

### Java 17核心特性

**密封类（Sealed Classes）：**
```java
// 限制继承范围
public sealed class Shape permits Circle, Rectangle {}

public final class Circle extends Shape {}
public non-sealed class Rectangle extends Shape {}
```

**记录类（Records）：**
```java
// 不可变数据类
public record Point(int x, int y) {}
```

### 安装JDK

**Linux（Ubuntu/Debian）：**
```bash
# 安装OpenJDK 17
sudo apt update
sudo apt install openjdk-17-jdk

# 验证安装
java -version
javac -version
```

**macOS：**
```bash
# 使用Homebrew
brew install openjdk@17

# 配置环境变量
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Windows：**
1. 下载Oracle JDK或OpenJDK
2. 安装并配置JAVA_HOME环境变量
3. 添加%JAVA_HOME%\bin到PATH

### 环境变量配置

```bash
# Linux/macOS (~/.bashrc 或 ~/.zshrc)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib

# 验证
echo $JAVA_HOME
java -version
```

## 开发工具

### IntelliJ IDEA

JetBrains出品，社区版免费。

**特性：**
- 智能代码补全
- 重构功能
- 内置调试器和性能分析
- 集成Maven/Gradle
- Git版本控制

**快捷键（macOS/Windows）：**
- `Cmd/Ctrl + N`：快速查找类
- `Cmd/Ctrl + Shift + N`：快速查找文件
- `Cmd/Ctrl + Alt + L`：格式化代码
- `Cmd/Ctrl + /`：注释/取消注释
- `Shift + F10/F9`：运行/调试

### Eclipse

开源Java IDE，功能完整。

**特性：**
- 免费开源
- 插件生态丰富
- 资源占用较小

### VS Code

轻量级编辑器，通过插件支持Java。

**必装插件：**
- Extension Pack for Java
- Debugger for Java
- Maven for Java

## 构建工具

### Maven

基于XML的项目管理工具，依赖管理自动化。

**pom.xml示例：**
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0-SNAPSHOT</version>
    
    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.9.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

**常用命令：**
```bash
mvn clean           # 清理
mvn compile         # 编译
mvn test            # 测试
mvn package         # 打包
mvn install         # 安装到本地仓库
mvn clean package   # 组合命令
```

### Gradle

基于Groovy/Kotlin的现代构建工具，配置更简洁。

**build.gradle示例：**
```groovy
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}

dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.9.0'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}
```

**常用命令：**
```bash
gradle clean        # 清理
gradle build        # 构建
gradle test         # 测试
gradle run          # 运行
./gradlew build     # 使用wrapper
```

## Hello World

### 基本程序结构

```java
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### 编译和运行

```bash
# 编译
javac HelloWorld.java

# 运行
java HelloWorld

# 输出
Hello, World!
```

### 带包的程序

```java
// src/main/java/com/example/App.java
package com.example;

public class App {
    public static void main(String[] args) {
        System.out.println("Hello from package!");
    }
}
```

```bash
# 编译（在项目根目录）
javac -d out src/main/java/com/example/App.java

# 运行
java -cp out com.example.App
```

## 调试工具

### jdb（命令行调试器）

```bash
# 编译时加调试信息
javac -g HelloWorld.java

# 启动调试
jdb HelloWorld

# 常用命令
stop in HelloWorld.main  # 设置断点
run                      # 运行
print variable           # 打印变量
step                     # 单步执行
next                     # 下一行
cont                     # 继续执行
quit                     # 退出
```

### IntelliJ IDEA调试

- F8：单步跳过
- F7：单步进入
- Shift + F8：单步跳出
- F9：继续执行
- Cmd/Ctrl + F8：切换断点
- Alt + F9：运行到光标

## 常用工具

### jshell（Java 9+）

交互式Java REPL，快速验证代码。

```bash
# 启动
jshell

# 使用
jshell> int x = 10;
jshell> System.out.println(x * 2);
20
jshell> /exit
```

### jconsole/jvisualvm

JVM监控和性能分析工具。

```bash
# 启动jconsole
jconsole

# 启动jvisualvm
jvisualvm
```

**监控内容：**
- 堆内存使用
- 线程状态
- CPU占用
- GC活动

## 编码规范

### 命名约定

```java
// 类名：大驼峰
public class StudentInfo {}

// 方法/变量：小驼峰
public void calculateSum() {}
private int studentAge;

// 常量：全大写+下划线
public static final int MAX_SIZE = 100;

// 包名：全小写
package com.example.myapp;

// 接口：大驼峰（可选I前缀）
public interface Runnable {}
public interface IService {}
```

### 代码风格

```java
// 缩进：4空格
if (condition) {
    statement;
}

// 大括号：K&R风格
public void method() {
    // ...
}

// 一行一条语句
int a = 1;
int b = 2;
```

## 项目结构

### Maven标准结构

```
my-app/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/           # Java源代码
│   │   │   └── com/example/
│   │   └── resources/      # 资源文件
│   └── test/
│       ├── java/           # 测试代码
│       └── resources/      # 测试资源
└── target/                 # 编译输出
```

### Gradle标准结构

```
my-app/
├── build.gradle
├── settings.gradle
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
└── build/                  # 编译输出
```


## Java 17完整特性列表

### 语言特性

**1. 密封类（Sealed Classes - JEP 409）**
- 限制类的继承层次
- 编译期完整性检查
- switch穷尽性分析

**2. 记录类（Records - JEP 395）**  
- 不可变数据载体
- 自动生成样板代码
- 模式匹配支持

**3. 模式匹配（Pattern Matching - JEP 406）**
- instanceof自动转型
- switch表达式扩展
- 减少类型转换代码

**4. 文本块（Text Blocks - JEP 378）**
- 多行字符串字面量
- 保留格式和缩进
- 简化JSON/SQL/HTML编写

### API增强

**Stream增强：**
```java
// toList()快捷方法
List<String> list = stream.toList();

// mapMulti替代flatMap（性能更好）
stream.mapMulti((item, consumer) -> {
    consumer.accept(item);
    consumer.accept(item * 2);
});
```

**RandomGenerator统一API：**
```java
import java.util.random.*;

RandomGenerator rng = RandomGenerator.of("L128X256MixRandom");
int value = rng.nextInt(100);
```

**Foreign Function & Memory API（孵化）：**
- 替代JNI调用本地代码
- 直接内存访问
- 更安全的本地互操作

### JVM改进

**ZGC和Shenandoah GC正式版：**
- 低延迟垃圾收集器
- 适合大堆内存场景

**强封装JDK内部：**
```bash
# 访问内部API需要显式声明
java --add-opens java.base/java.lang=ALL-UNNAMED App
```

**性能优化：**
- 向量API（孵化）：SIMD支持
- 增强伪随机数生成器
- macOS ARM64支持

### 从Java 11到17的演进

| 版本 | 关键特性 |
|------|---------|
| Java 12 | switch表达式（Preview） |
| Java 13 | 文本块（Preview） |
| Java 14 | instanceof模式（Preview）、Records（Preview）、NPE增强 |
| Java 15 | 密封类（Preview）、文本块（正式） |
| Java 16 | instanceof模式（正式）、Records（正式）、Stream.toList() |
| Java 17 | 密封类（正式）、模式匹配增强、LTS版本 |

**升级建议：**
- 从Java 8升级：需要处理模块化、弃用API
- 从Java 11升级：主要是新特性，兼容性好
- 新项目直接用Java 17

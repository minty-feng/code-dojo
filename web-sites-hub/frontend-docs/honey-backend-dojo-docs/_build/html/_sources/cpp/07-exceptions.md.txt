# 07-异常处理

异常处理是C++的错误处理机制，通过 `throw`/`catch` 实现错误传播。比返回错误码更清晰，但有性能开销。

## 异常基础

异常将错误检测和处理分离。`throw` 抛出异常，`catch` 捕获处理。未捕获异常导致程序终止。

### 异常抛出

`throw` 可抛出任何类型对象，但推荐使用标准异常类或其派生类。异常对象会被复制。


```cpp
#include <stdexcept>

// 抛出标准异常
void divide(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero");
    }
    return a / b;
}

// 抛出自定义异常
class CustomException : public std::exception {
private:
    std::string message;
public:
    CustomException(const std::string& msg) : message(msg) {}
    const char* what() const noexcept override {
        return message.c_str();
    }
};

void riskyFunction() {
    throw CustomException("Something went wrong");
}
```

### 异常捕获

`catch` 按类型匹配异常，从上到下顺序检查。派生类应在基类前，`catch(...)` 捕获所有异常。

```cpp
try {
    divide(10, 0);
} catch (const std::invalid_argument& e) {
    std::cout << "Invalid argument: " << e.what() << std::endl;
} catch (const std::exception& e) {
    std::cout << "Standard exception: " << e.what() << std::endl;
} catch (...) {
    std::cout << "Unknown exception caught" << std::endl;
}
```

### 异常规范

`noexcept` 声明函数不抛异常，编译器可优化。违反`noexcept`会调用 `std::terminate()`。

```cpp
// C++11之前的异常规范（已废弃）
void oldFunction() throw(std::runtime_error);

// C++11的noexcept规范
void safeFunction() noexcept;  // 不抛出异常
void mayThrowFunction() noexcept(false);  // 可能抛出异常

// 条件noexcept
template<typename T>
void templateFunction(T value) noexcept(std::is_nothrow_copy_constructible_v<T>);
```

## 标准异常类

C++标准库提供异常类层次，所有标准异常继承自 `std::exception`。分为逻辑错误和运行时错误。

### 标准异常层次

标准异常形成树状继承关系，捕获基类可同时捕获所有派生类异常。


```text
std::exception
├── std::logic_error
│   ├── std::invalid_argument
│   ├── std::domain_error
│   ├── std::length_error
│   └── std::out_of_range
├── std::runtime_error
│   ├── std::range_error
│   ├── std::overflow_error
│   ├── std::underflow_error
│   └── std::system_error
└── std::bad_alloc
```

### 常用异常类型

选择合适的异常类型传达错误信息。逻辑错误表示程序bug，运行时错误表示外部因素导致的失败。

```cpp
// 逻辑错误
throw std::invalid_argument("Invalid parameter");
throw std::domain_error("Domain error");
throw std::length_error("Length error");
throw std::out_of_range("Index out of range");

// 运行时错误
throw std::range_error("Range error");
throw std::overflow_error("Overflow");
throw std::underflow_error("Underflow");
throw std::system_error(std::make_error_code(std::errc::no_such_file_or_directory));

// 内存错误
throw std::bad_alloc();
```

## RAII与异常安全

RAII确保异常发生时资源正确释放。异常安全分三个级别：基本保证、强保证、无异常保证。

### 异常安全保证

异常安全描述函数在异常时的行为保证。级别越高越安全，但实现难度也越大。


```cpp
class Resource {
private:
    int* data;
    size_t size;
    
public:
    // 基本异常安全
    Resource(size_t s) : size(s) {
        data = new int[size];
        // 如果这里抛出异常，析构函数不会被调用
        // 但构造函数中的分配会被清理
    }
    
    // 强异常安全
    Resource(const Resource& other) : size(other.size) {
        int* newData = new int[size];
        try {
            std::copy(other.data, other.data + size, newData);
        } catch (...) {
            delete[] newData;
            throw;  // 重新抛出异常
        }
        data = newData;
    }
    
    ~Resource() {
        delete[] data;
    }
};
```

### 智能指针与异常
```cpp
#include <memory>

void safeFunction() {
    // 使用智能指针确保异常安全
    auto ptr = std::make_unique<int>(42);
    
    // 即使这里抛出异常，智能指针也会自动清理
    riskyOperation();
    
    // 正常使用
    std::cout << *ptr << std::endl;
}
```

## 异常处理最佳实践

### 异常安全设计
```cpp
class SafeContainer {
private:
    std::vector<int> data;
    
public:
    // 强异常安全：要么成功，要么保持原状态
    void insert(int value) {
        std::vector<int> newData = data;  // 复制
        newData.push_back(value);         // 修改副本
        
        // 如果这里抛出异常，原data不受影响
        data = std::move(newData);        // 原子操作
    }
    
    // 无异常保证：使用noexcept
    void clear() noexcept {
        data.clear();
    }
};
```

### 异常传播
```cpp
// 让异常自然传播
void function1() {
    throw std::runtime_error("Error in function1");
}

void function2() {
    function1();  // 异常会传播到调用者
}

// 捕获并重新抛出
void function3() {
    try {
        function1();
    } catch (const std::exception& e) {
        std::cout << "Caught in function3: " << e.what() << std::endl;
        throw;  // 重新抛出原异常
    }
}

// 抛出新异常
void function4() {
    try {
        function1();
    } catch (const std::exception& e) {
        throw std::runtime_error("Wrapped: " + std::string(e.what()));
    }
}
```

## 异常与构造函数

### 构造函数中的异常
```cpp
class SafeClass {
private:
    std::unique_ptr<int> ptr1;
    std::unique_ptr<int> ptr2;
    
public:
    SafeClass(int value1, int value2) 
        : ptr1(std::make_unique<int>(value1)) {
        
        // 如果这里抛出异常，ptr1会被自动清理
        ptr2 = std::make_unique<int>(value2);
    }
    
    // 如果构造函数抛出异常，析构函数不会被调用
    // 但成员对象的析构函数会被调用
};
```

### 异常与析构函数
```cpp
class SafeDestructor {
public:
    ~SafeDestructor() noexcept {
        try {
            // 清理资源
            cleanup();
        } catch (...) {
            // 析构函数中不应该抛出异常
            // 记录错误但不重新抛出
            std::cerr << "Error in destructor" << std::endl;
        }
    }
    
private:
    void cleanup() {
        // 可能抛出异常的清理操作
    }
};
```

## 自定义异常类

### 继承标准异常
```cpp
class DatabaseException : public std::runtime_error {
private:
    int errorCode;
    
public:
    DatabaseException(const std::string& message, int code)
        : std::runtime_error(message), errorCode(code) {}
    
    int getErrorCode() const {
        return errorCode;
    }
    
    const char* what() const noexcept override {
        static std::string fullMessage = 
            std::runtime_error::what() + " (Code: " + std::to_string(errorCode) + ")";
        return fullMessage.c_str();
    }
};
```

### 异常链
```cpp
class ChainedException : public std::exception {
private:
    std::string message;
    std::exception_ptr cause;
    
public:
    ChainedException(const std::string& msg, std::exception_ptr c = nullptr)
        : message(msg), cause(c) {}
    
    const char* what() const noexcept override {
        return message.c_str();
    }
    
    std::exception_ptr getCause() const {
        return cause;
    }
    
    void rethrowCause() const {
        if (cause) {
            std::rethrow_exception(cause);
        }
    }
};
```

## 异常处理模式

### 异常处理装饰器
```cpp
template<typename Func>
auto withExceptionHandling(Func&& func) {
    return [func = std::forward<Func>(func)](auto&&... args) {
        try {
            return func(std::forward<decltype(args)>(args)...);
        } catch (const std::exception& e) {
            std::cerr << "Exception caught: " << e.what() << std::endl;
            throw;
        }
    };
}

// 使用
auto safeDivide = withExceptionHandling([](int a, int b) {
    if (b == 0) throw std::invalid_argument("Division by zero");
    return a / b;
});
```

### 异常安全包装器
```cpp
template<typename T>
class ExceptionSafeWrapper {
private:
    T value;
    bool valid;
    
public:
    ExceptionSafeWrapper(T&& v) : value(std::move(v)), valid(true) {}
    
    template<typename Func>
    auto apply(Func&& func) -> ExceptionSafeWrapper<decltype(func(value))> {
        if (!valid) {
            throw std::runtime_error("Wrapper is invalid");
        }
        
        try {
            return ExceptionSafeWrapper<decltype(func(value))>(func(value));
        } catch (...) {
            valid = false;
            throw;
        }
    }
    
    T& get() {
        if (!valid) {
            throw std::runtime_error("Wrapper is invalid");
        }
        return value;
    }
    
    bool isValid() const {
        return valid;
    }
};
```

## 异常处理最佳实践

### 何时使用异常

**适合使用异常：**
```cpp
// ✅ 构造函数失败（无法返回错误码）
class File {
public:
    File(const char* name) {
        fp = fopen(name, "r");
        if (!fp) {
            throw std::runtime_error("Cannot open file");
        }
    }
private:
    FILE* fp;
};

// ✅ 不可恢复的错误
void processData(const Data& data) {
    if (!data.isValid()) {
        throw std::invalid_argument("Invalid data");
    }
    // ...
}

// ✅ 跨多层函数传播错误
void deepFunction() {
    if (error) throw MyException();
}
void middleFunction() { deepFunction(); }
void topFunction() {
    try { middleFunction(); }
    catch (const MyException& e) { /* 处理 */ }
}
```

**不适合使用异常：**
```cpp
// ❌ 正常控制流
void findElement(const vector<int>& vec, int target) {
    for (int x : vec) {
        if (x == target) {
            throw FoundException();  // 错误！用return
        }
    }
}

// ❌ 预期的错误（用错误码或optional）
std::optional<int> parseInt(const string& s) {
    try {
        return std::stoi(s);
    } catch (...) {
        return std::nullopt;  // 解析失败是预期的
    }
}

// ❌ 性能关键路径
void hotPath(int x) {
    if (x < 0) throw Ex();  // 异常有开销
}
```

### 性能考虑

**异常的成本：**
```cpp
// 无异常路径：几乎零开销（现代编译器）
void normal() {
    // 正常执行，无性能损失
}

// 抛出异常：成本高
void throwing() {
    throw std::exception();  // 栈展开、对象析构、查找处理器
}

// 时间对比（近似）：
// - 正常返回：1ns
// - 抛出并捕获异常：1000ns - 10000ns
```

**优化建议：**
```cpp
// ✅ 1. noexcept用于不抛异常的函数
void fastFunction() noexcept {
    // 编译器可做更多优化
}

// ✅ 2. 移动操作标记noexcept（容器性能关键）
class MyClass {
public:
    MyClass(MyClass&& other) noexcept {
        // vector等容器在重新分配时会检查noexcept
        // 如果没有，会使用拷贝而非移动
    }
};

// ✅ 3. 异常只用于异常情况
// 正常错误（如文件不存在）用错误码或optional

// ✅ 4. catch引用避免切片
try {
    // ...
} catch (const std::exception& e) {  // 引用，保留派生类信息
    // ...
}
```

### 异常 vs 错误码

| 特性 | 异常 | 错误码 |
|------|------|--------|
| 可读性 | 高（分离错误处理） | 低（混杂正常逻辑） |
| 强制处理 | 否（可能忘记catch） | 是（必须检查返回值） |
| 性能 | 正常路径快，异常路径慢 | 一致 |
| 构造函数 | 唯一选择 | 不可用 |
| 资源管理 | 自动（栈展开） | 需手动清理 |
| 跨层传播 | 容易 | 繁琐 |

**选择建议：**
- 库接口：异常（用户可选择处理方式）
- 底层/实时系统：错误码（性能可预测）
- 构造函数：异常（无法返回错误码）
- C接口：错误码（C不支持异常）
- 现代C++：优先异常 + RAII

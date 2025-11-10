# 06-内存管理

## 内存模型

内存管理是C++编程中的核心概念，理解内存模型对于编写高效、安全的程序至关重要。C++提供了直接的内存控制能力，这既是其优势也是其挑战。掌握内存管理技术可以避免内存泄漏、提高程序性能，并编写出更加健壮的代码。

### 内存布局
程序运行时，内存被划分为不同的区域，每个区域有不同的用途和特性。理解这些区域的特点有助于更好地管理内存。

**代码段（Text Segment）：**
- 存储程序的机器码指令
- 只读区域，程序运行时不能修改
- 通常位于内存的低地址区域
- 包含程序的执行逻辑

**数据段（Data Segment）：**
- 存储已初始化的全局变量和静态变量
- 程序启动时分配，程序结束时释放
- 分为只读数据段和可读写数据段
- 包含程序的全局状态信息

**BSS段（Block Started by Symbol）：**
- 存储未初始化的全局变量和静态变量
- 程序启动时自动初始化为0
- 不占用可执行文件的空间
- 提高程序加载效率

**堆（Heap）：**
- 动态分配的内存区域
- 通过new/delete或malloc/free管理
- 内存分配和释放的时间不确定
- 需要程序员手动管理

**栈（Stack）：**
- 存储局部变量和函数调用信息
- 自动管理，后进先出（LIFO）
- 内存分配和释放速度快
- 大小有限，通常几MB

### 栈内存
栈内存是自动管理的内存区域，具有高效、安全的特点。它是函数调用和局部变量存储的主要场所。

**栈内存的特点：**
- 自动分配和释放，无需程序员干预
- 分配速度快，只需要移动栈指针
- 内存连续，缓存友好
- 大小有限，通常几MB
- 后进先出，符合函数调用模式

**栈内存的使用：**
```cpp
void function() {
    int localVar = 10;              // 栈上分配
    int array[100];                 // 栈上数组
    // 函数结束时自动释放
}
```

**栈内存的优势：**
- 无需手动管理，避免内存泄漏
- 分配速度快，性能优秀
- 自动清理，异常安全
- 内存局部性好，缓存命中率高

**栈内存的限制：**
- 大小有限，不适合大对象
- 生命周期固定，灵活性差
- 递归深度受限
- 不能动态调整大小

### 堆内存
堆内存是动态分配的内存区域，提供了更大的灵活性，但也带来了更多的管理复杂性。

**堆内存的特点：**
- 手动管理，程序员控制分配和释放
- 大小灵活，可以分配任意大小的内存
- 生命周期灵活，可以跨函数使用
- 分配速度相对较慢
- 可能产生内存碎片

**堆内存的使用：**
```cpp
void function() {
    int* ptr = new int(10);         // 堆上分配
    int* array = new int[100];      // 堆上数组
    
    delete ptr;                     // 释放单个对象
    delete[] array;                 // 释放数组
}
```

**堆内存的优势：**
- 大小灵活，适合大对象
- 生命周期灵活，可以跨函数使用
- 可以动态调整大小
- 适合不确定大小的数据结构

**堆内存的挑战：**
- 需要手动管理，容易出错
- 可能产生内存泄漏
- 分配速度较慢
- 可能产生内存碎片

## 动态内存分配

动态内存分配是C++中重要的内存管理技术，正确使用可以大大提高程序的灵活性。通过动态分配，可以在运行时决定需要多少内存，这对于处理不确定大小的数据特别有用。

### new和delete
new和delete是C++的动态内存分配操作符，提供了类型安全的内存管理。它们比C语言的malloc和free更加安全，因为它们会自动调用构造函数和析构函数。

**new和delete的优势：**
- 类型安全，编译器检查类型匹配
- 自动调用构造函数和析构函数
- 支持异常处理
- 与C++对象模型集成良好

**单个对象分配：**
```cpp
int* ptr = new int(42);    // 分配并初始化
delete ptr;                // 释放内存
```

**数组分配：**
```cpp
int* arr = new int[10];    // 分配数组
delete[] arr;              // 释放数组
```

**对象分配：**
```cpp
MyClass* obj = new MyClass();  // 调用构造函数
delete obj;                    // 调用析构函数
```

**对象数组分配：**
```cpp
MyClass* objs = new MyClass[5];  // 调用构造函数
delete[] objs;                   // 调用析构函数
```

**注意事项：**
- new和delete必须配对使用
- new[]和delete[]必须配对使用
- 不要混用new/delete和malloc/free
- 释放后要将指针设为nullptr

### 内存泄漏
内存泄漏是动态内存管理中的常见问题，需要特别注意。内存泄漏会导致程序占用越来越多的内存，最终可能导致系统崩溃。

**内存泄漏的原因：**
- 忘记调用delete释放内存
- 异常导致delete未执行
- 指针丢失，无法释放内存
- 循环引用导致无法释放

**错误示例：**
```cpp
void badFunction() {
    int* ptr = new int(42);
    // 忘记delete ptr;
    // 内存泄漏！
}
```

**防止内存泄漏的方法：**
- 使用RAII（资源获取即初始化）
- 使用智能指针
- 异常安全编程
- 代码审查和测试

**正确示例：**
```cpp
class Resource {
private:
    int* data;
public:
    Resource() : data(new int(42)) {}
    ~Resource() { delete data; }
};
```

### 异常安全
异常安全是动态内存管理中的重要概念，确保程序在异常情况下也能正确管理内存。

**异常安全问题：**
```cpp
void riskyFunction() {
    int* ptr1 = new int(42);
    int* ptr2 = new int(84);        // 如果这里抛出异常，ptr1泄漏
    
    delete ptr1;
    delete ptr2;
}
```

**异常安全解决方案：**
```cpp
void safeFunction() {
    unique_ptr<int> ptr1(new int(42));
    unique_ptr<int> ptr2(new int(84));
    // 即使抛出异常，智能指针也会自动释放
}
```

**异常安全保证级别：**
- 基本保证：不泄漏资源，对象处于有效状态
- 强保证：操作要么成功，要么保持原状态
- 无异常保证：操作不会抛出异常

## 智能指针

智能指针自动管理内存，避免手动 `new/delete` 的风险。C++11 提供三种智能指针应对不同场景。

### unique_ptr详解

`unique_ptr` 独占所有权，不可拷贝只能移动。适用于明确单一所有者的场景，零开销。
```cpp
#include <memory>

// 创建
unique_ptr<int> ptr1(new int(42));
auto ptr2 = make_unique<int>(42);

// 移动语义
unique_ptr<int> ptr3 = move(ptr1);  // ptr1变为nullptr

// 自定义删除器
auto deleter = [](int* p) { 
    cout << "Deleting: " << *p << endl; 
    delete p; 
};
unique_ptr<int, decltype(deleter)> ptr4(new int(42), deleter);

// 数组版本
unique_ptr<int[]> arr = make_unique<int[]>(10);
```

### shared_ptr详解
```cpp
// 创建
shared_ptr<int> ptr1(new int(42));
auto ptr2 = make_shared<int>(42);

// 共享所有权
shared_ptr<int> ptr3 = ptr1;
cout << "Reference count: " << ptr1.use_count() << endl;  // 2

// 自定义删除器
shared_ptr<int> ptr4(new int(42), [](int* p) {
    cout << "Custom delete" << endl;
    delete p;
});

// 弱引用
weak_ptr<int> weak = ptr1;
if (auto locked = weak.lock()) {
    cout << "Value: " << *locked << endl;
}
```

### weak_ptr详解
```cpp
shared_ptr<int> shared = make_shared<int>(42);
weak_ptr<int> weak = shared;

// 检查是否有效
if (!weak.expired()) {
    auto locked = weak.lock();
    cout << "Value: " << *locked << endl;
}

// 获取引用计数
cout << "Use count: " << weak.use_count() << endl;
```

## RAII（资源获取即初始化）

RAII 是 C++ 资源管理的核心模式：构造函数获取资源，析构函数释放资源。利用栈对象自动析构特性。

### 基本概念

RAII 将资源生命周期绑定到对象生命周期，自动管理文件、锁、内存等资源。
```cpp
class FileHandle {
private:
    FILE* file;
public:
    FileHandle(const char* filename) : file(fopen(filename, "r")) {
        if (!file) {
            throw runtime_error("Cannot open file");
        }
    }
    
    ~FileHandle() {
        if (file) {
            fclose(file);
        }
    }
    
    // 禁用拷贝
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    
    // 允许移动
    FileHandle(FileHandle&& other) noexcept : file(other.file) {
        other.file = nullptr;
    }
    
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (file) fclose(file);
            file = other.file;
            other.file = nullptr;
        }
        return *this;
    }
};
```

### 锁管理
```cpp
#include <mutex>

class LockGuard {
private:
    mutex& mtx;
public:
    LockGuard(mutex& m) : mtx(m) {
        mtx.lock();
    }
    
    ~LockGuard() {
        mtx.unlock();
    }
    
    // 禁用拷贝和移动
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;
    LockGuard(LockGuard&&) = delete;
    LockGuard& operator=(LockGuard&&) = delete;
};
```

## 内存池

### 简单内存池实现
```cpp
class SimpleMemoryPool {
private:
    char* memory;
    size_t size;
    size_t used;
    
public:
    SimpleMemoryPool(size_t poolSize) : size(poolSize), used(0) {
        memory = new char[size];
    }
    
    ~SimpleMemoryPool() {
        delete[] memory;
    }
    
    void* allocate(size_t bytes) {
        if (used + bytes > size) {
            return nullptr;  // 内存不足
        }
        
        void* ptr = memory + used;
        used += bytes;
        return ptr;
    }
    
    void deallocate(void* ptr) {
        // 简单实现：不实际释放，只是重置
        used = 0;
    }
};
```

## 内存对齐

### 对齐规则
```cpp
struct AlignedStruct {
    char c;      // 1字节
    int i;       // 4字节，对齐到4字节边界
    double d;    // 8字节，对齐到8字节边界
};
// 总大小：24字节（1 + 3填充 + 4 + 8）

struct PackedStruct {
    char c;
    int i;
    double d;
} __attribute__((packed));  // GCC属性，取消对齐
// 总大小：13字节
```

### 对齐控制
```cpp
#include <cstddef>

// 查询对齐要求
cout << alignof(int) << endl;        // 4
cout << alignof(double) << endl;     // 8

// 对齐分配
void* ptr = aligned_alloc(16, 64);   // 16字节对齐，64字节大小
free(ptr);
```

## 内存调试

### Valgrind使用
```bash
# 内存泄漏检查
valgrind --leak-check=full ./program

# 内存错误检查
valgrind --tool=memcheck ./program

# 性能分析
valgrind --tool=callgrind ./program
```

### AddressSanitizer
```bash
# 编译时启用
g++ -fsanitize=address -g -o program source.cpp

# 运行时检查内存错误
./program
```

### 自定义内存检查
```cpp
class MemoryTracker {
private:
    static size_t allocated;
    static size_t deallocated;
    
public:
    static void* allocate(size_t size) {
        allocated += size;
        cout << "Allocated: " << size << " bytes" << endl;
        return malloc(size);
    }
    
    static void deallocate(void* ptr, size_t size) {
        deallocated += size;
        cout << "Deallocated: " << size << " bytes" << endl;
        free(ptr);
    }
    
    static void report() {
        cout << "Total allocated: " << allocated << " bytes" << endl;
        cout << "Total deallocated: " << deallocated << " bytes" << endl;
        cout << "Leaked: " << allocated - deallocated << " bytes" << endl;
    }
};
```

## 常见内存错误与检测

### 内存错误类型

```cpp
// 1. 内存泄漏 - 分配后忘记释放
void leak() {
    int* p = new int(42);
    return;  // 忘记delete，内存泄漏！
}

// 2. 重复释放 - Double Free
void doubleFree() {
    int* p = new int(42);
    delete p;
    delete p;  // 未定义行为！
}

// 3. 悬空指针 - Use After Free
void useAfterFree() {
    int* p = new int(42);
    delete p;
    *p = 100;  // 未定义行为！
}

// 4. 数组越界
void bufferOverflow() {
    int* arr = new int[10];
    arr[10] = 42;  // 越界！
    delete[] arr;
}

// 5. 错误的delete方式
void wrongDelete() {
    int* p = new int(42);
    delete[] p;  // 错误！应该用delete

    int* arr = new int[10];
    delete arr;  // 错误！应该用delete[]
}
```

### 检测工具使用

**Valgrind（Linux必备）：**
```bash
# 编译时加调试信息
g++ -g -o program source.cpp

# 内存泄漏检测
valgrind --leak-check=full --show-leak-kinds=all ./program

# 输出示例
# ==12345== LEAK SUMMARY:
# ==12345==    definitely lost: 40 bytes in 1 blocks
# ==12345==    indirectly lost: 0 bytes in 0 blocks

# 未初始化内存使用
valgrind --track-origins=yes ./program
```

**AddressSanitizer（推荐，速度快）：**
```bash
# 编译时启用（GCC/Clang）
g++ -fsanitize=address -g -o program source.cpp

# 运行程序自动检测
./program

# 检测类型：
# - 堆缓冲区溢出
# - 栈缓冲区溢出
# - Use after free
# - Use after return
# - Double free
```

**LeakSanitizer（内存泄漏专用）：**
```bash
# 编译时启用
g++ -fsanitize=leak -g -o program source.cpp

# 运行结束时报告泄漏
./program
```

**静态分析（编译期检查）：**
```bash
# Clang静态分析器
clang++ --analyze source.cpp

# Cppcheck
cppcheck --enable=all source.cpp

# Clang-Tidy
clang-tidy source.cpp -- -std=c++17
```

### 预防最佳实践

```cpp
// ✅ 1. 使用智能指针
std::unique_ptr<int> p(new int(42));  // 自动释放

// ✅ 2. RAII封装资源
class FileHandle {
    FILE* fp;
public:
    FileHandle(const char* name) : fp(fopen(name, "r")) {}
    ~FileHandle() { if (fp) fclose(fp); }
};

// ✅ 3. 使用容器代替数组
std::vector<int> vec(10);  // 自动管理内存

// ✅ 4. 删除后置空指针
delete p;
p = nullptr;  // 防止悬空指针

// ✅ 5. 禁用拷贝或正确实现深拷贝
class NoCopy {
public:
    NoCopy(const NoCopy&) = delete;
    NoCopy& operator=(const NoCopy&) = delete;
};
```

**核心思想：让编译器和库管理内存，而不是手动管理。**

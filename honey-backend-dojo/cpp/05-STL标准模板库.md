# STL 标准模板库

STL（Standard Template Library）是 C++ 的核心库，提供容器、迭代器、算法和函数对象。掌握 STL 可大幅提高开发效率。

## 容器

容器管理对象集合，自动处理内存分配。根据访问模式选择合适的容器是性能优化的关键。

### 序列容器

序列容器按插入顺序存储元素，支持位置访问。各容器在插入、删除、随机访问上有不同时间复杂度。

#### vector（动态数组）

`vector` 是最常用的容器，连续内存存储，支持快速随机访问。尾部插入 O(1) 均摊，中间插入 O(n)。
```cpp
#include <vector>

vector<int> v1;                    // 空vector
vector<int> v2(10);                // 10个元素，值为0
vector<int> v3(10, 5);             // 10个元素，值为5
vector<int> v4{1, 2, 3, 4, 5};     // 初始化列表

// 常用操作
v.push_back(6);                    // 添加元素
v.pop_back();                      // 删除最后一个元素
v.size();                          // 元素个数
v.empty();                         // 是否为空
v[0];                              // 访问元素
v.at(0);                           // 安全访问
v.clear();                         // 清空
```

#### list（双向链表）

`list` 是双向链表，不支持随机访问但插入删除高效。任意位置插入/删除 O(1)，适合频繁插入删除场景。

```cpp
#include <list>

list<int> l{1, 2, 3, 4, 5};

// 常用操作
l.push_front(0);                   // 头部插入
l.push_back(6);                    // 尾部插入
l.pop_front();                     // 头部删除
l.pop_back();                      // 尾部删除
l.insert(it, 10);                  // 指定位置插入
l.erase(it);                       // 删除指定位置
l.sort();                          // 排序
l.merge(other);                    // 合并
```

#### deque（双端队列）

`deque` 支持两端高效插入删除和随机访问。内部分块存储，是 `vector` 和 `list` 的折中方案。

```cpp
#include <deque>

deque<int> d{1, 2, 3, 4, 5};

// 常用操作
d.push_front(0);                   // 头部插入
d.push_back(6);                    // 尾部插入
d.pop_front();                     // 头部删除
d.pop_back();                      // 尾部删除
d[0];                              // 随机访问
```

### 关联容器

关联容器通过键快速查找，内部通常用红黑树或哈希表实现。自动排序（tree-based）或无序（hash-based）。

#### set（集合）

`set` 存储唯一有序元素，基于红黑树实现。查找、插入、删除均为 O(log n)，适合需要去重和排序的场景。


```cpp
#include <set>

set<int> s{3, 1, 4, 1, 5};         // 自动排序去重

// 常用操作
s.insert(6);                       // 插入
s.erase(3);                        // 删除
s.find(4);                         // 查找
s.count(4);                        // 计数
s.lower_bound(3);                  // 下界
s.upper_bound(3);                  // 上界
```

#### map（映射）

`map` 存储键值对，键唯一且有序。基于红黑树，查找 O(log n)，适合需要按键排序的关联数据。

```cpp
#include <map>

map<string, int> m;
m["apple"] = 5;                     // 插入
m["banana"] = 3;

// 常用操作
m.insert({"orange", 8});            // 插入
m.erase("apple");                   // 删除
m.find("banana");                   // 查找
m.count("banana");                  // 计数
m["apple"];                         // 访问

// 遍历
for (const auto& pair : m) {
    cout << pair.first << ": " << pair.second << endl;
}
```

#### unordered_set和unordered_map

哈希表实现的无序容器，查找 O(1) 平均，但不保证顺序。适合只关心存在性、不需排序的场景。

```cpp
#include <unordered_set>
#include <unordered_map>

unordered_set<int> us{1, 2, 3, 4, 5};  // 哈希集合
unordered_map<string, int> um;          // 哈希映射

// 操作与set/map类似，但无序
```

### 容器适配器

容器适配器提供受限接口，底层可用其他容器实现。`stack`、`queue`、`priority_queue` 是最常用的适配器。

#### stack（栈）

后进先出（LIFO）结构，只能访问栈顶元素。默认基于 `deque` 实现，适合回溯、括号匹配等场景。


```cpp
#include <stack>

stack<int> st;
st.push(1);                         // 入栈
st.push(2);
st.pop();                           // 出栈
st.top();                           // 栈顶元素
st.empty();                         // 是否为空
st.size();                          // 元素个数
```

#### queue（队列）

先进先出（FIFO）结构，只能访问队首和队尾。默认基于 `deque`，适合BFS、任务调度等场景。

```cpp
#include <queue>

queue<int> q;
q.push(1);                          // 入队
q.push(2);
q.pop();                            // 出队
q.front();                          // 队首元素
q.back();                           // 队尾元素
q.empty();                          // 是否为空
q.size();                           // 元素个数
```

#### priority_queue（优先队列）

基于堆实现的优先队列，自动维护最大（或最小）元素在顶部。插入/删除 O(log n)，适合Top K、任务调度。

```cpp
#include <queue>

priority_queue<int> pq;             // 最大堆
priority_queue<int, vector<int>, greater<int>> min_pq; // 最小堆

pq.push(3);                         // 插入
pq.push(1);
pq.push(4);
pq.pop();                           // 删除最大元素
pq.top();                           // 最大元素
```

## 迭代器

迭代器是容器和算法之间的桥梁，提供统一的遍历接口。理解迭代器类别对选择算法至关重要。

### 迭代器类型

C++提供5种迭代器类别：输入、输出、前向、双向、随机访问。容器支持的迭代器类别决定了可用的算法。


```cpp
vector<int> v{1, 2, 3, 4, 5};

// 正向迭代器
vector<int>::iterator it;
for (it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";
}

// 反向迭代器
vector<int>::reverse_iterator rit;
for (rit = v.rbegin(); rit != v.rend(); ++rit) {
    cout << *rit << " ";
}

// 常量迭代器
vector<int>::const_iterator cit;
for (cit = v.cbegin(); cit != v.cend(); ++cit) {
    cout << *cit << " ";
}
```

### 范围for循环（C++11）

范围for是C++11引入的语法糖，简化容器遍历。编译器自动处理迭代器，代码更简洁易读。

```cpp
vector<int> v{1, 2, 3, 4, 5};

// 值拷贝
for (int value : v) {
    cout << value << " ";
}

// 引用
for (int& value : v) {
    value *= 2;
}

// const引用
for (const int& value : v) {
    cout << value << " ";
}
```

## 算法

STL算法是泛型函数模板，通过迭代器操作容器。算法与容器解耦，一个算法可用于多种容器。

### 查找算法

查找算法定位满足条件的元素。线性查找适用于无序容器，二分查找要求有序且支持随机访问。


```cpp
#include <algorithm>

vector<int> v{1, 2, 3, 4, 5};

// 查找
auto it = find(v.begin(), v.end(), 3);
if (it != v.end()) {
    cout << "Found at position: " << distance(v.begin(), it) << endl;
}

// 二分查找（需要有序）
sort(v.begin(), v.end());
bool found = binary_search(v.begin(), v.end(), 3);

// 查找第一个满足条件的元素
auto it2 = find_if(v.begin(), v.end(), [](int x) { return x > 3; });
```

### 排序算法

STL提供多种排序算法，默认使用快速排序的优化版本（Introsort）。`stable_sort` 保持相等元素的相对顺序。

```cpp
vector<int> v{5, 2, 8, 1, 9};

// 排序
sort(v.begin(), v.end());           // 升序
sort(v.begin(), v.end(), greater<int>()); // 降序

// 部分排序
partial_sort(v.begin(), v.begin() + 3, v.end());

// 稳定排序
stable_sort(v.begin(), v.end());

// 堆排序
make_heap(v.begin(), v.end());
sort_heap(v.begin(), v.end());
```

### 变换算法

变换算法对容器元素进行转换、填充或生成。`transform` 是函数式编程在C++中的体现。

```cpp
vector<int> v{1, 2, 3, 4, 5};
vector<int> result(v.size());

// 变换
transform(v.begin(), v.end(), result.begin(), [](int x) { return x * 2; });

// 填充
fill(v.begin(), v.end(), 0);

// 生成
generate(v.begin(), v.end(), []() { return rand() % 100; });
```

### 删除算法

删除算法不直接删除元素，而是将要保留的元素移到前面，返回新的逻辑末尾。需配合 `erase` 真正删除。

```cpp
vector<int> v{1, 2, 3, 2, 4, 2, 5};

// 删除指定值
v.erase(remove(v.begin(), v.end(), 2), v.end());

// 删除重复元素（需要先排序）
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());
```

## 函数对象和Lambda

函数对象和Lambda表达式是STL算法的强大工具，提供灵活的自定义行为。Lambda让代码更简洁。

### 函数对象

函数对象（Functor）是重载了 `operator()` 的类。比普通函数更灵活，可携带状态。


```cpp
class Multiply {
private:
    int factor;
public:
    Multiply(int f) : factor(f) {}
    int operator()(int x) const {
        return x * factor;
    }
};

vector<int> v{1, 2, 3, 4, 5};
transform(v.begin(), v.end(), v.begin(), Multiply(3));
```

### Lambda表达式（C++11）

Lambda是匿名函数，语法：`[捕获](参数){函数体}`。捕获外部变量，常用于STL算法的谓词。

```cpp
vector<int> v{1, 2, 3, 4, 5};

// 基本lambda
auto lambda = [](int x) { return x * 2; };

// 捕获变量
int factor = 3;
auto lambda2 = [factor](int x) { return x * factor; };

// 引用捕获
auto lambda3 = [&factor](int x) { return x * factor; };

// 通用捕获（C++14）
auto lambda4 = [factor = 3](int x) { return x * factor; };

// 使用lambda
transform(v.begin(), v.end(), v.begin(), [](int x) { return x * 2; });
```

## 智能指针

智能指针自动管理动态内存，是现代C++的基石。避免手动 `new/delete`，防止内存泄漏。

### unique_ptr（C++11）

独占所有权指针，不可拷贝只能移动。零开销，应优先使用。适合明确单一所有者的场景。


```cpp
#include <memory>

// 创建
unique_ptr<int> ptr1(new int(42));
auto ptr2 = make_unique<int>(42);  // C++14

// 移动语义
unique_ptr<int> ptr3 = move(ptr1);

// 自动释放
// 超出作用域时自动delete
```

### shared_ptr（C++11）

共享所有权指针，通过引用计数管理生命周期。最后一个`shared_ptr`销毁时释放资源。有一定开销。

```cpp
// 创建
shared_ptr<int> ptr1(new int(42));
auto ptr2 = make_shared<int>(42);

// 共享所有权
shared_ptr<int> ptr3 = ptr1;
cout << ptr1.use_count();          // 引用计数

// 自动释放
// 当最后一个shared_ptr销毁时自动delete
```

### weak_ptr（C++11）

弱引用指针，不增加引用计数，防止循环引用。使用前需 `lock()` 转换为 `shared_ptr`，可能返回空。

```cpp
shared_ptr<int> shared = make_shared<int>(42);
weak_ptr<int> weak = shared;

// 检查是否有效
if (auto locked = weak.lock()) {
    cout << *locked << endl;
}
```

## 容器选择指南

### 时间复杂度对比表

| 操作 | vector | deque | list | set/map | unordered_set/map |
|------|--------|-------|------|---------|-------------------|
| 随机访问 | O(1) | O(1) | O(n) | O(log n) | - |
| 头部插入 | O(n) | O(1) | O(1) | O(log n) | O(1) |
| 尾部插入 | O(1) | O(1) | O(1) | O(log n) | O(1) |
| 中间插入 | O(n) | O(n) | O(1) | O(log n) | O(1) |
| 查找 | O(n) | O(n) | O(n) | O(log n) | O(1) |
| 删除 | O(n) | O(n) | O(1) | O(log n) | O(1) |

### 选择决策树

```cpp
需要随机访问？
├─ 是 → 需要两端插入？
│  ├─ 是 → deque
│  └─ 否 → vector (首选)
└─ 否 → 需要排序？
   ├─ 是 → 需要键值对？
   │  ├─ 是 → map/multimap
   │  └─ 否 → set/multiset
   └─ 否 → 需要快速查找？
      ├─ 是 → 需要键值对？
      │  ├─ 是 → unordered_map
      │  └─ 否 → unordered_set
      └─ 否 → 频繁中间插入删除？
         ├─ 是 → list
         └─ 否 → vector
```

### 场景推荐

**vector（默认首选）：**
- 90%的情况下最佳选择
- 内存连续，缓存友好
- 动态数组，尾部操作O(1)
- 适用：数组、栈、动态缓冲区

**deque：**
- 需要两端插入删除
- 适用：双端队列、滑动窗口

**list：**
- 频繁中间插入删除
- 需要在任意位置O(1)插入
- 适用：LRU缓存、链表算法

**set/map：**
- 需要自动排序
- 需要O(log n)查找
- 适用：去重、有序数据、范围查询

**unordered_set/map：**
- 只关心存在性
- 需要O(1)查找
- 适用：计数、去重、哈希表

**priority_queue：**
- 需要快速访问最大/最小元素
- 适用：堆排序、Top K问题

### 性能陷阱

```cpp
// ❌ vector频繁头部插入
for (int i = 0; i < n; ++i) {
    vec.insert(vec.begin(), i);  // O(n)，总复杂度O(n²)
}

// ✅ 改用deque
deque<int> dq;
for (int i = 0; i < n; ++i) {
    dq.push_front(i);  // O(1)，总复杂度O(n)
}

// ❌ 未预留空间导致多次重新分配
vector<int> vec;
for (int i = 0; i < 10000; ++i) {
    vec.push_back(i);  // 可能多次重新分配
}

// ✅ 预留空间
vector<int> vec;
vec.reserve(10000);  // 一次分配
for (int i = 0; i < 10000; ++i) {
    vec.push_back(i);
}
```

**关键原则：默认用vector，有特殊需求再换其他容器。**

# 04-STL标准模板库

## 容器

### 序列容器

#### vector（动态数组）
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

#### set（集合）
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
```cpp
#include <unordered_set>
#include <unordered_map>

unordered_set<int> us{1, 2, 3, 4, 5};  // 哈希集合
unordered_map<string, int> um;          // 哈希映射

// 操作与set/map类似，但无序
```

### 容器适配器

#### stack（栈）
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

### 迭代器类型
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

### 查找算法
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
```cpp
vector<int> v{1, 2, 3, 2, 4, 2, 5};

// 删除指定值
v.erase(remove(v.begin(), v.end(), 2), v.end());

// 删除重复元素（需要先排序）
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());
```

## 函数对象和Lambda

### 函数对象
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

### unique_ptr（C++11）
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
```cpp
shared_ptr<int> shared = make_shared<int>(42);
weak_ptr<int> weak = shared;

// 检查是否有效
if (auto locked = weak.lock()) {
    cout << *locked << endl;
}
```

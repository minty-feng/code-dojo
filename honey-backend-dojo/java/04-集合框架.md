# 04-Java集合框架

Java集合框架（JCF）提供数据结构实现，是标准库的核心。掌握集合选择和使用是高效编程的基础。

## 集合框架结构

```
Collection
├── List（有序，可重复）
│   ├── ArrayList
│   ├── LinkedList
│   └── Vector（同步，少用）
├── Set（无序，不重复）
│   ├── HashSet
│   ├── LinkedHashSet
│   └── TreeSet
└── Queue（队列）
    ├── LinkedList
    ├── PriorityQueue
    └── Deque

Map（键值对）
├── HashMap
├── LinkedHashMap
├── TreeMap
├── Hashtable（同步，少用）
└── ConcurrentHashMap（并发）
```

## List接口

### ArrayList

基于动态数组，随机访问快，插入删除慢。

```java
import java.util.ArrayList;

// 创建
ArrayList<String> list = new ArrayList<>();
ArrayList<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3));

// 添加
list.add("apple");
list.add(0, "banana");           // 指定位置插入

// 访问
String first = list.get(0);
list.set(0, "cherry");           // 修改

// 删除
list.remove(0);                  // 按索引删除
list.remove("apple");            // 按对象删除

// 查询
int size = list.size();
boolean empty = list.isEmpty();
boolean contains = list.contains("apple");
int index = list.indexOf("apple");

// 遍历
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}

for (String item : list) {
    System.out.println(item);
}

list.forEach(System.out::println);  // Lambda
```

**时间复杂度：**
- 随机访问：O(1)
- 尾部添加：O(1)均摊
- 中间插入/删除：O(n)
- 查找：O(n)

### LinkedList

基于双向链表，插入删除快，随机访问慢。同时实现List和Deque。

```java
import java.util.LinkedList;

LinkedList<String> list = new LinkedList<>();

// List操作
list.add("apple");
list.add(0, "banana");

// Deque操作
list.addFirst("first");
list.addLast("last");
list.removeFirst();
list.removeLast();
list.getFirst();
list.getLast();

// 队列操作
list.offer("item");   // 入队
list.poll();          // 出队
list.peek();          // 查看队首
```

**时间复杂度：**
- 随机访问：O(n)
- 头尾插入/删除：O(1)
- 中间插入/删除：O(1)（已有迭代器）

### Vector

同步的ArrayList，线程安全但性能低，已过时。推荐用 `Collections.synchronizedList()` 或 `CopyOnWriteArrayList`。

## Set接口

### HashSet

基于HashMap实现，无序不重复，查找O(1)。

```java
import java.util.HashSet;

HashSet<String> set = new HashSet<>();

// 添加
set.add("apple");
set.add("banana");
set.add("apple");  // 重复，不会添加

// 查询
boolean contains = set.contains("apple");
int size = set.size();

// 删除
set.remove("apple");
set.clear();

// 遍历（无序）
for (String item : set) {
    System.out.println(item);
}
```

### LinkedHashSet

基于LinkedHashMap，维护插入顺序。

```java
LinkedHashSet<String> set = new LinkedHashSet<>();
set.add("c");
set.add("a");
set.add("b");
// 遍历顺序：c, a, b
```

### TreeSet

基于红黑树，元素自动排序。

```java
import java.util.TreeSet;

TreeSet<Integer> set = new TreeSet<>();
set.add(3);
set.add(1);
set.add(2);
// 遍历顺序：1, 2, 3（自动排序）

// 范围查询
set.first();             // 最小元素
set.last();              // 最大元素
set.lower(2);            // < 2的最大元素
set.higher(2);           // > 2的最小元素
set.headSet(5);          // < 5的元素集合
set.tailSet(5);          // >= 5的元素集合
set.subSet(2, 5);        // [2, 5)的元素集合
```

**时间复杂度：** O(log n)

## Map接口

### HashMap

基于哈希表，无序，查找O(1)，最常用的Map。

```java
import java.util.HashMap;

HashMap<String, Integer> map = new HashMap<>();

// 添加
map.put("apple", 5);
map.put("banana", 3);
map.put("apple", 10);            // 覆盖旧值

// 访问
Integer count = map.get("apple"); // 10
Integer def = map.getOrDefault("orange", 0);  // 不存在返回默认值

// 删除
map.remove("apple");

// 查询
boolean hasKey = map.containsKey("apple");
boolean hasValue = map.containsValue(5);
int size = map.size();

// 遍历
for (String key : map.keySet()) {
    System.out.println(key + ": " + map.get(key));
}

for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}

map.forEach((k, v) -> System.out.println(k + ": " + v));  // Lambda
```

**Java 8增强：**
```java
// computeIfAbsent：不存在时计算并添加
map.computeIfAbsent("key", k -> expensiveComputation(k));

// merge：合并值
map.merge("apple", 1, (oldVal, newVal) -> oldVal + newVal);  // 计数

// putIfAbsent：不存在时才添加
map.putIfAbsent("key", "value");
```

### LinkedHashMap

维护插入顺序或访问顺序，可实现LRU缓存。

```java
// 插入顺序
LinkedHashMap<String, Integer> map = new LinkedHashMap<>();

// 访问顺序（LRU）
LinkedHashMap<String, Integer> lruMap = new LinkedHashMap<>(16, 0.75f, true);

// LRU缓存实现
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private int capacity;
    
    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }
    
    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;  // 超过容量删除最老的
    }
}
```

### TreeMap

基于红黑树，键自动排序。

```java
import java.util.TreeMap;

TreeMap<String, Integer> map = new TreeMap<>();
map.put("c", 3);
map.put("a", 1);
map.put("b", 2);
// 遍历顺序：a, b, c（按键排序）

// 范围操作
map.firstKey();          // 最小键
map.lastKey();           // 最大键
map.lowerKey("b");       // < b的最大键
map.higherKey("b");      // > b的最小键
map.headMap("c");        // < c的映射
map.tailMap("b");        // >= b的映射
map.subMap("a", "c");    // [a, c)的映射
```

### ConcurrentHashMap

线程安全的HashMap，使用分段锁，性能优于Hashtable。

```java
import java.util.concurrent.ConcurrentHashMap;

ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 原子操作
map.putIfAbsent("key", 1);
map.compute("key", (k, v) -> v == null ? 1 : v + 1);
map.merge("key", 1, Integer::sum);  // 计数
```

## Queue和Deque

### Queue（队列）

```java
import java.util.Queue;
import java.util.LinkedList;

Queue<String> queue = new LinkedList<>();

// 添加（失败抛异常）
queue.add("first");

// 添加（失败返回false）
queue.offer("second");

// 删除并返回队首（失败抛异常）
String head = queue.remove();

// 删除并返回队首（失败返回null）
String head2 = queue.poll();

// 查看队首（不删除）
String peek1 = queue.element();  // 失败抛异常
String peek2 = queue.peek();     // 失败返回null
```

### PriorityQueue（优先队列）

基于堆实现，默认小顶堆。

```java
import java.util.PriorityQueue;

// 小顶堆（默认）
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(3);
minHeap.offer(1);
minHeap.offer(2);
minHeap.poll();  // 1（最小元素）

// 大顶堆
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);
maxHeap.offer(3);
maxHeap.offer(1);
maxHeap.offer(2);
maxHeap.poll();  // 3（最大元素）

// 自定义比较器
PriorityQueue<Task> taskQueue = new PriorityQueue<>(
    Comparator.comparingInt(Task::getPriority)
);
```

### Deque（双端队列）

```java
import java.util.Deque;
import java.util.ArrayDeque;

Deque<String> deque = new ArrayDeque<>();

// 作为栈使用
deque.push("a");
deque.push("b");
String top = deque.pop();  // LIFO

// 作为队列使用
deque.offer("a");
deque.offer("b");
String head = deque.poll();  // FIFO

// 双端操作
deque.offerFirst("first");
deque.offerLast("last");
deque.pollFirst();
deque.pollLast();
```

## Collections工具类

```java
import java.util.Collections;

List<Integer> list = new ArrayList<>(Arrays.asList(3, 1, 4, 1, 5));

// 排序
Collections.sort(list);                         // 升序
Collections.sort(list, Collections.reverseOrder());  // 降序

// 查找
int max = Collections.max(list);
int min = Collections.min(list);
int index = Collections.binarySearch(list, 3);  // 需有序

// 反转
Collections.reverse(list);

// 洗牌
Collections.shuffle(list);

// 填充
Collections.fill(list, 0);

// 复制
Collections.copy(dest, src);

// 同步包装
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());

// 不可修改包装
List<String> unmodifiable = Collections.unmodifiableList(list);
```

## 集合选择指南

### 时间复杂度对比

| 操作 | ArrayList | LinkedList | HashSet | TreeSet | HashMap | TreeMap |
|------|-----------|------------|---------|---------|---------|---------|
| 添加 | O(1)* | O(1) | O(1) | O(log n) | O(1) | O(log n) |
| 删除 | O(n) | O(1)** | O(1) | O(log n) | O(1) | O(log n) |
| 查找 | O(n) | O(n) | O(1) | O(log n) | O(1) | O(log n) |
| 随机访问 | O(1) | O(n) | - | - | O(1) | O(log n) |

*尾部添加，中间插入O(n)  
**已有迭代器

### 选择决策

```
需要键值对？
├─ 是 → 需要排序？
│  ├─ 是 → TreeMap
│  └─ 否 → HashMap（首选）
└─ 否 → 需要去重？
   ├─ 是 → 需要排序？
   │  ├─ 是 → TreeSet
   │  └─ 否 → HashSet
   └─ 否 → 需要随机访问？
      ├─ 是 → ArrayList（首选）
      └─ 否 → 需要队列？
         ├─ 是 → ArrayDeque
         └─ 否 → 频繁插入删除？
            └─ 是 → LinkedList
```

### 场景匹配

**ArrayList：**
- 默认List实现
- 查询多，修改少
- 顺序访问

**LinkedList：**
- 频繁头尾操作
- 需要队列/栈
- 中间插入删除多

**HashSet：**
- 去重
- 快速查找
- 不关心顺序

**TreeSet：**
- 需要排序
- 范围查询

**HashMap（最常用Map）：**
- 键值存储
- 快速查找
- 不需要排序

**TreeMap：**
- 需要按键排序
- 范围查询

## 集合常见陷阱

```java
// 1. 遍历时修改集合
List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));

// ❌ ConcurrentModificationException
for (Integer num : list) {
    if (num % 2 == 0) {
        list.remove(num);  // 抛出异常！
    }
}

// ✅ 使用迭代器
Iterator<Integer> it = list.iterator();
while (it.hasNext()) {
    if (it.next() % 2 == 0) {
        it.remove();  // 安全删除
    }
}

// ✅ removeIf（Java 8+）
list.removeIf(num -> num % 2 == 0);

// 2. HashMap的key必须重写equals和hashCode
class Person {
    String name;
    // 如果不重写hashCode，相同name的Person会被认为不同
}

// 3. 泛型擦除导致的问题
List<String> list1 = new ArrayList<>();
List<Integer> list2 = new ArrayList<>();
list1.getClass() == list2.getClass();  // true！运行时都是ArrayList

// 4. Arrays.asList返回固定大小List
List<Integer> list = Arrays.asList(1, 2, 3);
// list.add(4);  // UnsupportedOperationException

// ✅ 转换为可变List
List<Integer> mutable = new ArrayList<>(Arrays.asList(1, 2, 3));
```

## 集合性能优化

```java
// 1. 预分配容量
List<String> list = new ArrayList<>(10000);  // 避免扩容

// 2. HashMap初始容量和负载因子
// 容量 = 预期元素数 / 负载因子
Map<String, Integer> map = new HashMap<>(16, 0.75f);

// 3. 批量操作
list.addAll(anotherList);  // 优于逐个add

// 4. 使用原始类型流避免装箱
list.stream()
    .mapToInt(Integer::intValue)  // IntStream，避免装箱
    .sum();

// 5. EnumSet/EnumMap（枚举类型）
Set<Day> days = EnumSet.of(Day.MONDAY, Day.FRIDAY);  // 极高效

// 6. 只读场景用List.of（Java 9+）
List<String> immutable = List.of("a", "b", "c");  // 不可变，内存优化
```

## 比较器

### Comparable接口

对象自然排序。

```java
public class Student implements Comparable<Student> {
    private String name;
    private int score;
    
    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.score, other.score);  // 按分数排序
    }
}

List<Student> students = new ArrayList<>();
Collections.sort(students);  // 使用compareTo
```

### Comparator接口

自定义排序规则。

```java
// 匿名类
Comparator<Student> byName = new Comparator<Student>() {
    @Override
    public int compare(Student s1, Student s2) {
        return s1.getName().compareTo(s2.getName());
    }
};

// Lambda
Comparator<Student> byScore = (s1, s2) -> Integer.compare(s1.getScore(), s2.getScore());

// 方法引用
Comparator<Student> byName2 = Comparator.comparing(Student::getName);
Comparator<Student> byScore2 = Comparator.comparingInt(Student::getScore);

// 组合比较器
Comparator<Student> combined = Comparator
    .comparingInt(Student::getScore)
    .thenComparing(Student::getName);  // 分数相同按姓名

// 使用
students.sort(byScore);
Collections.sort(students, byName);
```

## 最佳实践

1. **优先接口类型声明**：`List<String> list = new ArrayList<>();`
2. **预分配容量**：已知大小时避免扩容
3. **使用泛型**：类型安全
4. **重写equals/hashCode**：用作HashMap的key必须重写
5. **不可变集合**：多线程共享用`Collections.unmodifiable`或`List.of()`
6. **迭代器删除**：遍历时修改用迭代器
7. **Stream API处理**：链式调用更清晰
8. **选对容器**：90%场景ArrayList+HashMap够用
9. **EnumSet/EnumMap**：枚举类型首选
10. **避免null值**：用Optional或空集合

**核心：** 选择合适的集合类型是性能和可读性的基础。


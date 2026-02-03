# 06-堆（Heap）

## 💡 核心结论

### 堆本质
- **定义**：完全二叉树，满足堆性质（父节点≥/≤所有子节点）
- **类型**：最大堆（父≥子）、最小堆（父≤子）
- **核心**：快速找到最大/最小值O(1)，插入删除O(log n)
- **实现**：用数组存储，利用完全二叉树性质计算索引
- **应用**：优先队列、Top K问题、堆排序

### 数组索引公式（从0开始）
```
父节点: (i - 1) / 2
左子节点: 2i + 1
右子节点: 2i + 2
```

### 关键操作
| 操作 | 复杂度 | 说明 |
|------|--------|------|
| 找最大/最小 | O(1) | 堆顶元素 |
| 插入 | O(log n) | 上浮调整 |
| 删除堆顶 | O(log n) | 下沉调整 |
| 建堆 | O(n) | 从底向上调整 |

### 堆 vs 其他结构
| 数据结构 | 找最大 | 插入 | 删除最大 |
|----------|--------|------|----------|
| 无序数组 | O(n) | O(1) | O(n) |
| 有序数组 | O(1) | O(n) | O(1) |
| BST | O(log n) | O(log n) | O(log n) |
| **堆** | **O(1)** | **O(log n)** | **O(log n)** |

### 应用场景（重要）
1. **优先队列**：任务调度、事件驱动
2. **Top K问题**：最大/最小的K个元素
3. **堆排序**：O(n log n)原地排序
4. **中位数维护**：双堆结构
5. **定时器**：最小堆管理定时任务

## 🔺 最大堆操作

### 上浮（Swim/Heapify Up）
```
插入新元素后，从底向上调整
如果子节点 > 父节点，交换
重复直到满足堆性质
```

### 下沉（Sink/Heapify Down）
```
删除堆顶后，将末尾元素放到堆顶
从上向下调整
与较大的子节点交换
重复直到满足堆性质
```

## 🏗️ 建堆

### 方法1：逐个插入
```python
# 时间复杂度：O(n log n)
for element in array:
    heap.insert(element)
```

### 方法2：自底向上（推荐）
```python
# 时间复杂度：O(n)
# 从最后一个非叶子节点开始下沉
for i in range((len(array) - 2) // 2, -1, -1):
    heapify_down(array, i)
```

**为什么O(n)**：
- 叶子节点占一半，不需要调整
- 倒数第二层最多下沉1次
- 倒数第三层最多下沉2次
- 总和：n/2×0 + n/4×1 + n/8×2 + ... = O(n)

## 🎯 堆排序

### 算法步骤
1. 建立最大堆：O(n)
2. 交换堆顶和末尾：O(1)
3. 减小堆大小，下沉新堆顶：O(log n)
4. 重复步骤2-3：n次

总时间复杂度：O(n log n)
空间复杂度：O(1)（原地排序）

```python
def heap_sort(arr):
    # 建堆
    for i in range((len(arr) - 2) // 2, -1, -1):
        heapify_down(arr, i, len(arr))
    
    # 排序
    for i in range(len(arr) - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_down(arr, 0, i)
```

## 💡 Top K问题

### 最大的K个元素
```python
# 使用最小堆，维护K个元素
import heapq

def top_k_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)  # 最小堆
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    
    return heap
```

### 最小的K个元素
```python
# 使用最大堆
def top_k_smallest(nums, k):
    # Python heapq是最小堆，取负数实现最大堆
    heap = [-x for x in nums[:k]]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if num < -heap[0]:
            heapq.heapreplace(heap, -num)
    
    return [-x for x in heap]
```

## 📚 LeetCode练习

- [215. Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)
- [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
- [703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)

## 💻 完整代码实现

### Python 实现

```{literalinclude} heap.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} heap.cpp
:language: cpp
:linenos:
```


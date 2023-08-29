# 15-bit-manipulation (位运算)

LeetCode精选75题 - 位运算专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 只出现一次的数字 | ⭐ | [136](https://leetcode.cn/problems/single-number/) | [01-single-number.py](./01-single-number.py) | [01-single-number.cpp](./01-single-number.cpp) |
| 02 | 汉明距离 | ⭐ | [461](https://leetcode.cn/problems/hamming-distance/) | [02-hamming-distance.py](./02-hamming-distance.py) | [02-hamming-distance.cpp](./02-hamming-distance.cpp) |
| 03 | 颠倒二进制位 | ⭐ | [190](https://leetcode.cn/problems/reverse-bits/) | [03-reverse-bits.py](./03-reverse-bits.py) | [03-reverse-bits.cpp](./03-reverse-bits.cpp) |

## 🎯 核心技巧

### 位运算基础
- **[只出现一次的数字](./01-single-number.py)**：异或运算的性质
- **[汉明距离](./02-hamming-distance.py)**：异或 + 位计数
- **[颠倒二进制位](./03-reverse-bits.py)**：位操作技巧

---

## 💡 解题模板

### 异或运算模板
```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

### 位计数模板
```python
def hamming_distance(x, y):
    xor = x ^ y
    count = 0
    
    while xor:
        count += xor & 1
        xor >>= 1
    
    return count
```

### 位操作模板
```python
def reverse_bits(n):
    result = 0
    
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    
    return result
```

---

## 📚 学习重点

1. **位运算基础**：与、或、异或、非
2. **异或性质**：a ^ a = 0, a ^ 0 = a
3. **位计数**：统计二进制中1的个数
4. **位操作技巧**：左移、右移、掩码

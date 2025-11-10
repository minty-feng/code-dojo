# 03-位运算详解

位运算直接操作二进制位，是底层编程和性能优化的利器。理解位运算需要先掌握计算机数字表示。

## 1. 计算机中的数字表示

计算机使用二进制存储数字。正负数的表示方式经历了原码、反码到补码的演进，现代计算机统一使用补码。

### 1.1 原码、反码、补码

#### 原码（Sign-Magnitude）
- **定义**：最高位为符号位（0表示正，1表示负），其余位表示数值的绝对值
- **范围**（8位）：-127 ~ +127
- **特点**：有两个零（+0 和 -0）

```
+5 的原码：0000 0101
-5 的原码：1000 0101
+0 的原码：0000 0000
-0 的原码：1000 0000
```

#### 反码（One's Complement）
- **正数**：反码与原码相同
- **负数**：符号位不变，其余位按位取反

```
+5 的反码：0000 0101
-5 的反码：1111 1010  (符号位1，数值位取反)
+0 的反码：0000 0000
-0 的反码：1111 1111
```

#### 补码（Two's Complement）
- **正数**：补码与原码相同
- **负数**：反码 + 1
- **特点**：只有一个零，能多表示一个负数

```
+5 的补码：0000 0101
-5 的补码：1111 1011  (反码 1111 1010 + 1)
+0 的补码：0000 0000
-0 的补码：0000 0000  (反码 1111 1111 + 1，溢出)

特殊：-128 的补码：1000 0000  (8位补码特有)
```

**为什么使用补码？**
1. **统一加减运算**：减法可以转换为加法
2. **只有一个零**：节省一个编码
3. **硬件实现简单**：CPU 只需要加法器

```cpp
// 补码加法示例
// 5 + (-3) = 2
  0000 0101  (+5)
+ 1111 1101  (-3 的补码)
-----------
  0000 0010  (+2)  正确
```

### 1.2 不同数据类型的范围

```cpp
// 有符号整型（补码表示）
char:      -128 ~ 127                    (8位)
short:     -32768 ~ 32767                (16位)
int:       -2147483648 ~ 2147483647      (32位)
long long: -9223372036854775808 ~ ...    (64位)

// 无符号整型
unsigned char:      0 ~ 255
unsigned short:     0 ~ 65535
unsigned int:       0 ~ 4294967295
unsigned long long: 0 ~ 18446744073709551615
```

### 1.3 整数溢出

#### 有符号整数溢出
```cpp
// 有符号溢出是未定义行为（Undefined Behavior）
int max = 2147483647;  // INT_MAX
int overflow = max + 1;  // UB! 可能得到 -2147483648

// 检测溢出
bool will_overflow(int a, int b) {
    // 加法溢出检测
    if (a > 0 && b > 0 && a > INT_MAX - b) return true;
    if (a < 0 && b < 0 && a < INT_MIN - b) return true;
    return false;
}
```

#### 无符号整数溢出
```cpp
// 无符号溢出是定义明确的（循环回绕）
unsigned int max = 4294967295U;  // UINT_MAX
unsigned int overflow = max + 1;  // 0 (定义良好)

// 常见陷阱
unsigned int a = 5, b = 10;
if (a - b < 0) {  // 永远为 false！
    // a - b = 4294967291 (循环回绕)
}

// 正确做法
if (a < b) {
    int diff = (int)a - (int)b;  // -5
}
```

## 2. 位运算符

C++提供6种位运算符，直接操作整数的二进制位。掌握它们的特性和应用场景是位运算的核心。

### 2.1 基本位运算符

```cpp
&   按位与(AND)
|   按位或(OR)
^   按位异或(XOR)
~   按位取反(NOT)
<<  左移
>>  右移
```

#### 按位与（&）
```cpp
// 规则：都为1才为1
  1010
& 1100
------
  1000

// 应用：
// 1. 取某位
int x = 0b1011;
bool bit2 = x & (1 << 2);  // 取第2位：1

// 2. 清零某位
x = x & ~(1 << 2);  // 清零第2位：0011

// 3. 判断奇偶
bool is_odd = (x & 1);  // 最低位为1则为奇数

// 4. 保留低n位
int low8bits = x & 0xFF;  // 保留低8位
```

#### 按位或（|）
```cpp
// 规则：有1则为1
  1010
| 1100
------
  1110

// 应用：
// 1. 设置某位为1
x = x | (1 << 2);  // 设置第2位为1

// 2. 合并标志位
enum Flags {
    READ = 1 << 0,   // 0001
    WRITE = 1 << 1,  // 0010
    EXEC = 1 << 2    // 0100
};
int permissions = READ | WRITE;  // 0011
```

#### 按位异或（^）
```cpp
// 规则：相同为0，不同为1
  1010
^ 1100
------
  0110

// 重要性质：
// 1. a ^ a = 0
// 2. a ^ 0 = a
// 3. a ^ b ^ b = a (消除律)
// 4. 满足交换律和结合律

// 应用：
// 1. 翻转某位
x = x ^ (1 << 2);  // 翻转第2位

// 2. 交换两个数（不用临时变量）
void swap(int& a, int& b) {
    a = a ^ b;
    b = a ^ b;  // b = (a ^ b) ^ b = a
    a = a ^ b;  // a = (a ^ b) ^ a = b
}

// 3. 加密（简单异或加密）
char encrypt(char c, char key) {
    return c ^ key;
}
char decrypt(char c, char key) {
    return c ^ key;  // 异或两次恢复
}
```

#### 按位取反（~）
```cpp
// 规则：0变1，1变0
~1010 = 0101

// 应用：
// 1. 创建掩码
int mask = ~(1 << 2);  // ...11110111 (第2位为0)

// 2. 取反
unsigned char x = 0b10101010;
unsigned char y = ~x;  // 0b01010101
```

### 2.2 移位运算符

#### 左移（<<）
```cpp
// 左移n位 = 乘以 2^n
int x = 5;        // 0000 0101
int y = x << 2;   // 0001 0100 = 20

// 应用：
// 1. 快速乘以2的幂
int mul8 = x << 3;  // x * 8

// 2. 创建位掩码
int bit_n = 1 << n;  // 第n位为1

// 3. 设置多个位
int bits = (1 << 3) | (1 << 5) | (1 << 7);  // 10101000
```

#### 右移（>>）

**逻辑右移**：高位补0（无符号数）
```cpp
unsigned int x = 0b10101010;
unsigned int y = x >> 2;  // 0b00101010
```

**算术右移**：高位补符号位（有符号数）
```cpp
int x = -8;        // 1111 1000 (补码)
int y = x >> 2;    // 1111 1110 = -2

// 应用：快速除以2的幂
int div4 = x >> 2;  // x / 4 (向下取整)

// 注意：负数右移行为是实现定义的！
// 大多数编译器使用算术右移
```

## 3. 位运算技巧

位运算技巧是算法优化的秘密武器。这些技巧看似巧妙，实则基于位运算的数学性质。

### 3.1 基础技巧

常用的位操作模式，如获取、设置、清除特定位，是位运算的基本功。

```cpp
// 1. 获取第n位
bool get_bit(int x, int n) {
    return (x >> n) & 1;
}

// 2. 设置第n位为1
int set_bit(int x, int n) {
    return x | (1 << n);
}

// 3. 清除第n位（设为0）
int clear_bit(int x, int n) {
    return x & ~(1 << n);
}

// 4. 翻转第n位
int toggle_bit(int x, int n) {
    return x ^ (1 << n);
}

// 5. 修改第n位为v（0或1）
int update_bit(int x, int n, bool v) {
    return (x & ~(1 << n)) | (v << n);
}

// 6. 清除最右边的1
int clear_rightmost_1(int x) {
    return x & (x - 1);
}
// 例：x = 1010100
//     x-1 = 1010011
//     x & (x-1) = 1010000

// 7. 提取最右边的1
int extract_rightmost_1(int x) {
    return x & (-x);
}
// 例：x = 1010100
//     -x = 0101100 (补码)
//     x & (-x) = 0000100

// 8. 判断是否为2的幂
bool is_power_of_2(int x) {
    return x > 0 && (x & (x - 1)) == 0;
}
// 2的幂只有一个1：1000, 0100, 0010...
```

### 3.2 进阶技巧

```cpp
// 9. 统计1的个数（Brian Kernighan算法）
int count_ones(int x) {
    int count = 0;
    while (x) {
        x &= (x - 1);  // 每次消除最右边的1
        count++;
    }
    return count;
}

// 更快的方法（查表法）
int count_ones_fast(unsigned int x) {
    x = (x & 0x55555555) + ((x >> 1) & 0x55555555);
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333);
    x = (x & 0x0F0F0F0F) + ((x >> 4) & 0x0F0F0F0F);
    x = (x & 0x00FF00FF) + ((x >> 8) & 0x00FF00FF);
    x = (x & 0x0000FFFF) + ((x >> 16) & 0x0000FFFF);
    return x;
}

// 10. 翻转所有位
unsigned int reverse_bits(unsigned int x) {
    unsigned int result = 0;
    for (int i = 0; i < 32; i++) {
        result <<= 1;
        result |= (x & 1);
        x >>= 1;
    }
    return result;
}

// 11. 交换奇偶位
unsigned int swap_odd_even(unsigned int x) {
    // 0x55555555 = 0101 0101 ...（偶数位）
    // 0xAAAAAAAA = 1010 1010 ...（奇数位）
    return ((x & 0xAAAAAAAA) >> 1) | ((x & 0x55555555) << 1);
}

// 12. 找到缺失的数字（数组0~n，缺少一个）
int find_missing(vector<int>& nums) {
    int result = nums.size();
    for (int i = 0; i < nums.size(); i++) {
        result ^= i ^ nums[i];
    }
    return result;
}

// 13. 只出现一次的数字（其他都出现两次）
int single_number(vector<int>& nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;  // 成对的数异或为0
    }
    return result;
}

// 14. 判断符号是否相同
bool same_sign(int a, int b) {
    return (a ^ b) >= 0;  // 符号位相同则异或后为正
}

// 15. 绝对值（不用分支）
int abs_no_branch(int x) {
    int mask = x >> 31;  // 负数：全1，非负：全0
    return (x + mask) ^ mask;
    // 负数：(x - 1) ^ -1 = -(x - 1) - 1 = -x
    // 非负：x ^ 0 = x
}

// 16. 两数平均值（避免溢出）
int average(int a, int b) {
    return (a & b) + ((a ^ b) >> 1);
}
```

### 3.3 位掩码应用

```cpp
// 权限系统
class Permission {
public:
    static const int READ = 1 << 0;    // 0001
    static const int WRITE = 1 << 1;   // 0010
    static const int EXECUTE = 1 << 2; // 0100
    static const int DELETE = 1 << 3;  // 1000
    
    int flags;
    
    // 添加权限
    void grant(int perm) {
        flags |= perm;
    }
    
    // 撤销权限
    void revoke(int perm) {
        flags &= ~perm;
    }
    
    // 检查权限
    bool has(int perm) {
        return (flags & perm) == perm;
    }
    
    // 切换权限
    void toggle(int perm) {
        flags ^= perm;
    }
};

// 使用示例
Permission p;
p.grant(Permission::READ | Permission::WRITE);
if (p.has(Permission::WRITE)) {
    // 有写权限
}
p.revoke(Permission::WRITE);
```

### 3.4 子集遍历

```cpp
// 遍历集合的所有非空子集
void enumerate_subsets(int set) {
    int subset = set;
    while (subset) {
        // 处理 subset
        cout << bitset<8>(subset) << endl;
        subset = (subset - 1) & set;  // 下一个子集
    }
}

// 示例：set = 1011 (11)
// 遍历：1011, 1010, 1001, 1000, 0011, 0010, 0001
```

## 4. 实战应用

### 4.1 位图（Bitmap）

```cpp
class Bitmap {
private:
    vector<unsigned int> bits;
    int size;
    
public:
    Bitmap(int n) : size(n) {
        bits.resize((n + 31) / 32, 0);  // 每32位一个int
    }
    
    void set(int pos) {
        int idx = pos / 32;
        int offset = pos % 32;
        bits[idx] |= (1U << offset);
    }
    
    void clear(int pos) {
        int idx = pos / 32;
        int offset = pos % 32;
        bits[idx] &= ~(1U << offset);
    }
    
    bool test(int pos) {
        int idx = pos / 32;
        int offset = pos % 32;
        return (bits[idx] >> offset) & 1;
    }
    
    int count() {
        int cnt = 0;
        for (unsigned int x : bits) {
            cnt += __builtin_popcount(x);  // GCC内置函数
        }
        return cnt;
    }
};
```

### 4.2 布隆过滤器核心

```cpp
class BloomFilter {
private:
    Bitmap bitmap;
    int hash_count;
    
    int hash(const string& str, int seed) {
        // 简化的哈希函数
        int h = seed;
        for (char c : str) {
            h = h * 31 + c;
        }
        return abs(h) % bitmap.size();
    }
    
public:
    BloomFilter(int size, int k) : bitmap(size), hash_count(k) {}
    
    void add(const string& str) {
        for (int i = 0; i < hash_count; i++) {
            int pos = hash(str, i);
            bitmap.set(pos);
        }
    }
    
    bool might_contain(const string& str) {
        for (int i = 0; i < hash_count; i++) {
            int pos = hash(str, i);
            if (!bitmap.test(pos)) return false;
        }
        return true;
    }
};
```

### 4.3 状态压缩 DP

```cpp
// 旅行商问题（TSP）- 状态压缩
// dp[mask][i] = 访问了mask集合的城市，当前在城市i的最短路径
int tsp(vector<vector<int>>& dist, int n) {
    vector<vector<int>> dp(1 << n, vector<int>(n, INT_MAX));
    dp[1][0] = 0;  // 从城市0出发
    
    for (int mask = 1; mask < (1 << n); mask++) {
        for (int i = 0; i < n; i++) {
            if (!(mask & (1 << i))) continue;  // i不在mask中
            
            for (int j = 0; j < n; j++) {
                if (mask & (1 << j)) continue;  // j已访问
                
                int next_mask = mask | (1 << j);
                dp[next_mask][j] = min(dp[next_mask][j], 
                                      dp[mask][i] + dist[i][j]);
            }
        }
    }
    
    // 返回最后一个城市回到起点的最短路径
    int full_mask = (1 << n) - 1;
    int result = INT_MAX;
    for (int i = 1; i < n; i++) {
        result = min(result, dp[full_mask][i] + dist[i][0]);
    }
    return result;
}
```

## 5. 常见陷阱

### 5.1 符号扩展

```cpp
// 错误示例
char c = -1;           // 1111 1111
int i = c;             // 1111 1111 1111 1111 1111 1111 1111 1111 (符号扩展)

// 正确做法
unsigned char c = 255; // 1111 1111
int i = c;             // 0000 0000 0000 0000 0000 0000 1111 1111
```

### 5.2 移位超过位宽

```cpp
// 未定义行为！
int x = 1;
int y = x << 32;  // UB！(int是32位)

// 正确做法
if (n < 32) {
    int y = x << n;
}
```

### 5.3 负数右移

```cpp
// 实现定义行为
int x = -8;
int y = x >> 2;  // 可能是 -2（算术右移）或 1073741822（逻辑右移）

// 安全做法：用除法
int y = x / 4;
```

### 5.4 优先级陷阱

```cpp
// 错误
if (x & 1 == 0) {  // 实际是 x & (1 == 0) = x & 0
    // ...
}

// 正确
if ((x & 1) == 0) {
    // ...
}
```

## 6. GCC 内置函数

```cpp
// 统计1的个数
int count = __builtin_popcount(x);          // 32位
int count = __builtin_popcountll(x);        // 64位

// 前导0的个数（从最高位开始）
int clz = __builtin_clz(x);                 // 32位

// 后缀0的个数（从最低位开始）
int ctz = __builtin_ctz(x);                 // 32位

// 奇偶校验（1的个数是否为奇数）
int parity = __builtin_parity(x);           // 32位

// 快速计算 log2
int log2_floor(unsigned int x) {
    return 31 - __builtin_clz(x);
}

int log2_ceil(unsigned int x) {
    return 32 - __builtin_clz(x - 1);
}
```

## 7. 练习题

```cpp
// 1. 反转整数的二进制表示
uint32_t reverseBits(uint32_t n);

// 2. 汉明距离（两数二进制表示中不同位的个数）
int hammingDistance(int x, int y);

// 3. 比特位计数（0到num每个数的1的个数）
vector<int> countBits(int num);

// 4. 数组中唯一成对的元素
int singleNumber(vector<int>& nums);

// 5. 最大单词长度乘积（单词无公共字母）
int maxProduct(vector<string>& words);
```

## 总结

位运算的核心优势：
1. **速度快**：直接操作硬件，无需函数调用
2. **节省空间**：一个int可以存储32个bool
3. **简洁优雅**：某些算法用位运算特别简洁

关键要点：
- 熟练掌握补码表示
- 理解位运算的数学性质
- 注意溢出和未定义行为
- 多用位掩码处理标志位
- 善用编译器内置函数

**记住**：可读性优先！除非性能关键，否则不要过度使用位运算技巧。

## 实战案例：快速幂算法

### 位运算实现快速幂

快速幂算法利用位运算计算 a^n，时间复杂度 O(log n)。核心思想：将指数二进制分解。

```cpp
// 普通方法：O(n)
long long slowPower(int a, int n) {
    long long result = 1;
    for (int i = 0; i < n; ++i) {
        result *= a;
    }
    return result;
}

// 快速幂：O(log n)
long long fastPower(int a, int n) {
    long long result = 1;
    long long base = a;
    
    while (n > 0) {
        if (n & 1) {           // 检查最低位是否为1
            result *= base;
        }
        base *= base;          // base平方
        n >>= 1;               // n右移1位
    }
    return result;
}

// 示例：计算 3^13
// 13 = 1101(二进制) = 8 + 4 + 1
// 3^13 = 3^8 * 3^4 * 3^1
// 
// n=13(1101): n&1=1, result=3,    base=3,   n=6(110)
// n=6 (110):  n&1=0, result=3,    base=9,   n=3(11)
// n=3 (11):   n&1=1, result=27,   base=81,  n=1(1)
// n=1 (1):    n&1=1, result=2187, base=..., n=0
// 结果：2187

// 带取模的快速幂（防止溢出）
long long modPower(long long a, long long n, long long mod) {
    long long result = 1;
    a %= mod;
    
    while (n > 0) {
        if (n & 1) {
            result = (result * a) % mod;
        }
        a = (a * a) % mod;
        n >>= 1;
    }
    return result;
}

// 应用：大数取模、密码学、组合数学
```

**时间复杂度分析：**
- 循环次数 = log₂(n)
- 例：n=1000，只需约10次循环
- 相比普通方法的1000次，提升显著

**实际应用：**
- LeetCode 50. Pow(x, n)
- 模运算：(a^b) mod m
- RSA加密算法
- 矩阵快速幂


/**
 * LeetCode 461. 汉明距离
 * https://leetcode.cn/problems/hamming-distance/
 * 
 * 两个整数之间的汉明距离指的是这两个数字对应二进制位不同的位置的数目。
 * 给你两个整数x和y，计算并返回它们之间的汉明距离。
 * 
 * 位运算
 * 
 * 时间复杂度：O(1)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int hammingDistance(int x, int y) {
        int xor_result = x ^ y;
        int count = 0;
        
        while (xor_result) {
            count += xor_result & 1;
            xor_result >>= 1;
        }
        
        return count;
    }
};

// 测试函数
#include <iostream>
using namespace std;

void testHammingDistance() {
    Solution solution;
    
    int x1 = 1, y1 = 4;
    int result1 = solution.hammingDistance(x1, y1);
    cout << "测试1 x=" << x1 << ", y=" << y1 << ": " << result1 << endl;  // 期望: 2
    
    int x2 = 3, y2 = 1;
    int result2 = solution.hammingDistance(x2, y2);
    cout << "测试2 x=" << x2 << ", y=" << y2 << ": " << result2 << endl;  // 期望: 1
    
    int x3 = 0, y3 = 0;
    int result3 = solution.hammingDistance(x3, y3);
    cout << "测试3 x=" << x3 << ", y=" << y3 << ": " << result3 << endl;  // 期望: 0
}

int main() {
    testHammingDistance();
    return 0;
}

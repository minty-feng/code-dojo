/**
 * LeetCode 190. 颠倒二进制位
 * https://leetcode.cn/problems/reverse-bits/
 * 
 * 颠倒给定的32位无符号整数的二进制位。
 * 
 * 位运算
 * 
 * 时间复杂度：O(1)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t result = 0;
        
        for (int i = 0; i < 32; i++) {
            result = (result << 1) | (n & 1);
            n >>= 1;
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
#include <bitset>
using namespace std;

void printBinary(uint32_t n) {
    cout << "0b" << bitset<32>(n).to_string();
}

void testReverseBits() {
    Solution solution;
    
    uint32_t n1 = 0b00000010100101000001111010011100;
    uint32_t result1 = solution.reverseBits(n1);
    cout << "测试1 n=";
    printBinary(n1);
    cout << ", result=";
    printBinary(result1);
    cout << endl;
    cout << "期望: 0b00111001011110000010100101000000" << endl << endl;
    
    uint32_t n2 = 0b11111111111111111111111111111101;
    uint32_t result2 = solution.reverseBits(n2);
    cout << "测试2 n=";
    printBinary(n2);
    cout << ", result=";
    printBinary(result2);
    cout << endl;
    cout << "期望: 0b10111111111111111111111111111111" << endl << endl;
    
    uint32_t n3 = 0b00000000000000000000000000000001;
    uint32_t result3 = solution.reverseBits(n3);
    cout << "测试3 n=";
    printBinary(n3);
    cout << ", result=";
    printBinary(result3);
    cout << endl;
    cout << "期望: 0b10000000000000000000000000000000" << endl;
}

int main() {
    testReverseBits();
    return 0;
}

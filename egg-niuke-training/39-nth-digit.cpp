/**
 * NC132 数字序列中某一位的数字
 * https://www.nowcoder.com/practice/29311ff7404d44e0b07077f4201418f5
 * 
 * 数字以0123456789101112131415...的格式序列化到一个字符序列中。
 * 
 * 时间复杂度：O(logn)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <string>
using namespace std;

class Solution {
public:
    int findNthDigit(int n) {
        if (n < 0) return -1;
        
        int digit = 1;  // 位数
        long start = 1;  // 该位数的起始数字
        long count = 9;  // 该位数的数字个数
        
        // 确定n所在的位数
        while (n > count) {
            n -= count;
            digit++;
            start *= 10;
            count = 9 * start * digit;
        }
        
        // 确定具体的数字
        long num = start + (n - 1) / digit;
        
        // 确定数字中的第几位
        int digitIndex = (n - 1) % digit;
        
        string numStr = to_string(num);
        return numStr[digitIndex] - '0';
    }
};

int main() {
    Solution solution;
    
    vector<int> testCases = {5, 13, 19, 1000};
    
    for (int n : testCases) {
        int result = solution.findNthDigit(n);
        cout << "第" << n << "位数字: " << result << endl;
    }
    
    return 0;
}


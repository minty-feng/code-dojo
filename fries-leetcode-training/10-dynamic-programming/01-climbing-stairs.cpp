/**
 * LeetCode 70. 爬楼梯
 * https://leetcode.cn/problems/climbing-stairs/
 * 
 * 假设你正在爬楼梯。需要n阶你才能到达楼顶。
 * 每次你可以爬1或2个台阶。你有多少种不同的方法可以爬到楼顶呢？
 * 
 * 动态规划
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        
        // 空间优化版本
        int prev2 = 1;  // dp[i-2]
        int prev1 = 2;  // dp[i-1]
        
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
};

// 测试函数
#include <iostream>
using namespace std;

void testClimbStairs() {
    Solution solution;
    
    int n1 = 2;
    int result1 = solution.climbStairs(n1);
    cout << "n=2: " << result1 << endl;  // 期望: 2
    
    int n2 = 3;
    int result2 = solution.climbStairs(n2);
    cout << "n=3: " << result2 << endl;  // 期望: 3
    
    int n3 = 5;
    int result3 = solution.climbStairs(n3);
    cout << "n=5: " << result3 << endl;  // 期望: 8
}

int main() {
    testClimbStairs();
    return 0;
}

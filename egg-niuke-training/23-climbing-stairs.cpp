/**
 * NC68 跳台阶
 * https://www.nowcoder.com/practice/8c82a5b80378478f9484d87d1c5f12a4
 * 
 * 一只青蛙一次可以跳上1级台阶，也可以跳上2级。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
using namespace std;

class Solution {
public:
    int jumpFloor(int n) {
        if (n <= 2) return n;
        
        int prev2 = 1;  // n=1
        int prev1 = 2;  // n=2
        
        for (int i = 3; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        
        return prev1;
    }
};

int main() {
    Solution solution;
    
    for (int n = 1; n <= 10; n++) {
        int result = solution.jumpFloor(n);
        cout << "n=" << n << ": " << result << "种跳法" << endl;
    }
    
    return 0;
}


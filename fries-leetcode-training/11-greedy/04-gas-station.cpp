/**
 * LeetCode 134. 加油站
 * https://leetcode.cn/problems/gas-station/
 * 
 * 在一条环路上有n个加油站，其中第i个加油站有汽油gas[i]升。
 * 你有一辆油箱容量无限的的汽车，从第i个加油站开往第i+1个加油站需要消耗汽油cost[i]升。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        if (gas.empty() || cost.empty() || gas.size() != cost.size()) {
            return -1;
        }
        
        int totalTank = 0;
        int currentTank = 0;
        int startStation = 0;
        
        for (int i = 0; i < gas.size(); i++) {
            totalTank += gas[i] - cost[i];
            currentTank += gas[i] - cost[i];
            
            // 如果当前油箱为负，说明从startStation到i都不能作为起点
            if (currentTank < 0) {
                startStation = i + 1;
                currentTank = 0;
            }
        }
        
        return totalTank >= 0 ? startStation : -1;
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testCanCompleteCircuit() {
    Solution solution;
    
    vector<int> gas1 = {1, 2, 3, 4, 5};
    vector<int> cost1 = {3, 4, 5, 1, 2};
    int result1 = solution.canCompleteCircuit(gas1, cost1);
    cout << "测试1 gas=[1,2,3,4,5], cost=[3,4,5,1,2]: " << result1 << endl;  // 期望: 3
    
    vector<int> gas2 = {2, 3, 4};
    vector<int> cost2 = {3, 4, 3};
    int result2 = solution.canCompleteCircuit(gas2, cost2);
    cout << "测试2 gas=[2,3,4], cost=[3,4,3]: " << result2 << endl;  // 期望: -1
    
    vector<int> gas3 = {5, 1, 2, 3, 4};
    vector<int> cost3 = {4, 4, 1, 5, 1};
    int result3 = solution.canCompleteCircuit(gas3, cost3);
    cout << "测试3 gas=[5,1,2,3,4], cost=[4,4,1,5,1]: " << result3 << endl;  // 期望: 4
}

int main() {
    testCanCompleteCircuit();
    return 0;
}

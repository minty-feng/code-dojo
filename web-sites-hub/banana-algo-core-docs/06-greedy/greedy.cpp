/**
 * 贪心算法实现
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 区间调度
int intervalScheduling(vector<vector<int>>& intervals) {
    if (intervals.empty()) return 0;
    
    // 按结束时间排序
    sort(intervals.begin(), intervals.end(), 
         [](const vector<int>& a, const vector<int>& b) {
             return a[1] < b[1];
         });
    
    int count = 1;
    int end = intervals[0][1];
    
    for (int i = 1; i < intervals.size(); i++) {
        if (intervals[i][0] >= end) {
            count++;
            end = intervals[i][1];
        }
    }
    
    return count;
}

// 跳跃游戏
bool canJump(const vector<int>& nums) {
    int maxReach = 0;
    
    for (int i = 0; i < nums.size(); i++) {
        if (i > maxReach) {
            return false;
        }
        maxReach = max(maxReach, i + nums[i]);
    }
    
    return true;
}

int jump(const vector<int>& nums) {
    int jumps = 0;
    int currEnd = 0;
    int maxReach = 0;
    
    for (int i = 0; i < nums.size() - 1; i++) {
        maxReach = max(maxReach, i + nums[i]);
        
        if (i == currEnd) {
            jumps++;
            currEnd = maxReach;
        }
    }
    
    return jumps;
}

// 分配饼干
int findContentChildren(vector<int>& g, vector<int>& s) {
    sort(g.begin(), g.end());
    sort(s.begin(), s.end());
    
    int child = 0, cookie = 0;
    
    while (child < g.size() && cookie < s.size()) {
        if (s[cookie] >= g[child]) {
            child++;
        }
        cookie++;
    }
    
    return child;
}

// 买卖股票II
int maxProfit(const vector<int>& prices) {
    int profit = 0;
    
    for (int i = 1; i < prices.size(); i++) {
        if (prices[i] > prices[i-1]) {
            profit += prices[i] - prices[i-1];
        }
    }
    
    return profit;
}

// 加油站
int canCompleteCircuit(const vector<int>& gas, const vector<int>& cost) {
    int totalTank = 0;
    int currTank = 0;
    int start = 0;
    
    for (int i = 0; i < gas.size(); i++) {
        totalTank += gas[i] - cost[i];
        currTank += gas[i] - cost[i];
        
        if (currTank < 0) {
            start = i + 1;
            currTank = 0;
        }
    }
    
    return totalTank >= 0 ? start : -1;
}

// 分发糖果
int candy(const vector<int>& ratings) {
    int n = ratings.size();
    vector<int> candies(n, 1);
    
    // 从左到右
    for (int i = 1; i < n; i++) {
        if (ratings[i] > ratings[i-1]) {
            candies[i] = candies[i-1] + 1;
        }
    }
    
    // 从右到左
    for (int i = n - 2; i >= 0; i--) {
        if (ratings[i] > ratings[i+1]) {
            candies[i] = max(candies[i], candies[i+1] + 1);
        }
    }
    
    int sum = 0;
    for (int c : candies) sum += c;
    return sum;
}

int main() {
    cout << "=== 贪心算法演示 ===" << endl << endl;
    
    // 区间调度
    vector<vector<int>> intervals = {{1,3}, {2,4}, {3,5}, {1,2}};
    cout << "区间调度 [[1,3],[2,4],[3,5],[1,2]]:" << endl;
    cout << "  最多不重叠区间: " << intervalScheduling(intervals) << endl << endl;
    
    // 跳跃游戏
    vector<int> nums = {2,3,1,1,4};
    cout << "跳跃游戏 [2,3,1,1,4]:" << endl;
    cout << "  能否跳到最后: " << (canJump(nums) ? "是" : "否") << endl;
    cout << "  最少跳跃次数: " << jump(nums) << endl << endl;
    
    // 分配饼干
    vector<int> g = {1,2,3};
    vector<int> s = {1,1};
    cout << "分配饼干 g=[1,2,3], s=[1,1]:" << endl;
    cout << "  满足孩子数: " << findContentChildren(g, s) << endl << endl;
    
    // 买卖股票
    vector<int> prices = {7,1,5,3,6,4};
    cout << "买卖股票II [7,1,5,3,6,4]:" << endl;
    cout << "  最大利润: " << maxProfit(prices) << endl << endl;
    
    // 加油站
    vector<int> gas = {1,2,3,4,5};
    vector<int> cost = {3,4,5,1,2};
    cout << "加油站 gas=[1,2,3,4,5], cost=[3,4,5,1,2]:" << endl;
    cout << "  起始站: " << canCompleteCircuit(gas, cost) << endl << endl;
    
    // 分发糖果
    vector<int> ratings = {1,0,2};
    cout << "分发糖果 [1,0,2]:" << endl;
    cout << "  最少糖果数: " << candy(ratings) << endl;
    
    return 0;
}


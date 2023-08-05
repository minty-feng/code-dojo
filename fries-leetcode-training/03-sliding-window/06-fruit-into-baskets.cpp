/**
 * LeetCode 904. 水果成篮
 * https://leetcode.cn/problems/fruit-into-baskets/
 * 
 * 你正在探访一家农场，农场从左到右种植了一排果树。这些树用一个整数数组fruits表示，
 * 其中fruits[i]是第i棵树上的水果种类。
 * 
 * 你想要尽可能多地收集水果。然而，农场的主人设定了一些严格的规则，你必须按照要求采摘水果：
 * 1. 你只有两个篮子，并且每个篮子只能装单一类型的水果
 * 2. 你可以选择任意一棵树开始采摘，你必须从每棵树上恰好摘一个水果
 * 3. 一旦你走到某棵树前，但水果不符合篮子的水果类型，那么就必须停止采摘
 * 
 * 滑动窗口
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        int left = 0;
        int max_fruits = 0;
        unordered_map<int, int> fruit_count;
        
        for (int right = 0; right < fruits.size(); right++) {
            // 扩展窗口
            int fruit = fruits[right];
            fruit_count[fruit]++;
            
            // 收缩窗口
            while (fruit_count.size() > 2) {
                int left_fruit = fruits[left];
                fruit_count[left_fruit]--;
                if (fruit_count[left_fruit] == 0) {
                    fruit_count.erase(left_fruit);
                }
                left++;
            }
            
            // 更新结果
            max_fruits = max(max_fruits, right - left + 1);
        }
        
        return max_fruits;
    }
};

// 测试函数
#include <iostream>
void testTotalFruit() {
    Solution solution;
    
    // 测试用例1
    vector<int> fruits1 = {1, 2, 1, 2, 3};
    int result1 = solution.totalFruit(fruits1);
    cout << "测试1: " << result1 << endl;
    
    // 测试用例2
    vector<int> fruits2 = {0, 1, 2, 2};
    int result2 = solution.totalFruit(fruits2);
    cout << "测试2: " << result2 << endl;
    
    // 测试用例3
    vector<int> fruits3 = {1, 2, 3, 2, 2};
    int result3 = solution.totalFruit(fruits3);
    cout << "测试3: " << result3 << endl;
}

int main() {
    testTotalFruit();
    return 0;
}

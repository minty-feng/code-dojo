/**
 * LeetCode 103. 二叉树的锯齿形层序遍历
 * https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/
 * 
 * 给你二叉树的根节点root，返回其节点值的锯齿形层序遍历。
 * 
 * BFS + 方向控制
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(w) w为树的最大宽度
 */

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (!root) {
            return result;
        }
        
        queue<TreeNode*> q;
        q.push(root);
        bool left_to_right = true;
        
        while (!q.empty()) {
            int level_size = q.size();
            vector<int> level;
            
            for (int i = 0; i < level_size; i++) {
                TreeNode* node = q.front();
                q.pop();
                level.push_back(node->val);
                
                if (node->left) {
                    q.push(node->left);
                }
                if (node->right) {
                    q.push(node->right);
                }
            }
            
            if (!left_to_right) {
                reverse(level.begin(), level.end());
            }
            
            result.push_back(level);
            left_to_right = !left_to_right;
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

void testZigzagLevelOrder() {
    Solution solution;
    
    // 创建测试二叉树: [3,9,20,null,null,15,7]
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    
    vector<vector<int>> result = solution.zigzagLevelOrder(root);
    
    cout << "锯齿形层序遍历结果: [";
    for (int i = 0; i < result.size(); i++) {
        cout << "[";
        for (int j = 0; j < result[i].size(); j++) {
            cout << result[i][j];
            if (j < result[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testZigzagLevelOrder();
    return 0;
}

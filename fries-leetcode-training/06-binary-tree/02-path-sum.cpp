/**
 * LeetCode 112. 路径总和
 * https://leetcode.cn/problems/path-sum/
 * 
 * 给你二叉树的根节点root和一个表示目标和的整数targetSum。
 * 判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和targetSum。
 * 
 * DFS递归
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(h) h为树的高度
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
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (!root) {
            return false;
        }
        
        if (!root->left && !root->right) {
            return root->val == targetSum;
        }
        
        return hasPathSum(root->left, targetSum - root->val) ||
               hasPathSum(root->right, targetSum - root->val);
    }
};

// 测试函数
#include <iostream>
void testHasPathSum() {
    Solution solution;
    
    // 创建测试二叉树: [5,4,8,11,null,13,4,7,2,null,null,null,1]
    TreeNode* root = new TreeNode(5);
    root->left = new TreeNode(4);
    root->right = new TreeNode(8);
    root->left->left = new TreeNode(11);
    root->right->left = new TreeNode(13);
    root->right->right = new TreeNode(4);
    root->left->left->left = new TreeNode(7);
    root->left->left->right = new TreeNode(2);
    root->right->right->right = new TreeNode(1);
    
    bool result1 = solution.hasPathSum(root, 22);
    cout << "是否存在路径和为22: " << (result1 ? "True" : "False") << endl;  // 期望: True
    
    bool result2 = solution.hasPathSum(root, 26);
    cout << "是否存在路径和为26: " << (result2 ? "True" : "False") << endl;  // 期望: True
}

int main() {
    testHasPathSum();
    return 0;
}

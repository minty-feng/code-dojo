/**
 * LeetCode 104. 二叉树的最大深度
 * https://leetcode.cn/problems/maximum-depth-of-binary-tree/
 * 
 * 给定一个二叉树，找出其最大深度。
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
    int maxDepth(TreeNode* root) {
        if (!root) {
            return 0;
        }
        
        int left_depth = maxDepth(root->left);
        int right_depth = maxDepth(root->right);
        
        return max(left_depth, right_depth) + 1;
    }
};

// 测试函数
#include <iostream>
void testMaxDepth() {
    Solution solution;
    
    // 创建测试二叉树: [3,9,20,null,null,15,7]
    //     3
    //    / \
    //   9  20
    //     /  \
    //    15   7
    
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    
    int result = solution.maxDepth(root);
    cout << "最大深度: " << result << endl;  // 期望: 3
}

int main() {
    testMaxDepth();
    return 0;
}

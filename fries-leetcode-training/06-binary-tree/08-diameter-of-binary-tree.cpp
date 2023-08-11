/**
 * LeetCode 543. 二叉树的直径
 * https://leetcode.cn/problems/diameter-of-binary-tree/
 * 
 * 给定一棵二叉树，你需要计算它的直径长度。一棵二叉树的直径长度是任意两个结点路径长度中的最大值。
 * 这条路径可能穿过也可能不穿过根结点。
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
    int diameterOfBinaryTree(TreeNode* root) {
        int max_diameter = 0;
        maxDepth(root, max_diameter);
        return max_diameter;
    }
    
private:
    int maxDepth(TreeNode* node, int& max_diameter) {
        if (!node) {
            return 0;
        }
        
        int left_depth = maxDepth(node->left, max_diameter);
        int right_depth = maxDepth(node->right, max_diameter);
        
        // 更新最大直径（经过当前节点的最长路径）
        max_diameter = max(max_diameter, left_depth + right_depth);
        
        // 返回当前节点的最大深度
        return max(left_depth, right_depth) + 1;
    }
};

// 测试函数
#include <iostream>
using namespace std;

void testDiameterOfBinaryTree() {
    Solution solution;
    
    // 创建测试二叉树: [1,2,3,4,5]
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    
    int result = solution.diameterOfBinaryTree(root);
    cout << "二叉树直径: " << result << endl;  // 期望: 3
    
    // 测试用例2: 单节点
    TreeNode* root2 = new TreeNode(1);
    int result2 = solution.diameterOfBinaryTree(root2);
    cout << "单节点直径: " << result2 << endl;  // 期望: 0
}

int main() {
    testDiameterOfBinaryTree();
    return 0;
}

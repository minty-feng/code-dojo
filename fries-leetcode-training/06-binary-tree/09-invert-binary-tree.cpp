/**
 * LeetCode 226. 翻转二叉树
 * https://leetcode.cn/problems/invert-binary-tree/
 * 
 * 给你一棵二叉树的根节点root，翻转这棵二叉树，并返回其根节点。
 * 
 * 递归
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
    TreeNode* invertTree(TreeNode* root) {
        if (!root) {
            return nullptr;
        }
        
        // 翻转左右子树
        TreeNode* temp = root->left;
        root->left = root->right;
        root->right = temp;
        
        // 递归翻转子树
        invertTree(root->left);
        invertTree(root->right);
        
        return root;
    }
};

// 测试函数
#include <iostream>
using namespace std;

void testInvertTree() {
    Solution solution;
    
    // 创建测试二叉树: [4,2,7,1,3,6,9]
    TreeNode* root = new TreeNode(4);
    root->left = new TreeNode(2);
    root->right = new TreeNode(7);
    root->left->left = new TreeNode(1);
    root->left->right = new TreeNode(3);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(9);
    
    TreeNode* inverted = solution.invertTree(root);
    
    cout << "翻转后的根节点值: " << inverted->val << endl;
    cout << "左子树根节点值: " << (inverted->left ? to_string(inverted->left->val) : "null") << endl;
    cout << "右子树根节点值: " << (inverted->right ? to_string(inverted->right->val) : "null") << endl;
}

int main() {
    testInvertTree();
    return 0;
}

/**
 * LeetCode 98. 验证二叉搜索树
 * https://leetcode.cn/problems/validate-binary-search-tree/
 * 
 * 给你一个二叉树的根节点root，判断其是否是一个有效的二叉搜索树。
 * 
 * 中序遍历
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
    bool isValidBST(TreeNode* root) {
        return validate(root, LONG_MIN, LONG_MAX);
    }
    
private:
    bool validate(TreeNode* node, long min_val, long max_val) {
        if (!node) {
            return true;
        }
        
        if (node->val <= min_val || node->val >= max_val) {
            return false;
        }
        
        return validate(node->left, min_val, node->val) &&
               validate(node->right, node->val, max_val);
    }
};

// 测试函数
#include <iostream>
#include <climits>
using namespace std;

void testIsValidBST() {
    Solution solution;
    
    // 测试用例1: [2,1,3] - 有效BST
    TreeNode* root1 = new TreeNode(2);
    root1->left = new TreeNode(1);
    root1->right = new TreeNode(3);
    
    bool result1 = solution.isValidBST(root1);
    cout << "测试1 [2,1,3]: " << (result1 ? "True" : "False") << endl;  // 期望: True
    
    // 测试用例2: [5,1,4,null,null,3,6] - 无效BST
    TreeNode* root2 = new TreeNode(5);
    root2->left = new TreeNode(1);
    root2->right = new TreeNode(4);
    root2->right->left = new TreeNode(3);
    root2->right->right = new TreeNode(6);
    
    bool result2 = solution.isValidBST(root2);
    cout << "测试2 [5,1,4,null,null,3,6]: " << (result2 ? "True" : "False") << endl;  // 期望: False
}

int main() {
    testIsValidBST();
    return 0;
}

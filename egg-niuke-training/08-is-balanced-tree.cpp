/**
 * NC62 判断是不是平衡二叉树
 * https://www.nowcoder.com/practice/8b3b95850edb4115918ecebdf1b4d222
 * 
 * 输入一棵节点数为 n 二叉树，判断该二叉树是否是平衡二叉树。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(h)
 */

#include <iostream>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    bool IsBalanced(TreeNode* root) {
        return height(root) != -1;
    }

private:
    int height(TreeNode* node) {
        if (!node) return 0;
        
        int leftHeight = height(node->left);
        if (leftHeight == -1) return -1;
        
        int rightHeight = height(node->right);
        if (rightHeight == -1) return -1;
        
        // 检查平衡性
        if (abs(leftHeight - rightHeight) > 1) {
            return -1;
        }
        
        return max(leftHeight, rightHeight) + 1;
    }
};

int main() {
    Solution solution;
    
    // 平衡二叉树
    TreeNode* root1 = new TreeNode(1);
    root1->left = new TreeNode(2);
    root1->right = new TreeNode(3);
    root1->left->left = new TreeNode(4);
    root1->left->right = new TreeNode(5);
    
    cout << "树1是否平衡: " << (solution.IsBalanced(root1) ? "是" : "否") << endl;
    
    // 不平衡二叉树
    TreeNode* root2 = new TreeNode(1);
    root2->left = new TreeNode(2);
    root2->left->left = new TreeNode(3);
    root2->left->left->left = new TreeNode(4);
    
    cout << "树2是否平衡: " << (solution.IsBalanced(root2) ? "是" : "否") << endl;
    
    return 0;
}


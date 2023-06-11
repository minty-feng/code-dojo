/**
 * NC72 二叉树的最大深度
 * https://www.nowcoder.com/practice/8a2b2bf6c19b4f23a9bdb9b233eefa73
 * 
 * 求给定二叉树的最大深度。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(h)
 */

#include <iostream>
#include <queue>
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
    /**
     * 方法1：递归
     */
    int maxDepth_Recursive(TreeNode* root) {
        if (!root) {
            return 0;
        }
        
        int leftDepth = maxDepth_Recursive(root->left);
        int rightDepth = maxDepth_Recursive(root->right);
        
        return max(leftDepth, rightDepth) + 1;
    }
    
    /**
     * 方法2：BFS层序遍历
     */
    int maxDepth_BFS(TreeNode* root) {
        if (!root) {
            return 0;
        }
        
        queue<TreeNode*> q;
        q.push(root);
        int depth = 0;
        
        while (!q.empty()) {
            int levelSize = q.size();
            depth++;
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode* node = q.front();
                q.pop();
                
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
        }
        
        return depth;
    }
};

int main() {
    // 创建二叉树
    //       1
    //      / \
    //     2   3
    //    / \
    //   4   5
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    
    Solution solution;
    
    cout << "递归法 - 最大深度: " << solution.maxDepth_Recursive(root) << endl;
    cout << "BFS法 - 最大深度: " << solution.maxDepth_BFS(root) << endl;
    
    return 0;
}


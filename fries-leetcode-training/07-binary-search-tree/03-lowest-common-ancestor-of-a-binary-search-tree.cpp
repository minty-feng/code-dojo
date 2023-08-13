/**
 * LeetCode 235. 二叉搜索树的最近公共祖先
 * https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/
 * 
 * 给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。
 * 
 * 利用BST性质
 * 
 * 时间复杂度：O(h) h为树的高度
 * 空间复杂度：O(1)
 */

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        while (root) {
            // 如果p和q都在左子树
            if (p->val < root->val && q->val < root->val) {
                root = root->left;
            }
            // 如果p和q都在右子树
            else if (p->val > root->val && q->val > root->val) {
                root = root->right;
            }
            // 否则当前节点就是最近公共祖先
            else {
                return root;
            }
        }
        return nullptr;
    }
};

// 测试函数
#include <iostream>
using namespace std;

void testLowestCommonAncestor() {
    Solution solution;
    
    // 创建测试二叉搜索树: [6,2,8,0,4,7,9,null,null,3,5]
    TreeNode* root = new TreeNode(6);
    root->left = new TreeNode(2);
    root->right = new TreeNode(8);
    root->left->left = new TreeNode(0);
    root->left->right = new TreeNode(4);
    root->right->left = new TreeNode(7);
    root->right->right = new TreeNode(9);
    root->left->right->left = new TreeNode(3);
    root->left->right->right = new TreeNode(5);
    
    TreeNode* p = root->left;      // 节点2
    TreeNode* q = root->right;    // 节点8
    
    TreeNode* result1 = solution.lowestCommonAncestor(root, p, q);
    cout << "节点2和节点8的最近公共祖先: " << result1->val << endl;  // 期望: 6
    
    TreeNode* p2 = root->left->left;      // 节点0
    TreeNode* q2 = root->left->right->right;  // 节点5
    
    TreeNode* result2 = solution.lowestCommonAncestor(root, p2, q2);
    cout << "节点0和节点5的最近公共祖先: " << result2->val << endl;  // 期望: 2
}

int main() {
    testLowestCommonAncestor();
    return 0;
}

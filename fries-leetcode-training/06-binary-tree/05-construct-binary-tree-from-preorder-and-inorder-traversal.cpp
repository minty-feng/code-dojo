/**
 * LeetCode 105. 从前序与中序遍历序列构造二叉树
 * https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
 * 
 * 给定两个整数数组preorder和inorder，其中preorder是二叉树的先序遍历，inorder是同一棵树的中序遍历，
 * 请构造二叉树并返回其根节点。
 * 
 * 递归构建
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
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
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        if (preorder.empty() || inorder.empty()) {
            return nullptr;
        }
        
        // 创建中序遍历的索引映射
        unordered_map<int, int> inorder_map;
        for (int i = 0; i < inorder.size(); i++) {
            inorder_map[inorder[i]] = i;
        }
        
        int preorder_idx = 0;
        return buildTreeHelper(preorder, inorder_map, preorder_idx, 0, inorder.size() - 1);
    }
    
private:
    TreeNode* buildTreeHelper(vector<int>& preorder, unordered_map<int, int>& inorder_map, 
                               int& preorder_idx, int left, int right) {
        if (left > right) {
            return nullptr;
        }
        
        // 选择preorder_idx位置的元素作为根节点
        int root_val = preorder[preorder_idx++];
        TreeNode* root = new TreeNode(root_val);
        
        // 在中序遍历中找到根节点的位置
        int root_index = inorder_map[root_val];
        
        // 递归构建左右子树
        root->left = buildTreeHelper(preorder, inorder_map, preorder_idx, left, root_index - 1);
        root->right = buildTreeHelper(preorder, inorder_map, preorder_idx, root_index + 1, right);
        
        return root;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

void testBuildTree() {
    Solution solution;
    
    vector<int> preorder = {3, 9, 20, 15, 7};
    vector<int> inorder = {9, 3, 15, 20, 7};
    
    TreeNode* root = solution.buildTree(preorder, inorder);
    
    // 验证构造的树
    cout << "构造的树根节点值: " << root->val << endl;
    cout << "左子树根节点值: " << (root->left ? to_string(root->left->val) : "null") << endl;
    cout << "右子树根节点值: " << (root->right ? to_string(root->right->val) : "null") << endl;
}

int main() {
    testBuildTree();
    return 0;
}

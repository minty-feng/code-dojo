/**
 * LeetCode 230. 二叉搜索树中第K小的元素
 * https://leetcode.cn/problems/kth-smallest-element-in-a-bst/
 * 
 * 给定一个二叉搜索树的根节点root，和一个整数k，请你设计一个算法查找其中第k个最小元素。
 * 
 * 中序遍历
 * 
 * 时间复杂度：O(h + k) h为树的高度
 * 空间复杂度：O(h)
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
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> st;
        TreeNode* current = root;
        
        while (true) {
            // 遍历到最左节点
            while (current) {
                st.push(current);
                current = current->left;
            }
            
            // 弹出节点
            current = st.top();
            st.pop();
            k--;
            
            if (k == 0) {
                return current->val;
            }
            
            // 访问右子树
            current = current->right;
        }
    }
};

// 测试函数
#include <iostream>
#include <stack>
using namespace std;

void testKthSmallest() {
    Solution solution;
    
    // 创建测试二叉搜索树: [3,1,4,null,2]
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(1);
    root->right = new TreeNode(4);
    root->left->right = new TreeNode(2);
    
    int result1 = solution.kthSmallest(root, 1);
    cout << "第1小的元素: " << result1 << endl;  // 期望: 1
    
    int result2 = solution.kthSmallest(root, 3);
    cout << "第3小的元素: " << result2 << endl;  // 期望: 3
}

int main() {
    testKthSmallest();
    return 0;
}

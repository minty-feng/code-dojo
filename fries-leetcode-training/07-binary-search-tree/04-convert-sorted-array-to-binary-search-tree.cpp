/**
 * LeetCode 108. 将有序数组转换为二叉搜索树
 * https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/
 * 
 * 给你一个整数数组nums，其中元素已经按升序排列，请你将其转换为一棵高度平衡的二叉搜索树。
 * 
 * 递归构建
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(log n)
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
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        if (nums.empty()) {
            return nullptr;
        }
        
        return buildTree(nums, 0, nums.size() - 1);
    }
    
private:
    TreeNode* buildTree(vector<int>& nums, int left, int right) {
        if (left > right) {
            return nullptr;
        }
        
        // 选择中间元素作为根节点
        int mid = left + (right - left) / 2;
        TreeNode* root = new TreeNode(nums[mid]);
        
        // 递归构建左右子树
        root->left = buildTree(nums, left, mid - 1);
        root->right = buildTree(nums, mid + 1, right);
        
        return root;
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testSortedArrayToBST() {
    Solution solution;
    
    vector<int> nums1 = {-10, -3, 0, 5, 9};
    TreeNode* root1 = solution.sortedArrayToBST(nums1);
    
    cout << "构造的BST根节点值: " << root1->val << endl;
    cout << "左子树根节点值: " << (root1->left ? to_string(root1->left->val) : "null") << endl;
    cout << "右子树根节点值: " << (root1->right ? to_string(root1->right->val) : "null") << endl;
    
    vector<int> nums2 = {1, 3};
    TreeNode* root2 = solution.sortedArrayToBST(nums2);
    
    cout << "构造的BST根节点值: " << root2->val << endl;
    cout << "左子树根节点值: " << (root2->left ? to_string(root2->left->val) : "null") << endl;
    cout << "右子树根节点值: " << (root2->right ? to_string(root2->right->val) : "null") << endl;
}

int main() {
    testSortedArrayToBST();
    return 0;
}

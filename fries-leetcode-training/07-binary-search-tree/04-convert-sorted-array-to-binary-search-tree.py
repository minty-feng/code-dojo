"""
LeetCode 108. 将有序数组转换为二叉搜索树
https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/

给你一个整数数组nums，其中元素已经按升序排列，请你将其转换为一棵高度平衡的二叉搜索树。

递归构建

时间复杂度：O(n)
空间复杂度：O(log n)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sorted_array_to_bst(nums):
    """
    将有序数组转换为二叉搜索树 - 递归法
    
    Args:
        nums: 升序排列的整数数组
        
    Returns:
        高度平衡的二叉搜索树根节点
    """
    if not nums:
        return None
    
    def build_tree(left, right):
        if left > right:
            return None
        
        # 选择中间元素作为根节点
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        
        # 递归构建左右子树
        root.left = build_tree(left, mid - 1)
        root.right = build_tree(mid + 1, right)
        
        return root
    
    return build_tree(0, len(nums) - 1)


def test_sorted_array_to_bst():
    """测试函数"""
    # 测试用例1
    nums1 = [-10, -3, 0, 5, 9]
    root1 = sorted_array_to_bst(nums1)
    
    def inorder_traversal(root):
        if not root:
            return []
        return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)
    
    result1 = inorder_traversal(root1)
    print(f"构造的BST中序遍历: {result1}")
    print(f"是否与原数组相同: {result1 == nums1}")
    
    # 测试用例2
    nums2 = [1, 3]
    root2 = sorted_array_to_bst(nums2)
    result2 = inorder_traversal(root2)
    print(f"构造的BST中序遍历: {result2}")
    print(f"是否与原数组相同: {result2 == nums2}")


if __name__ == "__main__":
    test_sorted_array_to_bst()

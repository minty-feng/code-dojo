"""
LeetCode 112. 路径总和
https://leetcode.cn/problems/path-sum/

给你二叉树的根节点root和一个表示目标和的整数targetSum。
判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和targetSum。

DFS递归

时间复杂度：O(n)
空间复杂度：O(h) h为树的高度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum(root, target_sum):
    """
    路径总和 - DFS递归法
    
    Args:
        root: 二叉树根节点
        target_sum: 目标和
        
    Returns:
        是否存在路径
    """
    if not root:
        return False
    
    if not root.left and not root.right:
        return root.val == target_sum
    
    return (has_path_sum(root.left, target_sum - root.val) or
            has_path_sum(root.right, target_sum - root.val))


def test_has_path_sum():
    """测试函数"""
    # 创建测试二叉树: [5,4,8,11,null,13,4,7,2,null,null,null,1]
    #       5
    #      / \
    #     4   8
    #    /   / \
    #   11  13  4
    #  / \      \
    # 7  2      1
    
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.right.right = TreeNode(1)
    
    result1 = has_path_sum(root, 22)
    print(f"是否存在路径和为22: {result1}")  # 期望: True
    
    result2 = has_path_sum(root, 26)
    print(f"是否存在路径和为26: {result2}")  # 期望: True


if __name__ == "__main__":
    test_has_path_sum()

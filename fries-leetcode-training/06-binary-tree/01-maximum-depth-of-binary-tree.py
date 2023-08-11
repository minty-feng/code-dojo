"""
LeetCode 104. 二叉树的最大深度
https://leetcode.cn/problems/maximum-depth-of-binary-tree/

给定一个二叉树，找出其最大深度。

DFS递归

时间复杂度：O(n)
空间复杂度：O(h) h为树的高度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root):
    """
    二叉树的最大深度 - DFS递归法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        最大深度
    """
    if not root:
        return 0
    
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return max(left_depth, right_depth) + 1


def test_max_depth():
    """测试函数"""
    # 创建测试二叉树: [3,9,20,null,null,15,7]
    #     3
    #    / \
    #   9  20
    #     /  \
    #    15   7
    
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    result = max_depth(root)
    print(f"最大深度: {result}")  # 期望: 3


if __name__ == "__main__":
    test_max_depth()

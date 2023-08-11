"""
LeetCode 543. 二叉树的直径
https://leetcode.cn/problems/diameter-of-binary-tree/

给定一棵二叉树，你需要计算它的直径长度。一棵二叉树的直径长度是任意两个结点路径长度中的最大值。
这条路径可能穿过也可能不穿过根结点。

DFS递归

时间复杂度：O(n)
空间复杂度：O(h) h为树的高度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter_of_binary_tree(root):
    """
    二叉树的直径 - DFS递归法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        二叉树的直径
    """
    max_diameter = 0
    
    def max_depth(node):
        nonlocal max_diameter
        
        if not node:
            return 0
        
        left_depth = max_depth(node.left)
        right_depth = max_depth(node.right)
        
        # 更新最大直径（经过当前节点的最长路径）
        max_diameter = max(max_diameter, left_depth + right_depth)
        
        # 返回当前节点的最大深度
        return max(left_depth, right_depth) + 1
    
    max_depth(root)
    return max_diameter


def test_diameter_of_binary_tree():
    """测试函数"""
    # 创建测试二叉树: [1,2,3,4,5]
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    result = diameter_of_binary_tree(root)
    print(f"二叉树直径: {result}")  # 期望: 3 (路径4-2-1-3或路径5-2-1-3)
    
    # 测试用例2: 单节点
    root2 = TreeNode(1)
    result2 = diameter_of_binary_tree(root2)
    print(f"单节点直径: {result2}")  # 期望: 0


if __name__ == "__main__":
    test_diameter_of_binary_tree()

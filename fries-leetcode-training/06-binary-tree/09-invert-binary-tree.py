"""
LeetCode 226. 翻转二叉树
https://leetcode.cn/problems/invert-binary-tree/

给你一棵二叉树的根节点root，翻转这棵二叉树，并返回其根节点。

递归

时间复杂度：O(n)
空间复杂度：O(h) h为树的高度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root):
    """
    翻转二叉树 - 递归法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        翻转后的二叉树根节点
    """
    if not root:
        return None
    
    # 翻转左右子树
    root.left, root.right = root.right, root.left
    
    # 递归翻转子树
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root


def test_invert_tree():
    """测试函数"""
    # 创建测试二叉树: [4,2,7,1,3,6,9]
    #     4
    #    / \
    #   2   7
    #  / \ / \
    # 1  3 6  9
    
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(9)
    
    inverted = invert_tree(root)
    
    def print_tree(node):
        if not node:
            return
        print(node.val, end=" ")
        print_tree(node.left)
        print_tree(node.right)
    
    print("翻转后的前序遍历:")
    print_tree(inverted)
    print()


if __name__ == "__main__":
    test_invert_tree()

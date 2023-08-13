"""
LeetCode 98. 验证二叉搜索树
https://leetcode.cn/problems/validate-binary-search-tree/

给你一个二叉树的根节点root，判断其是否是一个有效的二叉搜索树。

中序遍历

时间复杂度：O(n)
空间复杂度：O(h) h为树的高度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root):
    """
    验证二叉搜索树 - 中序遍历法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        是否为有效的BST
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


def test_is_valid_bst():
    """测试函数"""
    # 测试用例1: [2,1,3] - 有效BST
    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)
    
    result1 = is_valid_bst(root1)
    print(f"测试1 [2,1,3]: {result1}")  # 期望: True
    
    # 测试用例2: [5,1,4,null,null,3,6] - 无效BST
    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)
    
    result2 = is_valid_bst(root2)
    print(f"测试2 [5,1,4,null,null,3,6]: {result2}")  # 期望: False


if __name__ == "__main__":
    test_is_valid_bst()

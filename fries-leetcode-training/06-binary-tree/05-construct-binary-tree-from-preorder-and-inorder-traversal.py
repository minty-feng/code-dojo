"""
LeetCode 105. 从前序与中序遍历序列构造二叉树
https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

给定两个整数数组preorder和inorder，其中preorder是二叉树的先序遍历，inorder是同一棵树的中序遍历，
请构造二叉树并返回其根节点。

递归构建

时间复杂度：O(n)
空间复杂度：O(n)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(preorder, inorder):
    """
    从前序与中序遍历序列构造二叉树 - 递归法
    
    Args:
        preorder: 前序遍历序列
        inorder: 中序遍历序列
        
    Returns:
        构造的二叉树根节点
    """
    if not preorder or not inorder:
        return None
    
    # 前序遍历的第一个元素是根节点
    root_val = preorder[0]
    root = TreeNode(root_val)
    
    # 在中序遍历中找到根节点的位置
    root_index = inorder.index(root_val)
    
    # 递归构建左右子树
    root.left = build_tree(preorder[1:root_index+1], inorder[:root_index])
    root.right = build_tree(preorder[root_index+1:], inorder[root_index+1:])
    
    return root


def build_tree_optimized(preorder, inorder):
    """
    从前序与中序遍历序列构造二叉树 - 优化版本
    
    Args:
        preorder: 前序遍历序列
        inorder: 中序遍历序列
        
    Returns:
        构造的二叉树根节点
    """
    if not preorder or not inorder:
        return None
    
    # 创建中序遍历的索引映射
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    preorder_idx = 0
    
    def build_tree_helper(left, right):
        nonlocal preorder_idx
        
        if left > right:
            return None
        
        # 选择preorder_idx位置的元素作为根节点
        root_val = preorder[preorder_idx]
        root = TreeNode(root_val)
        preorder_idx += 1
        
        # 在中序遍历中找到根节点的位置
        root_index = inorder_map[root_val]
        
        # 递归构建左右子树
        root.left = build_tree_helper(left, root_index - 1)
        root.right = build_tree_helper(root_index + 1, right)
        
        return root
    
    return build_tree_helper(0, len(inorder) - 1)


def test_build_tree():
    """测试函数"""
    # 测试用例1
    preorder1 = [3, 9, 20, 15, 7]
    inorder1 = [9, 3, 15, 20, 7]
    
    root1 = build_tree(preorder1, inorder1)
    
    def preorder_traversal(root):
        if not root:
            return []
        return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)
    
    def inorder_traversal(root):
        if not root:
            return []
        return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)
    
    result_preorder1 = preorder_traversal(root1)
    result_inorder1 = inorder_traversal(root1)
    
    print(f"构造的树前序遍历: {result_preorder1}")
    print(f"构造的树中序遍历: {result_inorder1}")
    print(f"前序遍历匹配: {result_preorder1 == preorder1}")
    print(f"中序遍历匹配: {result_inorder1 == inorder1}")


if __name__ == "__main__":
    test_build_tree()

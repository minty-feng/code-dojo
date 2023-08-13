"""
LeetCode 230. 二叉搜索树中第K小的元素
https://leetcode.cn/problems/kth-smallest-element-in-a-bst/

给定一个二叉搜索树的根节点root，和一个整数k，请你设计一个算法查找其中第k个最小元素。

中序遍历

时间复杂度：O(h + k) h为树的高度
空间复杂度：O(h)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def kth_smallest(root, k):
    """
    二叉搜索树中第K小的元素 - 中序遍历法
    
    Args:
        root: 二叉搜索树根节点
        k: 第k个最小元素
        
    Returns:
        第k个最小元素的值
    """
    stack = []
    current = root
    
    while True:
        # 遍历到最左节点
        while current:
            stack.append(current)
            current = current.left
        
        # 弹出节点
        current = stack.pop()
        k -= 1
        
        if k == 0:
            return current.val
        
        # 访问右子树
        current = current.right


def kth_smallest_recursive(root, k):
    """
    二叉搜索树中第K小的元素 - 递归中序遍历法
    
    Args:
        root: 二叉搜索树根节点
        k: 第k个最小元素
        
    Returns:
        第k个最小元素的值
    """
    result = []
    
    def inorder(node):
        if node and len(result) < k:
            inorder(node.left)
            if len(result) < k:
                result.append(node.val)
            inorder(node.right)
    
    inorder(root)
    return result[k-1]


def test_kth_smallest():
    """测试函数"""
    # 创建测试二叉搜索树: [3,1,4,null,2]
    #     3
    #    / \
    #   1   4
    #    \
    #     2
    
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.right = TreeNode(2)
    
    result1 = kth_smallest(root, 1)
    print(f"第1小的元素: {result1}")  # 期望: 1
    
    result2 = kth_smallest(root, 3)
    print(f"第3小的元素: {result2}")  # 期望: 3
    
    result3 = kth_smallest_recursive(root, 2)
    print(f"递归方法第2小的元素: {result3}")  # 期望: 2


if __name__ == "__main__":
    test_kth_smallest()

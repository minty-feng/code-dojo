"""
LeetCode 235. 二叉搜索树的最近公共祖先
https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/

给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。

利用BST性质

时间复杂度：O(h) h为树的高度
空间复杂度：O(1)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(root, p, q):
    """
    二叉搜索树的最近公共祖先 - 利用BST性质
    
    Args:
        root: 二叉搜索树根节点
        p: 节点p
        q: 节点q
        
    Returns:
        最近公共祖先节点
    """
    while root:
        # 如果p和q都在左子树
        if p.val < root.val and q.val < root.val:
            root = root.left
        # 如果p和q都在右子树
        elif p.val > root.val and q.val > root.val:
            root = root.right
        # 否则当前节点就是最近公共祖先
        else:
            return root
    
    return None


def lowest_common_ancestor_recursive(root, p, q):
    """
    二叉搜索树的最近公共祖先 - 递归法
    
    Args:
        root: 二叉搜索树根节点
        p: 节点p
        q: 节点q
        
    Returns:
        最近公共祖先节点
    """
    if not root:
        return None
    
    # 如果p和q都在左子树
    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor_recursive(root.left, p, q)
    
    # 如果p和q都在右子树
    if p.val > root.val and q.val > root.val:
        return lowest_common_ancestor_recursive(root.right, p, q)
    
    # 否则当前节点就是最近公共祖先
    return root


def test_lowest_common_ancestor():
    """测试函数"""
    # 创建测试二叉搜索树: [6,2,8,0,4,7,9,null,null,3,5]
    #       6
    #      / \
    #     2   8
    #    / \ / \
    #   0  4 7  9
    #     / \
    #    3   5
    
    root = TreeNode(6)
    root.left = TreeNode(2)
    root.right = TreeNode(8)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    root.left.right.left = TreeNode(3)
    root.left.right.right = TreeNode(5)
    
    p = root.left      # 节点2
    q = root.right     # 节点8
    
    result1 = lowest_common_ancestor(root, p, q)
    print(f"节点2和节点8的最近公共祖先: {result1.val}")  # 期望: 6
    
    p2 = root.left.left      # 节点0
    q2 = root.left.right.right  # 节点5
    
    result2 = lowest_common_ancestor(root, p2, q2)
    print(f"节点0和节点5的最近公共祖先: {result2.val}")  # 期望: 2


if __name__ == "__main__":
    test_lowest_common_ancestor()

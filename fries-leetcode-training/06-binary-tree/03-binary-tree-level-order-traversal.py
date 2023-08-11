"""
LeetCode 102. 二叉树的层序遍历
https://leetcode.cn/problems/binary-tree-level-order-traversal/

给你二叉树的根节点root，返回其节点值的层序遍历。

BFS队列

时间复杂度：O(n)
空间复杂度：O(w) w为树的最大宽度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root):
    """
    二叉树的层序遍历 - BFS队列法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        层序遍历结果
    """
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.pop(0)
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


def test_level_order():
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
    
    result = level_order(root)
    print(f"层序遍历结果: {result}")
    # 期望: [[3], [9, 20], [15, 7]]


if __name__ == "__main__":
    test_level_order()

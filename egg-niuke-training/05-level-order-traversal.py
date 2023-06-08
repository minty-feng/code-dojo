"""
NC15 二叉树的层序遍历
https://www.nowcoder.com/practice/04a5560e43e24e9db4595865dc9c63a3

给定一个二叉树，返回该二叉树层序遍历的结果。

时间复杂度：O(n)
空间复杂度：O(n)
"""

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root):
    """
    层序遍历 - BFS
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_nodes)
    
    return result

# 测试
if __name__ == "__main__":
    # 创建二叉树
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
    
    result = level_order(root)
    print("层序遍历:")
    for level in result:
        print(level)


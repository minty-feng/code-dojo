"""
NC72 二叉树的最大深度
https://www.nowcoder.com/practice/8a2b2bf6c19b4f23a9bdb9b233eefa73

求给定二叉树的最大深度。

解法1：递归（DFS）
解法2：层序遍历（BFS）

时间复杂度：O(n)
空间复杂度：O(h) - 递归栈深度
"""

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth_recursive(root):
    """
    方法1：递归
    """
    if not root:
        return 0
    
    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)
    
    return max(left_depth, right_depth) + 1

def max_depth_bfs(root):
    """
    方法2：BFS层序遍历
    """
    if not root:
        return 0
    
    queue = deque([root])
    depth = 0
    
    while queue:
        level_size = len(queue)
        depth += 1
        
        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth

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
    
    print(f"递归法 - 最大深度: {max_depth_recursive(root)}")
    print(f"BFS法 - 最大深度: {max_depth_bfs(root)}")


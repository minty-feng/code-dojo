"""
NC14 二叉树的锯齿形层序遍历
https://www.nowcoder.com/practice/91b69814117f4e8097390d107d2efbe0

给定一个二叉树，返回该二叉树层序遍历的结果，从左往右，下一层从右往左，以此类推。

层序遍历 + 奇偶层判断

时间复杂度：O(n)
空间复杂度：O(n)
"""

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def zigzag_level_order(root):
    """
    二叉树的锯齿形层序遍历
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    level = 0
    
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
        
        # 奇数层反转
        if level % 2 == 1:
            level_nodes.reverse()
        
        result.append(level_nodes)
        level += 1
    
    return result

# 测试
if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    result = zigzag_level_order(root)
    print("锯齿形层序遍历:")
    for level in result:
        print(level)


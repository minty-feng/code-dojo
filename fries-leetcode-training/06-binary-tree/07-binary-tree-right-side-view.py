"""
LeetCode 199. 二叉树的右视图
https://leetcode.cn/problems/binary-tree-right-side-view/

给定一个二叉树的根节点root，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

BFS层序遍历

时间复杂度：O(n)
空间复杂度：O(w) w为树的最大宽度
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root):
    """
    二叉树的右视图 - BFS层序遍历法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        右视图节点值列表
    """
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.pop(0)
            
            # 如果是当前层的最后一个节点，加入结果
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result


def right_side_view_dfs(root):
    """
    二叉树的右视图 - DFS法
    
    Args:
        root: 二叉树根节点
        
    Returns:
        右视图节点值列表
    """
    result = []
    
    def dfs(node, depth):
        if not node:
            return
        
        # 如果当前深度还没有记录节点，说明这是该深度最右边的节点
        if depth == len(result):
            result.append(node.val)
        
        # 先访问右子树，再访问左子树
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)
    
    dfs(root, 0)
    return result


def test_right_side_view():
    """测试函数"""
    # 创建测试二叉树: [1,2,3,null,5,null,4]
    #     1
    #    / \
    #   2   3
    #    \   \
    #     5   4
    
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    
    result1 = right_side_view(root)
    print(f"BFS方法右视图: {result1}")  # 期望: [1, 3, 4]
    
    result2 = right_side_view_dfs(root)
    print(f"DFS方法右视图: {result2}")  # 期望: [1, 3, 4]


if __name__ == "__main__":
    test_right_side_view()

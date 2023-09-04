"""
NC6 二叉树中和为某一值的路径
https://www.nowcoder.com/practice/b736e784e3e34731af99065031301bca

输入一颗二叉树的根节点root和一个整数expectNumber，找出二叉树中结点值的和为expectNumber的所有路径。

DFS + 回溯

时间复杂度：O(n^2)
空间复杂度：O(n)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_path(root, target):
    """
    二叉树中和为某一值的路径
    """
    if not root:
        return []
    
    result = []
    path = []
    
    def dfs(node, remaining):
        if not node:
            return
        
        # 添加当前节点
        path.append(node.val)
        remaining -= node.val
        
        # 叶子节点且和为target
        if not node.left and not node.right and remaining == 0:
            result.append(path[:])
        
        # 递归左右子树
        dfs(node.left, remaining)
        dfs(node.right, remaining)
        
        # 回溯
        path.pop()
    
    dfs(root, target)
    return result

# 测试
if __name__ == "__main__":
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(12)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(7)
    
    target = 22
    result = find_path(root, target)
    
    print(f"和为{target}的路径:")
    for path in result:
        print(path)


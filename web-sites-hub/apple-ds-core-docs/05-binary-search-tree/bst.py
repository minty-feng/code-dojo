"""
二叉搜索树（BST）实现
"""

class TreeNode:
    """BST节点"""
    
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


class BST:
    """二叉搜索树"""
    
    def __init__(self):
        self.root = None
    
    # ========== 查找 ==========
    
    def search(self, val):
        """查找节点（迭代）"""
        curr = self.root
        while curr and curr.val != val:
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return curr
    
    def search_recursive(self, root, val):
        """查找节点（递归）"""
        if not root or root.val == val:
            return root
        if val < root.val:
            return self.search_recursive(root.left, val)
        return self.search_recursive(root.right, val)
    
    # ========== 插入 ==========
    
    def insert(self, val):
        """插入节点"""
        self.root = self._insert(self.root, val)
    
    def _insert(self, root, val):
        """插入辅助函数（递归）"""
        if not root:
            return TreeNode(val)
        
        if val < root.val:
            root.left = self._insert(root.left, val)
        elif val > root.val:
            root.right = self._insert(root.right, val)
        # val == root.val 则不插入（BST不存重复值）
        
        return root
    
    def insert_iterative(self, val):
        """插入节点（迭代）"""
        if not self.root:
            self.root = TreeNode(val)
            return
        
        curr = self.root
        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = TreeNode(val)
                    return
                curr = curr.left
            elif val > curr.val:
                if not curr.right:
                    curr.right = TreeNode(val)
                    return
                curr = curr.right
            else:
                return  # 已存在
    
    # ========== 删除 ==========
    
    def delete(self, val):
        """删除节点"""
        self.root = self._delete(self.root, val)
    
    def _delete(self, root, val):
        """删除辅助函数"""
        if not root:
            return None
        
        # 查找节点
        if val < root.val:
            root.left = self._delete(root.left, val)
        elif val > root.val:
            root.right = self._delete(root.right, val)
        else:
            # 找到要删除的节点
            
            # 情况1：没有子节点或只有一个子节点
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            
            # 情况2：有两个子节点
            # 用右子树的最小节点（后继）替换
            successor = self._find_min(root.right)
            root.val = successor.val
            root.right = self._delete(root.right, successor.val)
        
        return root
    
    # ========== 辅助方法 ==========
    
    def _find_min(self, root):
        """找最小节点"""
        while root.left:
            root = root.left
        return root
    
    def _find_max(self, root):
        """找最大节点"""
        while root.right:
            root = root.right
        return root
    
    def find_min(self):
        """找最小值"""
        if not self.root:
            return None
        return self._find_min(self.root).val
    
    def find_max(self):
        """找最大值"""
        if not self.root:
            return None
        return self._find_max(self.root).val
    
    # ========== 遍历 ==========
    
    def inorder(self):
        """中序遍历（有序输出）"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, root, result):
        if root:
            self._inorder(root.left, result)
            result.append(root.val)
            self._inorder(root.right, result)
    
    # ========== 验证 ==========
    
    def is_valid_bst(self):
        """验证是否为有效BST"""
        def validate(node, min_val, max_val):
            if not node:
                return True
            if not (min_val < node.val < max_val):
                return False
            return (validate(node.left, min_val, node.val) and
                    validate(node.right, node.val, max_val))
        
        return validate(self.root, float('-inf'), float('inf'))
    
    # ========== 打印 ==========
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        """打印树结构"""
        if node is None:
            node = self.root
        
        if node:
            print(" " * (level * 4) + prefix + str(node.val))
            if node.left or node.right:
                if node.left:
                    self.print_tree(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                
                if node.right:
                    self.print_tree(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


def demo():
    """演示BST操作"""
    print("=== 二叉搜索树演示 ===\n")
    
    bst = BST()
    
    # 插入节点
    values = [5, 3, 7, 2, 4, 6, 8]
    print(f"插入节点: {values}")
    for val in values:
        bst.insert(val)
    
    print("\n树结构:")
    bst.print_tree()
    
    # 遍历
    print(f"\n中序遍历（有序）: {bst.inorder()}")
    
    # 查找
    search_val = 4
    found = bst.search(search_val)
    print(f"\n查找 {search_val}: {'找到' if found else '未找到'}")
    
    # 最小最大值
    print(f"最小值: {bst.find_min()}")
    print(f"最大值: {bst.find_max()}")
    
    # 验证
    print(f"是否为有效BST: {bst.is_valid_bst()}")
    
    # 删除
    print(f"\n删除节点 3")
    bst.delete(3)
    print("树结构:")
    bst.print_tree()
    print(f"中序遍历: {bst.inorder()}")


if __name__ == '__main__':
    demo()


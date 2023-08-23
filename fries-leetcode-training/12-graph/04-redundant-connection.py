"""
LeetCode 684. 冗余连接
https://leetcode.cn/problems/redundant-connection/

树可以看成是一个连通且无环的无向图。
给定往一棵n个节点（节点值1～n）的树中添加一条边后的图。
添加的边的两个顶点包含在1到n中间，且这条附加的边不属于树中已存在的边。

并查集

时间复杂度：O(n)
空间复杂度：O(n)
"""

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        self.parent[px] = py
        return True


def find_redundant_connection(edges):
    """
    冗余连接 - 并查集法
    
    Args:
        edges: 边集合
        
    Returns:
        冗余的边
    """
    n = len(edges)
    uf = UnionFind(n + 1)
    
    for edge in edges:
        if not uf.union(edge[0], edge[1]):
            return edge
    
    return []


def test_find_redundant_connection():
    """测试函数"""
    # 测试用例1
    edges1 = [[1, 2], [1, 3], [2, 3]]
    result1 = find_redundant_connection(edges1)
    print(f"测试1: {result1}")  # 期望: [2, 3]
    
    # 测试用例2
    edges2 = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    result2 = find_redundant_connection(edges2)
    print(f"测试2: {result2}")  # 期望: [1, 4]


if __name__ == "__main__":
    test_find_redundant_connection()

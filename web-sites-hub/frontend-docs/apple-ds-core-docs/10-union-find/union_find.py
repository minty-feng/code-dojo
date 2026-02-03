"""
并查集实现
"""

class UnionFind:
    """并查集（路径压缩 + 按秩合并）"""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # 连通分量数
    
    def find(self, x):
        """查找根节点（路径压缩）"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """合并两个集合（按秩合并）"""
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        
        self.count -= 1
        return True
    
    def connected(self, x, y):
        """判断是否连通"""
        return self.find(x) == self.find(y)
    
    def get_count(self):
        """获取连通分量数"""
        return self.count


# ========== 应用示例 ==========

def num_islands(grid):
    """岛屿数量"""
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    uf = UnionFind(m * n)
    zeros = 0
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '0':
                zeros += 1
            else:
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == '1':
                        uf.union(i * n + j, ni * n + nj)
    
    return uf.get_count() - zeros


def find_circle_num(is_connected):
    """朋友圈数量"""
    n = len(is_connected)
    uf = UnionFind(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j] == 1:
                uf.union(i, j)
    
    return uf.get_count()


def find_redundant_connection(edges):
    """找冗余连接"""
    n = len(edges)
    uf = UnionFind(n + 1)
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    
    return []


def demo():
    """演示并查集"""
    print("=== 并查集演示 ===\n")
    
    uf = UnionFind(10)
    
    print(f"初始连通分量数: {uf.get_count()}")
    
    # 合并
    uf.union(1, 2)
    uf.union(2, 3)
    uf.union(4, 5)
    
    print(f"合并后连通分量数: {uf.get_count()}")
    print(f"1和3连通: {uf.connected(1, 3)}")
    print(f"1和4连通: {uf.connected(1, 4)}")
    
    uf.union(3, 4)
    print(f"\n合并3和4后")
    print(f"连通分量数: {uf.get_count()}")
    print(f"1和5连通: {uf.connected(1, 5)}")
    
    # 朋友圈问题
    print("\n=== 朋友圈问题 ===\n")
    is_connected = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ]
    print(f"朋友圈矩阵: {is_connected}")
    print(f"朋友圈数量: {find_circle_num(is_connected)}")


if __name__ == '__main__':
    demo()


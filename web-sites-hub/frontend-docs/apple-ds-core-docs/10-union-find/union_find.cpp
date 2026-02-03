/**
 * 并查集实现
 */

#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;
    int count;  // 连通分量数

public:
    UnionFind(int n) : parent(n), rank(n, 0), count(n) {
        iota(parent.begin(), parent.end(), 0);  // 初始化为0,1,2,...
    }
    
    // 查找根节点（路径压缩）
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    // 合并两个集合（按秩合并）
    bool unite(int x, int y) {
        int px = find(x);
        int py = find(y);
        
        if (px == py) {
            return false;
        }
        
        if (rank[px] < rank[py]) {
            parent[px] = py;
        } else if (rank[px] > rank[py]) {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px]++;
        }
        
        count--;
        return true;
    }
    
    // 判断是否连通
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
    
    // 获取连通分量数
    int getCount() const {
        return count;
    }
};

// 岛屿数量
int numIslands(vector<vector<char>>& grid) {
    if (grid.empty()) return 0;
    
    int m = grid.size();
    int n = grid[0].size();
    UnionFind uf(m * n);
    int zeros = 0;
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '0') {
                zeros++;
            } else {
                // 向右和向下连接
                if (j + 1 < n && grid[i][j+1] == '1') {
                    uf.unite(i * n + j, i * n + j + 1);
                }
                if (i + 1 < m && grid[i+1][j] == '1') {
                    uf.unite(i * n + j, (i + 1) * n + j);
                }
            }
        }
    }
    
    return uf.getCount() - zeros;
}

// 朋友圈数量
int findCircleNum(const vector<vector<int>>& isConnected) {
    int n = isConnected.size();
    UnionFind uf(n);
    
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (isConnected[i][j] == 1) {
                uf.unite(i, j);
            }
        }
    }
    
    return uf.getCount();
}

// 冗余连接
vector<int> findRedundantConnection(const vector<vector<int>>& edges) {
    int n = edges.size();
    UnionFind uf(n + 1);
    
    for (const auto& edge : edges) {
        if (!uf.unite(edge[0], edge[1])) {
            return edge;
        }
    }
    
    return {};
}

int main() {
    cout << "=== 并查集演示 ===" << endl << endl;
    
    UnionFind uf(10);
    
    cout << "初始连通分量数: " << uf.getCount() << endl;
    
    uf.unite(1, 2);
    uf.unite(2, 3);
    uf.unite(4, 5);
    
    cout << "合并后连通分量数: " << uf.getCount() << endl;
    cout << "1和3连通: " << (uf.connected(1, 3) ? "是" : "否") << endl;
    cout << "1和4连通: " << (uf.connected(1, 4) ? "是" : "否") << endl;
    
    uf.unite(3, 4);
    cout << "\n合并3和4后" << endl;
    cout << "连通分量数: " << uf.getCount() << endl;
    cout << "1和5连通: " << (uf.connected(1, 5) ? "是" : "否") << endl << endl;
    
    // 朋友圈
    cout << "朋友圈问题:" << endl;
    vector<vector<int>> isConnected = {
        {1, 1, 0},
        {1, 1, 0},
        {0, 0, 1}
    };
    cout << "  朋友圈数量: " << findCircleNum(isConnected) << endl;
    
    return 0;
}


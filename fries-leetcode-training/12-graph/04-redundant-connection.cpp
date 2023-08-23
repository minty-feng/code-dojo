/**
 * LeetCode 684. 冗余连接
 * https://leetcode.cn/problems/redundant-connection/
 * 
 * 树可以看成是一个连通且无环的无向图。
 * 给定往一棵n个节点（节点值1～n）的树中添加一条边后的图。
 * 添加的边的两个顶点包含在1到n中间，且这条附加的边不属于树中已存在的边。
 * 
 * 并查集
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;
    
public:
    UnionFind(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    bool union_nodes(int x, int y) {
        int px = find(x);
        int py = find(y);
        
        if (px == py) {
            return false;  // 已经连通，形成环
        }
        
        if (rank[px] < rank[py]) {
            parent[px] = py;
        } else if (rank[px] > rank[py]) {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px]++;
        }
        
        return true;
    }
};

class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        UnionFind uf(n + 1);  // 节点编号从1开始
        
        for (const auto& edge : edges) {
            int u = edge[0];
            int v = edge[1];
            
            if (!uf.union_nodes(u, v)) {
                return edge;  // 找到冗余连接
            }
        }
        
        return {};  // 没有冗余连接
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testFindRedundantConnection() {
    Solution solution;
    
    vector<vector<int>> edges1 = {{1, 2}, {1, 3}, {2, 3}};
    vector<int> result1 = solution.findRedundantConnection(edges1);
    cout << "测试1 {{1,2},{1,3},{2,3}}: [" << result1[0] << "," << result1[1] << "]" << endl;  // 期望: [2,3]
    
    vector<vector<int>> edges2 = {{1, 2}, {2, 3}, {3, 4}, {1, 4}, {1, 5}};
    vector<int> result2 = solution.findRedundantConnection(edges2);
    cout << "测试2 {{1,2},{2,3},{3,4},{1,4},{1,5}}: [" << result2[0] << "," << result2[1] << "]" << endl;  // 期望: [1,4]
}

int main() {
    testFindRedundantConnection();
    return 0;
}

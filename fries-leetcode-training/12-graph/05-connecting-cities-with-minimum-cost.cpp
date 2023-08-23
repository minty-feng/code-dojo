/**
 * LeetCode 1135. 连接所有城市的最小成本
 * https://leetcode.cn/problems/connecting-cities-with-minimum-cost/
 * 
 * 想象一下你是个城市基建工程师，城市中有N个城市，编号从1到N。
 * 给你一些可选的连接，其中每个连接connect[i] = [city1, city2, cost]表示将city1和city2连接的成本为cost。
 * 
 * 最小生成树（Kruskal算法）
 * 
 * 时间复杂度：O(E log E)
 * 空间复杂度：O(V)
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
        
        return true;
    }
};

class Solution {
public:
    int minimumCost(int n, vector<vector<int>>& connections) {
        if (n <= 1) {
            return 0;
        }
        
        // 按成本排序
        sort(connections.begin(), connections.end(), 
             [](const vector<int>& a, const vector<int>& b) {
                 return a[2] < b[2];
             });
        
        UnionFind uf(n);
        int totalCost = 0;
        int edgesUsed = 0;
        
        for (const auto& connection : connections) {
            int city1 = connection[0] - 1;  // 转换为0-based索引
            int city2 = connection[1] - 1;
            int cost = connection[2];
            
            if (uf.union_nodes(city1, city2)) {
                totalCost += cost;
                edgesUsed++;
                
                if (edgesUsed == n - 1) {
                    break;
                }
            }
        }
        
        return edgesUsed == n - 1 ? totalCost : -1;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMinimumCost() {
    Solution solution;
    
    int n1 = 3;
    vector<vector<int>> connections1 = {{1, 2, 5}, {1, 3, 6}, {2, 3, 1}};
    int result1 = solution.minimumCost(n1, connections1);
    cout << "测试1 n=" << n1 << ", connections={{1,2,5},{1,3,6},{2,3,1}}: " << result1 << endl;  // 期望: 6
    
    int n2 = 4;
    vector<vector<int>> connections2 = {{1, 2, 3}, {3, 4, 4}};
    int result2 = solution.minimumCost(n2, connections2);
    cout << "测试2 n=" << n2 << ", connections={{1,2,3},{3,4,4}}: " << result2 << endl;  // 期望: -1
}

int main() {
    testMinimumCost();
    return 0;
}

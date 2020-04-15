/**
 * DFS和BFS实现
 */

#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_set>
#include <unordered_map>

using namespace std;

// DFS递归
void dfsRecursive(const unordered_map<int, vector<int>>& graph, 
                  int node, unordered_set<int>& visited) {
    visited.insert(node);
    cout << node << " ";
    
    if (graph.count(node)) {
        for (int neighbor : graph.at(node)) {
            if (!visited.count(neighbor)) {
                dfsRecursive(graph, neighbor, visited);
            }
        }
    }
}

// DFS迭代（栈）
vector<int> dfsIterative(const unordered_map<int, vector<int>>& graph, int start) {
    unordered_set<int> visited;
    stack<int> st;
    vector<int> result;
    
    st.push(start);
    
    while (!st.empty()) {
        int node = st.top();
        st.pop();
        
        if (!visited.count(node)) {
            visited.insert(node);
            result.push_back(node);
            
            if (graph.count(node)) {
                auto neighbors = graph.at(node);
                for (auto it = neighbors.rbegin(); it != neighbors.rend(); ++it) {
                    if (!visited.count(*it)) {
                        st.push(*it);
                    }
                }
            }
        }
    }
    
    return result;
}

// BFS（队列）
vector<int> bfs(const unordered_map<int, vector<int>>& graph, int start) {
    unordered_set<int> visited;
    queue<int> q;
    vector<int> result;
    
    visited.insert(start);
    q.push(start);
    
    while (!q.empty()) {
        int node = q.front();
        q.pop();
        result.push_back(node);
        
        if (graph.count(node)) {
            for (int neighbor : graph.at(node)) {
                if (!visited.count(neighbor)) {
                    visited.insert(neighbor);
                    q.push(neighbor);
                }
            }
        }
    }
    
    return result;
}

// 岛屿数量
void dfsIsland(vector<vector<char>>& grid, int i, int j) {
    int m = grid.size();
    int n = grid[0].size();
    
    if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == '0') {
        return;
    }
    
    grid[i][j] = '0';
    
    dfsIsland(grid, i + 1, j);
    dfsIsland(grid, i - 1, j);
    dfsIsland(grid, i, j + 1);
    dfsIsland(grid, i, j - 1);
}

int numIslands(vector<vector<char>>& grid) {
    if (grid.empty()) return 0;
    
    int count = 0;
    int m = grid.size();
    int n = grid[0].size();
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '1') {
                count++;
                dfsIsland(grid, i, j);
            }
        }
    }
    
    return count;
}

int main() {
    cout << "=== DFS和BFS演示 ===" << endl << endl;
    
    // 构建图
    unordered_map<int, vector<int>> graph;
    graph[0] = {1, 2};
    graph[1] = {0, 3, 4};
    graph[2] = {0, 5};
    graph[3] = {1};
    graph[4] = {1, 5};
    graph[5] = {2, 4};
    
    cout << "图结构:" << endl;
    for (const auto& pair : graph) {
        cout << "  " << pair.first << ": [";
        for (size_t i = 0; i < pair.second.size(); i++) {
            cout << pair.second[i];
            if (i < pair.second.size() - 1) cout << ", ";
        }
        cout << "]" << endl;
    }
    cout << endl;
    
    // DFS
    cout << "DFS遍历（递归）: ";
    unordered_set<int> visited;
    dfsRecursive(graph, 0, visited);
    cout << endl << endl;
    
    cout << "DFS遍历（迭代）: ";
    vector<int> dfs_result = dfsIterative(graph, 0);
    for (int node : dfs_result) {
        cout << node << " ";
    }
    cout << endl << endl;
    
    // BFS
    cout << "BFS遍历: ";
    vector<int> bfs_result = bfs(graph, 0);
    for (int node : bfs_result) {
        cout << node << " ";
    }
    cout << endl << endl;
    
    // 岛屿数量
    cout << "岛屿数量:" << endl;
    vector<vector<char>> grid = {
        {'1', '1', '0', '0', '0'},
        {'1', '1', '0', '0', '0'},
        {'0', '0', '1', '0', '0'},
        {'0', '0', '0', '1', '1'}
    };
    
    for (const auto& row : grid) {
        cout << "  ";
        for (char cell : row) {
            cout << cell << " ";
        }
        cout << endl;
    }
    cout << "岛屿数量: " << numIslands(grid) << endl;
    
    return 0;
}


/**
 * 图的实现和基本算法
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <climits>

using namespace std;

class Graph {
private:
    unordered_map<int, vector<pair<int, int>>> graph;  // node -> [(neighbor, weight)]
    bool directed;

public:
    Graph(bool dir = false) : directed(dir) {}
    
    void addEdge(int u, int v, int weight = 1) {
        graph[u].push_back({v, weight});
        if (!directed) {
            graph[v].push_back({u, weight});
        }
    }
    
    // DFS递归
    void dfsHelper(int node, unordered_set<int>& visited, vector<int>& result) {
        visited.insert(node);
        result.push_back(node);
        
        for (auto& [neighbor, weight] : graph[node]) {
            if (!visited.count(neighbor)) {
                dfsHelper(neighbor, visited, result);
            }
        }
    }
    
    vector<int> dfs(int start) {
        unordered_set<int> visited;
        vector<int> result;
        dfsHelper(start, visited, result);
        return result;
    }
    
    // BFS
    vector<int> bfs(int start) {
        unordered_set<int> visited;
        queue<int> q;
        vector<int> result;
        
        visited.insert(start);
        q.push(start);
        
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            result.push_back(node);
            
            for (auto& [neighbor, weight] : graph[node]) {
                if (!visited.count(neighbor)) {
                    visited.insert(neighbor);
                    q.push(neighbor);
                }
            }
        }
        
        return result;
    }
    
    // 检测环（有向图）
    bool hasCycleHelper(int node, unordered_set<int>& visited, 
                       unordered_set<int>& recStack) {
        visited.insert(node);
        recStack.insert(node);
        
        for (auto& [neighbor, weight] : graph[node]) {
            if (!visited.count(neighbor)) {
                if (hasCycleHelper(neighbor, visited, recStack)) {
                    return true;
                }
            } else if (recStack.count(neighbor)) {
                return true;
            }
        }
        
        recStack.erase(node);
        return false;
    }
    
    bool hasCycle() {
        unordered_set<int> visited;
        unordered_set<int> recStack;
        
        for (auto& [node, edges] : graph) {
            if (!visited.count(node)) {
                if (hasCycleHelper(node, visited, recStack)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    // 拓扑排序（Kahn算法）
    vector<int> topologicalSort() {
        unordered_map<int, int> inDegree;
        
        for (auto& [node, edges] : graph) {
            if (!inDegree.count(node)) {
                inDegree[node] = 0;
            }
            for (auto& [neighbor, weight] : edges) {
                inDegree[neighbor]++;
            }
        }
        
        queue<int> q;
        for (auto& [node, degree] : inDegree) {
            if (degree == 0) {
                q.push(node);
            }
        }
        
        vector<int> result;
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            result.push_back(node);
            
            for (auto& [neighbor, weight] : graph[node]) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }
        
        return result.size() == inDegree.size() ? result : vector<int>();
    }
};

// Dijkstra最短路径
unordered_map<int, int> dijkstra(
    const unordered_map<int, vector<pair<int, int>>>& graph, 
    int start) {
    
    unordered_map<int, int> distances;
    for (auto& [node, edges] : graph) {
        distances[node] = INT_MAX;
    }
    distances[start] = 0;
    
    // 优先队列：(distance, node)
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [currDist, currNode] = pq.top();
        pq.pop();
        
        if (currDist > distances[currNode]) {
            continue;
        }
        
        if (graph.count(currNode)) {
            for (auto& [neighbor, weight] : graph.at(currNode)) {
                int distance = currDist + weight;
                if (distance < distances[neighbor]) {
                    distances[neighbor] = distance;
                    pq.push({distance, neighbor});
                }
            }
        }
    }
    
    return distances;
}

int main() {
    cout << "=== 图算法演示 ===" << endl << endl;
    
    // 创建无向图
    Graph g(false);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 3);
    
    cout << "DFS遍历: ";
    vector<int> dfs_result = g.dfs(0);
    for (int node : dfs_result) {
        cout << node << " ";
    }
    cout << endl;
    
    cout << "BFS遍历: ";
    vector<int> bfs_result = g.bfs(0);
    for (int node : bfs_result) {
        cout << node << " ";
    }
    cout << endl << endl;
    
    // 拓扑排序
    cout << "拓扑排序:" << endl;
    Graph dag(true);
    dag.addEdge(5, 2);
    dag.addEdge(5, 0);
    dag.addEdge(4, 0);
    dag.addEdge(4, 1);
    dag.addEdge(2, 3);
    dag.addEdge(3, 1);
    
    vector<int> topo = dag.topologicalSort();
    cout << "  ";
    for (int node : topo) {
        cout << node << " ";
    }
    cout << endl << endl;
    
    // Dijkstra
    cout << "Dijkstra最短路径:" << endl;
    unordered_map<int, vector<pair<int, int>>> weighted_graph;
    weighted_graph[0] = {{1, 4}, {2, 2}};
    weighted_graph[1] = {{2, 1}, {3, 5}};
    weighted_graph[2] = {{3, 3}};
    weighted_graph[3] = {};
    
    auto distances = dijkstra(weighted_graph, 0);
    for (auto& [node, dist] : distances) {
        cout << "  到节点" << node << "的距离: " << dist << endl;
    }
    
    return 0;
}


/**
 * NC109 岛屿数量
 * https://www.nowcoder.com/practice/0c9664d1554e466aa107d899418e8145
 * 
 * 给一个01矩阵，1代表是陆地，0代表海洋。
 * 相邻的1属于同一个岛屿，求岛屿数量。
 * 
 * 时间复杂度：O(n*m)
 * 空间复杂度：O(n*m)
 */

#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    /**
     * 方法1：DFS
     */
    int numIslands_DFS(vector<vector<char>>& grid) {
        if (grid.empty() || grid[0].empty()) {
            return 0;
        }
        
        int m = grid.size(), n = grid[0].size();
        int count = 0;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        
        return count;
    }
    
    /**
     * 方法2：BFS
     */
    int numIslands_BFS(vector<vector<char>>& grid) {
        if (grid.empty() || grid[0].empty()) {
            return 0;
        }
        
        int m = grid.size(), n = grid[0].size();
        int count = 0;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    bfs(grid, i, j);
                }
            }
        }
        
        return count;
    }

private:
    void dfs(vector<vector<char>>& grid, int i, int j) {
        int m = grid.size(), n = grid[0].size();
        
        // 边界检查
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == '0') {
            return;
        }
        
        // 标记已访问
        grid[i][j] = '0';
        
        // 四个方向搜索
        dfs(grid, i + 1, j);
        dfs(grid, i - 1, j);
        dfs(grid, i, j + 1);
        dfs(grid, i, j - 1);
    }
    
    void bfs(vector<vector<char>>& grid, int i, int j) {
        int m = grid.size(), n = grid[0].size();
        queue<pair<int, int>> q;
        
        q.push({i, j});
        grid[i][j] = '0';
        
        int dirs[4][2] = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        
        while (!q.empty()) {
            auto [x, y] = q.front();
            q.pop();
            
            for (int d = 0; d < 4; d++) {
                int nx = x + dirs[d][0];
                int ny = y + dirs[d][1];
                
                if (nx >= 0 && nx < m && ny >= 0 && ny < n && grid[nx][ny] == '1') {
                    grid[nx][ny] = '0';
                    q.push({nx, ny});
                }
            }
        }
    }
};

int main() {
    Solution solution;
    
    vector<vector<char>> grid = {
        {'1', '1', '0', '0', '0'},
        {'0', '1', '0', '1', '1'},
        {'0', '0', '0', '1', '1'},
        {'0', '0', '0', '0', '0'},
        {'0', '0', '1', '1', '1'}
    };
    
    int count = solution.numIslands_DFS(grid);
    cout << "岛屿数量: " << count << endl;
    
    return 0;
}


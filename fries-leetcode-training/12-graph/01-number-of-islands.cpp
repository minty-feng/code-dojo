/**
 * LeetCode 200. 岛屿数量
 * https://leetcode.cn/problems/number-of-islands/
 * 
 * 给你一个由'1'（陆地）和'0'（水）组成的二维网格，请你计算网格中岛屿的数量。
 * 
 * DFS/BFS
 * 
 * 时间复杂度：O(m*n)
 * 空间复杂度：O(m*n)
 */

class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty() || grid[0].empty()) {
            return 0;
        }
        
        int rows = grid.size();
        int cols = grid[0].size();
        int count = 0;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    dfs(grid, i, j);
                    count++;
                }
            }
        }
        
        return count;
    }
    
private:
    void dfs(vector<vector<char>>& grid, int i, int j) {
        if (i < 0 || i >= grid.size() || j < 0 || j >= grid[0].size() || grid[i][j] != '1') {
            return;
        }
        
        grid[i][j] = '0';  // 标记为已访问
        
        // 四个方向DFS
        dfs(grid, i + 1, j);
        dfs(grid, i - 1, j);
        dfs(grid, i, j + 1);
        dfs(grid, i, j - 1);
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testNumIslands() {
    Solution solution;
    
    vector<vector<char>> grid1 = {
        {'1','1','1','1','0'},
        {'1','1','0','1','0'},
        {'1','1','0','0','0'},
        {'0','0','0','0','0'}
    };
    int result1 = solution.numIslands(grid1);
    cout << "测试1: " << result1 << endl;  // 期望: 1
    
    vector<vector<char>> grid2 = {
        {'1','1','0','0','0'},
        {'1','1','0','0','0'},
        {'0','0','1','0','0'},
        {'0','0','0','1','1'}
    };
    int result2 = solution.numIslands(grid2);
    cout << "测试2: " << result2 << endl;  // 期望: 3
}

int main() {
    testNumIslands();
    return 0;
}

"""
LeetCode 210. 课程表II
https://leetcode.cn/problems/course-schedule-ii/

现在你总共有numCourses门课需要选，记为0到numCourses-1。
给你一个数组prerequisites，其中prerequisites[i] = [ai, bi]，
表示在选修课程ai前必须先选修bi。

拓扑排序

时间复杂度：O(V + E)
空间复杂度：O(V + E)
"""

def find_order(num_courses, prerequisites):
    """
    课程表II - 拓扑排序法
    
    Args:
        num_courses: 课程总数
        prerequisites: 先修课程关系
        
    Returns:
        完成所有课程的顺序，如果无法完成则返回空列表
    """
    # 构建邻接表和入度数组
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    # 找到所有入度为0的课程
    queue = []
    for i in range(num_courses):
        if indegree[i] == 0:
            queue.append(i)
    
    result = []
    
    while queue:
        course = queue.pop(0)
        result.append(course)
        
        # 处理该课程的所有后续课程
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return result if len(result) == num_courses else []


def test_find_order():
    """测试函数"""
    # 测试用例1
    num_courses1 = 2
    prerequisites1 = [[1, 0]]
    result1 = find_order(num_courses1, prerequisites1)
    print(f"测试1 numCourses=2, prerequisites=[[1,0]]: {result1}")  # 期望: [0,1]
    
    # 测试用例2
    num_courses2 = 4
    prerequisites2 = [[1, 0], [2, 0], [3, 1], [3, 2]]
    result2 = find_order(num_courses2, prerequisites2)
    print(f"测试2 numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]: {result2}")  # 期望: [0,1,2,3]或[0,2,1,3]
    
    # 测试用例3
    num_courses3 = 1
    prerequisites3 = []
    result3 = find_order(num_courses3, prerequisites3)
    print(f"测试3 numCourses=1, prerequisites=[]: {result3}")  # 期望: [0]


if __name__ == "__main__":
    test_find_order()

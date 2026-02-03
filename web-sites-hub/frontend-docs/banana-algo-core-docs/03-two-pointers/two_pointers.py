"""
双指针技巧实现
"""

# ========== 对撞指针 ==========

def two_sum_sorted(nums, target):
    """有序数组两数之和"""
    left, right = 0, len(nums) - 1
    
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1
    
    return []


def three_sum(nums):
    """三数之和为0"""
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # 去重
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # 去重
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result


def container_with_most_water(height):
    """盛最多水的容器"""
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        area = width * min(height[left], height[right])
        max_area = max(max_area, area)
        
        # 移动较短的那边
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


# ========== 快慢指针 ==========

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head):
    """检测链表环"""
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False


def detect_cycle(head):
    """找环的起始节点"""
    slow = fast = head
    
    # 找相遇点
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None
    
    # 找起始点
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow


def find_middle(head):
    """找链表中点"""
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


# ========== 滑动窗口 ==========

def length_of_longest_substring(s):
    """最长无重复字符子串"""
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len


def min_window(s, t):
    """最小覆盖子串"""
    from collections import Counter
    
    need = Counter(t)
    window = {}
    left = 0
    valid = 0
    start, length = 0, float('inf')
    
    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1
        
        if c in need and window[c] == need[c]:
            valid += 1
        
        while valid == len(need):
            if right - left + 1 < length:
                start = left
                length = right - left + 1
            
            d = s[left]
            left += 1
            if d in need and window[d] == need[d]:
                valid -= 1
            window[d] -= 1
    
    return s[start:start + length] if length != float('inf') else ""


def find_anagrams(s, p):
    """找所有字母异位词"""
    from collections import Counter
    
    need = Counter(p)
    window = {}
    left = 0
    valid = 0
    result = []
    
    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1
        
        if c in need and window[c] == need[c]:
            valid += 1
        
        while right - left + 1 >= len(p):
            if valid == len(need):
                result.append(left)
            
            d = s[left]
            left += 1
            if d in need and window[d] == need[d]:
                valid -= 1
            window[d] -= 1
    
    return result


def demo():
    """演示双指针"""
    print("=== 双指针技巧演示 ===\n")
    
    # 两数之和
    nums = [2, 7, 11, 15]
    target = 9
    print(f"两数之和 {nums}, target={target}:")
    print(f"  结果: {two_sum_sorted(nums, target)}\n")
    
    # 三数之和
    nums = [-1, 0, 1, 2, -1, -4]
    print(f"三数之和 {nums}:")
    print(f"  结果: {three_sum(nums)}\n")
    
    # 盛水
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"盛最多水 {height}:")
    print(f"  最大面积: {container_with_most_water(height)}\n")
    
    # 最长无重复子串
    s = "abcabcbb"
    print(f"最长无重复子串 '{s}':")
    print(f"  长度: {length_of_longest_substring(s)}\n")
    
    # 字母异位词
    s, p = "cbaebabacd", "abc"
    print(f"找字母异位词 s='{s}', p='{p}':")
    print(f"  起始索引: {find_anagrams(s, p)}")


if __name__ == '__main__':
    demo()


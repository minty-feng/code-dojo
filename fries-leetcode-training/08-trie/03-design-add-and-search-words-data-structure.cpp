/**
 * LeetCode 211. 添加与搜索单词
 * https://leetcode.cn/problems/design-add-and-search-words-data-structure/
 * 
 * 请你设计一个数据结构，支持添加新单词和查找字符串是否与任何先前添加的字符串匹配。
 * 
 * Trie + 通配符处理
 * 
 * 时间复杂度：O(m) 添加，O(m) 搜索（m为字符串长度）
 * 空间复杂度：O(ALPHABET_SIZE * N * M) N为键的数量，M为键的长度
 */

struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool is_end;
    
    TrieNode() : is_end(false) {}
};

class WordDictionary {
private:
    TrieNode* root;
    
public:
    WordDictionary() {
        root = new TrieNode();
    }
    
    void addWord(string word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->is_end = true;
    }
    
    bool search(string word) {
        return dfs(root, word, 0);
    }
    
private:
    bool dfs(TrieNode* node, const string& word, int index) {
        if (index == word.length()) {
            return node->is_end;
        }
        
        char c = word[index];
        
        if (c == '.') {
            // 通配符，尝试所有子节点
            for (auto& pair : node->children) {
                if (dfs(pair.second, word, index + 1)) {
                    return true;
                }
            }
            return false;
        } else {
            // 普通字符
            if (node->children.find(c) == node->children.end()) {
                return false;
            }
            return dfs(node->children[c], word, index + 1);
        }
    }
};

// 测试函数
#include <iostream>
#include <unordered_map>
using namespace std;

void testWordDictionary() {
    WordDictionary wordDict;
    
    // 添加单词
    wordDict.addWord("bad");
    wordDict.addWord("dad");
    wordDict.addWord("mad");
    
    // 测试搜索
    cout << "搜索 'pad': " << (wordDict.search("pad") ? "True" : "False") << endl;    // 期望: False
    cout << "搜索 'bad': " << (wordDict.search("bad") ? "True" : "False") << endl;    // 期望: True
    cout << "搜索 '.ad': " << (wordDict.search(".ad") ? "True" : "False") << endl;    // 期望: True
    cout << "搜索 'b..': " << (wordDict.search("b..") ? "True" : "False") << endl;   // 期望: True
    cout << "搜索 'b.x': " << (wordDict.search("b.x") ? "True" : "False") << endl;    // 期望: False
}

int main() {
    testWordDictionary();
    return 0;
}

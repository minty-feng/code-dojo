/**
 * 字典树（Trie）实现
 */

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool isEnd;
    
    TrieNode() : isEnd(false) {}
};

class Trie {
private:
    TrieNode* root;
    
    void deleteTree(TrieNode* node) {
        if (node) {
            for (auto& [ch, child] : node->children) {
                deleteTree(child);
            }
            delete node;
        }
    }
    
    void dfsCollect(TrieNode* node, const string& path, vector<string>& result) {
        if (node->isEnd) {
            result.push_back(path);
        }
        
        for (auto& [ch, child] : node->children) {
            dfsCollect(child, path + ch, result);
        }
    }

public:
    Trie() {
        root = new TrieNode();
    }
    
    ~Trie() {
        deleteTree(root);
    }
    
    // 插入单词
    void insert(const string& word) {
        TrieNode* node = root;
        for (char ch : word) {
            if (!node->children.count(ch)) {
                node->children[ch] = new TrieNode();
            }
            node = node->children[ch];
        }
        node->isEnd = true;
    }
    
    // 查找完整单词
    bool search(const string& word) {
        TrieNode* node = root;
        for (char ch : word) {
            if (!node->children.count(ch)) {
                return false;
            }
            node = node->children[ch];
        }
        return node->isEnd;
    }
    
    // 查找前缀
    bool startsWith(const string& prefix) {
        TrieNode* node = root;
        for (char ch : prefix) {
            if (!node->children.count(ch)) {
                return false;
            }
            node = node->children[ch];
        }
        return true;
    }
    
    // 获取所有以prefix开头的单词
    vector<string> getAllWordsWithPrefix(const string& prefix) {
        TrieNode* node = root;
        for (char ch : prefix) {
            if (!node->children.count(ch)) {
                return {};
            }
            node = node->children[ch];
        }
        
        vector<string> result;
        dfsCollect(node, prefix, result);
        return result;
    }
};

int main() {
    cout << "=== 字典树演示 ===" << endl << endl;
    
    Trie trie;
    
    // 插入单词
    vector<string> words = {"cat", "car", "card", "care", "dog", "dodge"};
    cout << "插入单词: ";
    for (const auto& word : words) {
        cout << word << " ";
        trie.insert(word);
    }
    cout << endl << endl;
    
    // 查找
    cout << "查找:" << endl;
    vector<string> testWords = {"cat", "can", "car", "card"};
    for (const auto& word : testWords) {
        bool found = trie.search(word);
        cout << "  " << word << ": " << (found ? "✅找到" : "❌未找到") << endl;
    }
    cout << endl;
    
    // 前缀查找
    cout << "前缀查找:" << endl;
    vector<string> prefixes = {"ca", "do", "da"};
    for (const auto& prefix : prefixes) {
        bool found = trie.startsWith(prefix);
        cout << "  " << prefix << ": " << (found ? "✅存在" : "❌不存在") << endl;
    }
    cout << endl;
    
    // 自动补全
    string prefix = "car";
    cout << "自动补全:" << endl;
    vector<string> completions = trie.getAllWordsWithPrefix(prefix);
    cout << "  以'" << prefix << "'开头的单词: ";
    for (const auto& word : completions) {
        cout << word << " ";
    }
    cout << endl;
    
    return 0;
}




#include <iostream>
#include <fstream>
#include <unordered_map>

class trieNode {
public:
    std::unordered_map<char, trieNode*> children;
    bool is_end_of_word;

    trieNode() : is_end_of_word(false) {}
};

class trie {
private:
    trieNode* root;

public:
    trie() {
        root = new trieNode();
    }

    void insert(const std::string& word) {
        trieNode* current = root;
        for (char ch : word) {
            if (current->children.find(ch) == current->children.end()) {
                current->children[ch] = new trieNode();
            }
            current = current->children[ch];
        }
        current->is_end_of_word = true;
    }

    bool search(const std::string& word) {
        trieNode* current = root;
        for (char ch : word) {
            // each character in the word given in main
            if (current->children.find(ch) == current->children.end()) {
                // not found
                return false; 
            }
            current = current->children[ch];
        }
        return current != nullptr && current->is_end_of_word;
    }

    void buildtrieFromBadWordsFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "please download make for windows using chocolatey and then try the command 'make'\n";
            return;
        }
        
        std::string word;
        while (file >> word) {
            insert(word);
        }
        file.close();
    }
    int main(const std::string& filename)
    {
        trie trie;
        trie.buildtrieFromBadWordsFile(filename);

        std::string testWord = "fuck";
        if (trie.search(testWord))
        {
            std::cout << testWord << " IS A NONO WORD!!!!\n";
        }
        else
        {
            std::cout << testWord << " is a good word :).\n";
        }

        std::string test_word_2 = "goodytwoshoes";
        if (trie.search(test_word_2))
        {
            std::cout << test_word_2 << " IS A NONO WORD!!!!\n";
        }
        else
        {
            std::cout << test_word_2 << " is a good word :)\n";
        }

        return 0;
    }
};


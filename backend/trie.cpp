#include <algorithm>
#include <cctype>
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <string>
#include <sstream>

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

    bool search(const std::string &message)
    {
        std::istringstream iss(message);
        std::string word;

        while (iss >> word)
        {
            std::transform(word.begin(), word.end(), word.begin(),
                           [](unsigned char c)
                           { return std::tolower(c); });

            // Remove special characters like newline characters
            word.erase(std::remove_if(word.begin(), word.end(), [](char c)
                                      { return !std::isalnum(c); }),
                       word.end());

            if (!word.empty())
            {
                if (searchWord(word))
                {
                    return true; // Found a bad word
                }
            }
        }

        return false; // No bad words found in the entire message
    }

    bool searchWord(const std::string &word)
    {
        trieNode *current = root;
        for (char ch : word)
        {
            if (current->children.find(ch) == current->children.end())
            {
                return false; // Not found
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
        while (std::getline(file, word))
        {
            if (word.empty())
                continue;

            insert(word);
        }
        file.close();
    }
};

// int main()
// {
//     trie trie;
//     trie.buildtrieFromBadWordsFile("../bad-words.txt");

//     std::string testWord = "fuck";
//     if (trie.search(testWord))
//     {
//         std::cout << testWord << " IS A NONO WORD!!!!\n";
//     }
//     else
//     {
//         std::cout << testWord << " is a good word :).\n";
//     }

//     std::string test_word_2 = "goodytwoshoes";
//     if (trie.search(test_word_2))
//     {
//         std::cout << test_word_2 << " IS A NONO WORD!!!!\n";
//     }
//     else
//     {
//         std::cout << test_word_2 << " is a good word :)\n";
//     }

//     test_word_2 = "FUCK lol";
//     if (trie.search(test_word_2))
//     {
//         std::cout << test_word_2 << " IS A NONO WORD!!!!\n";
//     }
//     else
//     {
//         std::cout << test_word_2 << " is a good word :)\n";
//     }

//     return 0;
// }

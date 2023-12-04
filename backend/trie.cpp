#include <algorithm>
#include <cctype>
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <string>
#include <sstream>

class trieNode
{
public:
    std::unordered_map<char, trieNode *> children;
    bool is_end_of_phrase;

    trieNode() : is_end_of_phrase(false) {}
};

class trie
{
private:
    trieNode *root;

public:
    trie()
    {
        root = new trieNode();
    }

    void insert(const std::string &phrase)
    {
        trieNode *current = root;
        // make a new trieNode for each character in the phrase
        for (char ch : phrase)
        {
            if (current->children.find(ch) == current->children.end())
            {
                current->children[ch] = new trieNode();
            }
            current = current->children[ch];
        }
        current->is_end_of_phrase = true;
    }

    bool search(const std::string &message)
    {
        // transform the message into lowercase,
        // because the bad words are all in lowercase.
        std::string lowercase_msg = message;
        std::transform(lowercase_msg.begin(), lowercase_msg.end(), lowercase_msg.begin(),
                       [](unsigned char c)
                       { return std::tolower(c); });

        // create a trieNode for each character.
        for (int i = 0; i < lowercase_msg.length(); ++i)
        {
            trieNode *current = root;
            // iterate from the current position to find any words with
            // spaces
            for (int j = i; j < lowercase_msg.length(); ++j)
            {
                char ch = lowercase_msg[j];
                if (current->children.find(ch) == current->children.end())
                {
                    break;
                }
                current = current->children[ch];
                // this accounts for words such as "class" (because ass is bad)
                if (current->is_end_of_phrase &&
                    (j + 1 == lowercase_msg.length() || !isalpha(lowercase_msg[j + 1])) &&
                    (i == 0 || !isalpha(lowercase_msg[i - 1])))
                {
                    return true; // found a bad phrase
                }
            }
        }
        return false; // no bad phrases found in the entire message
    }

    void buildTrieFromBadPhrasesFile(const std::string &filename)
    {
        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "COULD NOT OPEN BAD WORDS\n";
            return;
        }

        std::string phrase;
        while (std::getline(file, phrase))
        {
            if (phrase.empty())
            {
                continue;
            }
            insert(phrase);
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

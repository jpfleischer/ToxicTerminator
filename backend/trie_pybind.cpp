#include <pybind11/pybind11.h>

namespace py = pybind11;
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
        std::string lowercase_msg = message;
        std::transform(lowercase_msg.begin(), lowercase_msg.end(), lowercase_msg.begin(),
                       [](unsigned char c)
                       { return std::tolower(c); });

        for (int i = 0; i < lowercase_msg.length(); ++i)
        {
            trieNode *current = root;
            for (int j = i; j < lowercase_msg.length(); ++j)
            {
                char ch = lowercase_msg[j];
                if (current->children.find(ch) == current->children.end())
                {
                    break;
                }
                current = current->children[ch];
                if (current->is_end_of_phrase &&
                    (j + 1 == lowercase_msg.length() || !isalpha(lowercase_msg[j + 1])) &&
                    (i == 0 || !isalpha(lowercase_msg[i - 1])))
                {
                    return true; // Found a bad phrase
                }
            }
        }
        return false; // No bad phrases found in the entire message
    }

    void buildTrieFromBadPhrasesFile(const std::string &filename)
    {
        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "File open error\n";
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

PYBIND11_MODULE(trie, module)
{
    module.doc() = "yerr";
    // module.def("say_hello", &say_hello);

    py::class_<trie>(module, "trie")
        .def(py::init<>())
        // .def(pybind11::init<>(), "constructor 2", pybind11::arg("x"), pybind11::arg("y"))
        .def("insert", &trie::insert)
        .def("search", &trie::search)
        // .def("main", &trie::main)
        .def("buildTrieFromBadPhrasesFile", &trie::buildTrieFromBadPhrasesFile);
    // m.def("add", &add, "A function that adds two numbers");
}

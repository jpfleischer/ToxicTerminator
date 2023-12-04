#include <iostream>
#include <fstream>
#include <forward_list>
#include <algorithm>
#include <cctype>
#include <string>
#include <sstream>
#include <vector>

class hashmap
{
public:
    hashmap()
    {
        // initialization of the members in the constructor
        messageVector = std::vector<std::string>();
        // SEPCHAINMAP IS THE HASHMAP
        sepChainMap = std::vector<std::forward_list<std::string>>(1000);

        
    }
    
    std::vector<std::string> messageVector;
    std::vector<std::forward_list<std::string>> sepChainMap;
    
    int asciiSum;

    void buildHashmap(const std::string &filename)
    {
        std::ifstream file(filename);
        std::string userMessage;

        if (!file.is_open())
        {
            std::cerr << "COULD NOT FIND THE FILE\n";
            return;
        }

        while (std::getline(file, userMessage))
        {
            if (userMessage.empty())
            {
                continue;
            }

            // hash userMessage and store it in the hash map at the correct position.
            asciiSum = 0; 
            for (int i = 0; i < userMessage.length(); i++)
            {
                asciiSum += (int)userMessage[i];
            }

            int index = asciiSum % sepChainMap.size();
            sepChainMap[index].push_front(userMessage); //  indexing
            messageVector.push_back(userMessage);
        }
    }

    bool search(const std::string &message)
    {
        std::istringstream iss(message);

        std::string word;
        std::vector<std::string> words;

        // split the message into individual words
        while (iss >> word)
        {
            std::transform(word.begin(), word.end(), word.begin(),
                           [](unsigned char c)
                           { return std::tolower(c); });

            // remove special characters like newline characters
            word.erase(std::remove_if(word.begin(), word.end(), [](char c)
                                      { return !std::isalnum(c); }),
                       word.end());

            if (!word.empty())
            {
                words.push_back(word);
            }
        }

        // check phrases starting from each word in the message
        for (size_t i = 0; i < words.size(); ++i)
        {
            for (size_t j = i; j < words.size(); ++j)
            {
                std::string phrase;
                for (size_t k = i; k <= j; ++k)
                {
                    phrase += words[k];
                    if (k != j)
                    {
                        phrase += " ";
                    }

                    int asciiSum = 0; // calculate the hash value for the given phrase
                    for (char c : phrase)
                    {
                        asciiSum += static_cast<int>(c);
                    }

                    int index = asciiSum % sepChainMap.size();

                    // check each element in the forward list at the calculated index
                    for (const auto &entry : sepChainMap.at(index))
                    {
                        if (entry == phrase)
                        {
                            return true; // found
                        }
                    }
                }
            }
        }
        return false; // not found
    }

    int test(const std::string &word)
    {
        buildHashmap("../bad-words.txt");
        std::string wordToSearch = word;

        bool isBadWord = search(wordToSearch);

        if (isBadWord)
        {
            std::cout << "The word '" << wordToSearch << "' is a bad word.\n";
        }
        else
        {
            std::cout << "The word '" << wordToSearch << "' is not a bad word.\n";
        }
        return 0;
    }
};

int main()
{
    std::cout << "hey\n";
    hashmap ha = hashmap();
    ha.test("fuck"); // adds to 425
    ha.test("FUCK"); // adds to 425
    ha.test("goodietwoshoes");
    ha.test("hahahahahahahaha");
    ha.test("lamo"); // adds to 425
}

#include <iostream>
#include <random>
#include <fstream>
#include <forward_list>
#include <algorithm>
#include <cctype>
#include <string>

class hashmap
{
public:
    hashmap()
    {
        // Initialization of the members in the constructor
        messageVector = std::vector<std::string>();
        // SEPCHAINMAP IS THE HASHMAP
        sepChainMap = std::vector<std::forward_list<std::string>>(1000);

        // Setting up random number stuff.
        std::random_device rd;
        gen = std::mt19937(rd());
        distribution = std::uniform_int_distribution<int>(0, 626493);
    }
    
    std::vector<std::string> messageVector;
    std::vector<std::forward_list<std::string>> sepChainMap;
    std::mt19937 gen;
    std::uniform_int_distribution<int> distribution;
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

    bool search(const std::string &word)
    {
        std::string lower_word = word;
        std::transform(lower_word.begin(), lower_word.end(), lower_word.begin(),
                       [](unsigned char c)
                       { return std::tolower(c); });

        lower_word.erase(0, lower_word.find_first_not_of("\n\r"));
        lower_word.erase(lower_word.find_last_not_of("\n\r") + 1);

        // // Set the chars in a string to lowercase.
        // for (char &newChar : word) {
        //     newChar = std::tolower(newChar);
        // }
        
        int asciiSum = 0; // calculate the hash value for the given word
        for (int i = 0; i < lower_word.length(); i++)
        {
            asciiSum += (int)lower_word[i];
        }

        // calculate the index within the valid range of sepChainMap size
        int index = asciiSum % sepChainMap.size();

        // check each element in the forward list at the calculated index
        for (const auto &entry : sepChainMap.at(index))
        {
            if (entry == lower_word)
            {
                return true; // found
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

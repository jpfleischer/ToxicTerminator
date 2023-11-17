#include <iostream>
#include <random>
#include <fstream>
#include <forward_list>

int main() {
    // Source cited: https://stackoverflow.com/questions/38367976/do-stdrandom-device-and-stdmt19937-follow-an-uniform-distribution is where I learned where to generate random integers over a uniform distribution.
    // Setting up random number stuff.
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> distribution(0, 626493);

    // Set userTesting to 1 if there is user input, and 0 if we want to generate a random message.
    bool userTesting;
    std::cin >> userTesting;

    // If we want to execute the program for when the user types something in.
    if (userTesting) {
        std::string userInput;
        std::cin >> userInput;

    }
    // Otherwise, generate a random chat message from our dataset and check that one.
    else {

        // Create vector of forward lists. We initialize with the constant 13672 because our math showed that is the max constant size of our vector.
        static std::vector<std::forward_list<std::string>> sepChainMap (13672);

        // Creating a vector to store the messages.
        std::vector<std::string> messageVector;

        // Setting up file
        std::ifstream file("./cleaned_dota2_chat_messages.csv");
        std::string userMessage;

        // Read over entire file.
        while (!file.eof()) {
            // Read in a user message over a line.
            std::getline(file, userMessage);

            // Hash userMessage and store it in the hash map at the correct position.
            int asciiSum = 0;
            for (int i = 0; i <userMessage.length(); i++) {
                asciiSum += (int)userMessage[i];
            }
            sepChainMap.at(asciiSum).push_front(userMessage);

            // Store all the messages in a vector.
            messageVector.push_back(userMessage);
        }

        // Generate a random number. Complexity O(1).
        int randomInt = distribution(gen);

        // Store the message stored at hashMap[randomInt]
        std::string randomString;
        randomString = messageVector.at(randomInt);

        // Search hash table for our string by hashing our string and using our hashed value to search for it in our hash map.

        // Hashing our string. O(L) where L is the length of our randomly generated string from our dataset.
        int asciiSum = 0;
        for (int i = 0; i < randomString.length(); i++) {
            asciiSum += (int)randomString[i];
        }

        // Now, let's search for our string in the map using our hashed value. O(k), where k is the number of keys in the hash table that are in a given slot.
        bool successfulSearch = false;
        for (auto it = sepChainMap.at(asciiSum).begin(); it != sepChainMap.at(asciiSum).end(); it++) {
            if (*it == randomString) {
                successfulSearch = true;
                // We break so that way we only iterate up to the first instance of this message, saving time.
                break;
            }
        }

        // If we can't find our message in the map, throw an exception because that means our search function in the hash map does not work.
        // Since our hash map works, this should never execute.
        if (!successfulSearch) {
            throw std::exception();
        }

        // Search message for blocked words


        // Display whether message has blocked word.

    }
    return 0;
}

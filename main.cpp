#include <iostream>
#include <random>
#include <fstream>

int main() {
    // Source cited: https://stackoverflow.com/questions/38367976/do-stdrandom-device-and-stdmt19937-follow-an-uniform-distribution is where I learned where to generate random integers over a uniform distribution.
    // Setting up random number stuff.
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> distribution(0, 2000000);

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
        // Creating an array for the hash map.
        int arraySize = 626494;
        static std::string hashMap[626494];
        // initializing the values in the hashMap array to empty string.
        std::fill(hashMap, hashMap + 626494, "");


        // Creating a vector to store the messages.
        std::vector<std::string> messageVector;
        // Setting up file
        std::ifstream file("./cleaned_dota2_chat_messages.csv");
        std::string userMessage;

        int i = 0;
        while (!file.eof()) {
            std::getline(file, userMessage);

            //std::cout << userMessage << std::endl;
            static int asciiSum = 0;
            for (int i = 0; i <userMessage.length(); i++) {
                asciiSum += (int)userMessage[i];
            }
            //std::cout << (asciiSum % 626495) << std::endl;

            // hash userMessage and store it in the array at the correct position.
            hashMap[(asciiSum % 626494)] = userMessage;
            ++i;
        }
        

        // Generate a random number. Complexity O(1).
        // int randomInt = distribution(gen);
        // Display the message stored at hashMap[randomInt]
        // Search message for blocked words
        // Display whether message has blocked word.


    }
    return 0;
}

from cloudmesh.common.util import readfile
import pandas as pd
import cppyy
import random

# Read the C++ files
trie_cpp_file_contents = readfile('backend/trie.cpp')
hash_file_contents = readfile('backend/hashmap.cpp')

print('hello.')
cppyy.cppdef(trie_cpp_file_contents)
print('i am testing.')
cppyy.cppdef(hash_file_contents)
print('i made it through.')
trie_object = cppyy.gbl.trie()  # Create Trie object
trie_object.buildTrieFromBadPhrasesFile("bad-words.txt")  # Build Trie
hash_obj = cppyy.gbl.hashmap()  # Create Hash Map object
hash_obj.buildHashmap("bad-words.txt")  # Build Hash Map


# Define Trie and Hash Map logic functions
def check_message_with_trie(message):

    return trie_object.search(message)  # Check message using Trie

def check_message_with_hashmap(message):

    return hash_obj.search(message)  # Check message using Hash Map

# Function to process messages from DataFrame
def process_messages(df):
    problematic_messages = []
    true_count = 0
    try:
        # Apply Trie logic to each message
        true_count = df['message'].apply(lambda x: check_message_with_trie(x)).sum()
    except TypeError as e:
        problematic_messages.append(e)  # Store the problematic message causing TypeError
    
    false_count = len(df) - true_count
    return true_count, false_count, problematic_messages  # Return counts and problematic messages


# Read CSV file into a DataFrame
df = pd.read_csv('backend/chats/tf2100k.csv')
# Assuming df is your DataFrame
df.dropna(subset=['message'], inplace=True)
num_msgs = len(df)


def process_messages_route():
    true_count, false_count, problematic_messages = process_messages(df)  # Process messages
    print(problematic_messages)
    print(f'True Count: {true_count}, False Count: {false_count}')
    percent = (true_count / num_msgs) * 100  # Convert to percentage
    print(f'Bad words are {percent:.2f}% of {num_msgs} total messages')  # Display as percentage with 2 decimal places

    # Get indices of True messages
    true_indices = df[df['message'].apply(check_message_with_trie)].index.tolist()

    # Randomly select 10 indices
    random_true_indices = random.sample(true_indices, min(10, len(true_indices)))

    # Print the selected messages
    print("\nTen random messages that were flagged as 'True':")
    for index in random_true_indices:
        print(df.loc[index, 'message'])


if __name__ == "__main__":
    process_messages_route()
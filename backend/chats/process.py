from cloudmesh.common.util import readfile
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.systeminfo import os_is_windows, os_is_linux
import pandas as pd
if os_is_windows():
    import cppyy
elif os_is_linux():
    import sys
    sys.path.insert(0, '/home/toxicterminator/ToxicTerminator')
    from backend import trie
    from backend import hashmap
import random
import sys

class chatReader:
    def __init__(self, choice: str, structure: str="both"):
        if os_is_windows():
            choices = {
                'Team Fortress 2': "tf2100k.csv",
                'Minecraft': "minecraft260k.csv",
                'Dota 2': "dota2-620k.csv",
            }
        else:
            choices = {
                'Team Fortress 2': "/home/toxicterminator/ToxicTerminator/backend/chats/tf2100k.csv",
                'Minecraft': "/home/toxicterminator/ToxicTerminator/backend/chats/minecraft260k.csv",
                'Dota 2': "/home/toxicterminator/ToxicTerminator/backend/chats/dota2-620k.csv",
            }
        if choice not in choices:
            raise KeyError("please choose Team Fortress 2, " \
                           "Minecraft, or Dota 2.")
        self.choice = choice
        try:
            # Read the C++ files
            if os_is_windows():
                trie_cpp_file_contents = readfile('backend/trie.cpp')
                hash_file_contents = readfile('backend/hashmap.cpp')

                cppyy.cppdef(trie_cpp_file_contents)
                cppyy.cppdef(hash_file_contents)


            print('hello.')
            
            print('i am testing.')
            
            print('i made it through.')
        except SyntaxError:
            pass

        if os_is_windows():
            # Handle processing with Trie
            self.trie_object = cppyy.gbl.trie()
            self.trie_object.buildTrieFromBadPhrasesFile("bad-words.txt")

        elif os_is_linux():
            self.trie_object = trie.trie()
            self.trie_object.buildTrieFromBadPhrasesFile("/home/toxicterminator/ToxicTerminator/bad-words.txt")

        if os_is_windows():
            self.hash_obj = cppyy.gbl.hashmap()
            self.hash_obj.buildHashmap("bad-words.txt")
        elif os_is_linux():
            self.hash_obj = hashmap.hashmap()
            self.hash_obj.buildHashmap("/home/toxicterminator/ToxicTerminator/bad-words.txt")
        # Read CSV file into a DataFrame
        self.df = pd.read_csv(f'backend/chats/{choices[choice]}')
        # Assuming df is your DataFrame
        self.df.dropna(subset=['message'], inplace=True)
        # only 100000k !
        self.df = self.df.head(100000)
        
        

    # Define Trie and Hash Map logic functions
    def check_message_with_trie(self, message):

        return self.trie_object.search(message)  # Check message using Trie

    def check_message_with_hashmap(self, message):

        return self.hash_obj.search(message)  # Check message using Hash Map

    # Function to process messages from DataFrame
    def process_messages(self, df, datastruc: str):
        """
        data struc can be trie or hashmap
        """
        problem_errors = []
        true_count = 0
        try:
            if datastruc == 'trie':
                print('trie')
                # Apply Trie logic to each message
                true_count = df['message'].apply(lambda x: self.check_message_with_trie(x)).sum()
            else:
                print('has')
                true_count = df['message'].apply(lambda x: self.check_message_with_hashmap(x)).sum()
        except TypeError as e:
            problem_errors.append(e)  # Store the problematic message causing TypeError
        
        false_count = len(df) - true_count
        return true_count, false_count, problem_errors  # Return counts and problematic messages


    def process_messages_route(self, struc: str):
        almighty_dictionary = \
        {
            struc: {
                'game_name': None,
                'true_count': None,
                'false_count': None,
                'total_count': None,
                'problem_errors': None,
                'time': None,
                'percent': None,
                'example_bad_phrases': None
            }
        }

        # for struc in ['trie', 'hashmap']:
        print('#'*40, struc, '#'*40)
        
        StopWatch.start('timer')
        true_count, false_count, problem_errors = self.process_messages(self.df, struc)  # Process messages
        StopWatch.stop('timer')
        time_almighty = StopWatch.get('timer')
        print(problem_errors)

        num_msgs = len(self.df)

        print(f'True Count: {true_count}, False Count: {false_count}')
        percent = (true_count / num_msgs) * 100  # Convert to percentage
        print(f'Bad words are {percent:.2f}% of {num_msgs} total messages')  # Display as percentage with 2 decimal places

        if struc == 'trie':
            # Get indices of True messages
            true_indices = self.df[self.df['message'].apply(self.check_message_with_trie)].index.tolist()
        elif struc == 'hashmap':
            true_indices = self.df[self.df['message'].apply(self.check_message_with_hashmap)].index.tolist()
        else:

            raise KeyError(f'you didnt choose right one {struc}')

        # Randomly select 10 indices
        random_true_indices = random.sample(true_indices, min(10, len(true_indices)))

        # Print the selected messages
        print("\nTen random messages that were flagged as 'True':")
        for index in random_true_indices:
            print(self.df.loc[index, 'message'])

        almighty_dictionary[struc] = {
            'game_name': self.choice,
            'true_count': true_count,
            'false_count': false_count,
            'total_count': len(self.df),
            'problem_errors': problem_errors,
            'time': f'{time_almighty} seconds',
            'percent': f'{percent:.2f}%',
            'example_bad_phrases': [self.df.loc[index, 'message'] for index in random_true_indices]
        }
        return almighty_dictionary


if __name__ == "__main__":
    choice = sys.argv[1]
    print(choice)
    obj = chatReader(choice)

    obj.process_messages_route()
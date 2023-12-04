from flask import Flask, render_template, request, Response, jsonify
import json
import threading
import csv
import random


from cloudmesh.common.util import readfile
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.systeminfo import os_is_windows, os_is_linux
from queue import Queue
import numpy as np

if os_is_windows():
    import cppyy
elif os_is_linux():
    import sys
    sys.path.insert(0, '/home/toxicterminator/ToxicTerminator')
    from backend import trie
    from backend import hashmap

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '.')


# trie_obj = trie()
# trie_obj.buildtrieFromBadWordsFile("")
# trie_obj.main("bad-words.txt")


app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        if os_is_windows():
            trie_cpp_file_contents = readfile('backend/trie.cpp')
            hash_file_contents = readfile('backend/hashmap.cpp')

            cppyy.cppdef(trie_cpp_file_contents)
            cppyy.cppdef(hash_file_contents)

        
    except SyntaxError:
        pass

    # trie_object = cppyy.gbl.trie()  # Create Trie object

    if request.method == 'POST':
        # message-contents contains the message that the user input into the text box.
        message_content = request.form.get('message-contents')
        selected_option = request.form['data-structure']  # Get the selected radio button value
        print('!!!!!!!!!!!!!!', selected_option)
        if selected_option == 'trie':
            StopWatch.start('trie')
            print('trie')

            if os_is_windows():
                # Handle processing with Trie
                trie_object = cppyy.gbl.trie()
                trie_object.buildTrieFromBadPhrasesFile("bad-words.txt")

            elif os_is_linux():
                trie_object = trie.trie()
                trie_object.buildTrieFromBadPhrasesFile("/home/toxicterminator/ToxicTerminator/bad-words.txt")

            # print(trie_object)
            
            it_is_bad = trie_object.search(message_content)
            print(message_content, f'BAD WORD: {it_is_bad}')
            StopWatch.stop('trie')
            time = StopWatch.get('trie')
            return_message = f'BAD WORD! NAUGHTY! 👿 Seconds: {time}' if it_is_bad else f'Not a bad word! You are so nice 😇 Seconds: {time}'

        elif selected_option == 'hashmap':
            # Handle processing with Hash Map or any other logic
            # ...
            StopWatch.start('hashmap')
            print("HAAAAASH!")

            if os_is_windows():
                hash_obj = cppyy.gbl.hashmap()
                hash_obj.buildHashmap("bad-words.txt")
            elif os_is_linux():
                hash_obj = hashmap.hashmap()
                hash_obj.buildHashmap("/home/toxicterminator/ToxicTerminator/bad-words.txt")
            # print(hash_obj)
            
            print('debugging')
            print(message_content)
            it_is_bad = hash_obj.search(message_content)
            StopWatch.stop('hashmap') 
            time = StopWatch.get('hashmap')
            return_message = f'BAD WORD! NAUGHTY! 👿 Second: {time}' if it_is_bad else f'Not a bad word! You are so nice 😇 Seconds: {time}'

        return return_message


# this route points to root /
@app.route('/', methods=['POST', 'GET'])
def hello_world():

    return render_template('solution.html')


@app.route('/game-comparison', methods=['POST', 'GET'])
def game():

    return render_template('game.html')


@app.route('/calculate-toxicity', methods=['POST'])
def calculate_toxicity():
    game = request.form['game']
    data_structure = request.form['dataStructure']

    # Perform your toxicity calculation logic here for the specified game and data structure
    # ...
    # Example: Calculate and prepare live updates
    live_updates = f"Calculating toxicity for {game} using {data_structure}. Progress: 25%. Message: 'Sample message'."
    # ...

    # Return live updates as HTML content
    return live_updates

# def run_analysis():
#     from backend.chats.process import chatReader
#     obj = chatReader('tf2')

#     obj.process_messages_route()

@app.route('/live-updates/<game>/<data_structure>')
def live_updates(game, data_structure):
    def generate():
        def run_analysis(game, data_structure, queue):
            # Process messages for the specified game and data structure
            data_structure = data_structure.split('(')[-1][:-1].lower()
            if data_structure == 'hash':
                data_structure = 'hashmap'
            from backend.chats.process import chatReader
            obj = chatReader(game)
            # Additional logic based on data_structure if needed
            almighty_dictionary = obj.process_messages_route(data_structure)
            queue.put(almighty_dictionary)  # Put the dictionary into the queue

        
        queue = Queue()  # Create a Queue object to communicate between threads
        thread = threading.Thread(target=run_analysis, args=(game, data_structure, queue))
        thread.start()
        
        def np_encoder(object):
            if isinstance(object, np.generic):
                return object.item()

        yield "data: Analysis started...\n\n"
        from pprint import pprint
        thread.join()  # Wait for the analysis thread to finish
        result = queue.get()  # Retrieve the result from the queue
        pprint(result)
        print(type(result))
        json_data = json.dumps(result, default=np_encoder)
        
        pprint(json_data)
        print(':)')
        yield f"data: {json_data}\n\n"
        yield "data: END!\n\n"

    return Response(generate(), content_type='text/event-stream')

@app.route('/get-random-message/<game_id>')
def get_random_message(game_id):
    print('who dares enter')
    # Define the file paths for each game's CSV
    if os_is_linux():
        game_csv_paths = {
            'tf2': '/home/toxicterminator/ToxicTerminator/backend/chats/tf2100k-short.csv',
            'minecraft': '/home/toxicterminator/ToxicTerminator/backend/chats/minecraft260k-short.csv',
            'dota2': '/home/toxicterminator/ToxicTerminator/backend/chats/dota2-620k-short.csv'
        }
    else:
        game_csv_paths = {
            'tf2': 'backend/chats/tf2100k-short.csv',
            'minecraft': 'backend/chats/minecraft260k-short.csv',
            'dota2': 'backend/chats/dota2-620k-short.csv'
        }

    if game_id in game_csv_paths:
        csv_path = game_csv_paths[game_id]
        # Read the first 100 lines of the CSV file using DictReader
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            messages = []
            for idx, row in enumerate(reader):
                if idx < 100:
                    messages.append(row['message'])

            if messages:
                random_message = random.choice(messages)
                return jsonify({'message': random_message})
    
    return jsonify({'message': 'Invalid game ID or no messages found'})
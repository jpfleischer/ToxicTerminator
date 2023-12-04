from flask import Flask, render_template, request, Response, jsonify
import json
import threading
# import sys
# import os
# sys.path.insert(0, '')
# from backend import trie

from cloudmesh.common.util import readfile
from cloudmesh.common.StopWatch import StopWatch
from queue import Queue
import numpy as np
import cppyy

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

            # Handle processing with Trie
            trie_object = cppyy.gbl.trie()
            print('trie')
            print(trie_object)
            trie_object.buildTrieFromBadPhrasesFile("bad-words.txt")
            it_is_bad = trie_object.search(message_content)
            print(message_content, f'BAD WORD: {it_is_bad}')
            StopWatch.stop('trie')
            time = StopWatch.get('trie')
            return_message = f'BAD WORD! NAUGHTY! 👿 Seconds: {time}' if it_is_bad else f'Not a bad word! You are so nice 😇 Seconds: {time}'

        elif selected_option == 'hashmap':
            # Handle processing with Hash Map or any other logic
            # ...
            StopWatch.start('hashmap')
            hash_obj = cppyy.gbl.hashmap()
            print("HAAAAASH!")
            print(hash_obj)
            hash_obj.buildHashmap("bad-words.txt")
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
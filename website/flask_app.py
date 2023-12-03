from flask import Flask, render_template, request
# import sys
# import os
# sys.path.insert(0, '')
# from backend import trie

from cloudmesh.common.util import readfile
from cloudmesh.common.StopWatch import StopWatch
# StopWatch.start('mytimer')
# # 
# StopWatch.stop('mytimer')
# StopWatch.benchmark()
import cppyy


trie_cpp_file_contents = readfile('backend/trie.cpp')
hash_file_contents = readfile('backend/hashmap.cpp')

print('hello.')
cppyy.cppdef(trie_cpp_file_contents)
print('i am testing.')
cppyy.cppdef(hash_file_contents)
print('i made it through.')

from cppyy.gbl import trie, hashmap
# trie_obj = trie()
# trie_obj.buildtrieFromBadWordsFile("")
# trie_obj.main("bad-words.txt")


app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        # message-contents contains the message that the user input into the text box.
        message_content = request.form.get('message-contents')
        selected_option = request.form['data-structure']  # Get the selected radio button value
        print('!!!!!!!!!!!!!!', selected_option)
        if selected_option == 'trie':
            StopWatch.start('trie')
            # Handle processing with Trie
            trie_object = trie.trie()
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
            hash_obj = hashmap.hashmap()
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



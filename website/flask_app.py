from flask import Flask, render_template, request
# import sys
# import os
# sys.path.insert(0, '')
# from backend import trie

from cloudmesh.common.util import readfile
import cppyy

trie_cpp_file_contents = readfile('backend/trie_cpy.cpp')
hash_file_contents = readfile('backend/hashmap.cpp')

cppyy.cppdef(trie_cpp_file_contents)
cppyy.cppdef(hash_file_contents)

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
            # Handle processing with Trie
            trie_object = trie.trie()
            print('trie')
            print(trie_object)
            trie_object.buildtrieFromBadWordsFile("bad-words.txt")
            it_is_bad = trie_object.search(message_content)
            return_message = 'BAD WORD! NAUGHTY! 👿' if it_is_bad else 'Not a bad word! You are so nice 😇'

        elif selected_option == 'hashmap':
            # Handle processing with Hash Map or any other logic
            # ...

            hash_obj = hashmap.hashmap()
            print("HAAAAASH!")
            print(hash_obj)
            hash_obj.buildHashmap("bad-words.txt")
            it_is_bad = hash_obj.search(message_content)
            return_message = 'BAD WORD! NAUGHTY! 👿' if it_is_bad else 'Not a bad word! You are so nice 😇'

        return return_message


# this route points to root /
@app.route('/', methods=['POST', 'GET'])
def hello_world():

    return render_template('solution.html')



from flask import Flask, render_template, request
import sys
import os
sys.path.insert(0, '')
from backend import trie

app = Flask(__name__)

# this route points to root /
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        # message-contents contains the message that the user input into the text box.
        message_content = request.form.get('message-contents')
        # this line imports the C++ python binding program, tree implementation.
        trie_object = trie.trie()
        trie_object.buildtrieFromBadWordsFile("bad-words.txt")
        print('!!!')
        it_is_bad = False
        if trie_object.search(message_content):
             it_is_bad = True
        if it_is_bad:
            return_message = 'BAD WORD! NAUGHTY! 👿'
        else:
            return_message = 'not a bad word you are so nice 😇'
        # print(trie_object.search(message_content))
        # print('!!!')
        # print(message_content)
        # print('we got it :)')

        return render_template('solution.html', forward_message=return_message);
    else:
        return render_template('solution.html')



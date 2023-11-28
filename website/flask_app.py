from flask import Flask, render_template, request
import sys
import os
sys.path.insert(0, '')
from backend import trie

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        
        message_content = request.form.get('message-contents')
        hey = trie.trie()
        hey.buildtrieFromBadWordsFile("bad-words.txt")
        print('!!!')
        it_is_bad = False
        if hey.search(message_content):
             it_is_bad = True
        if it_is_bad:
            return_message = 'BAD WORD! NAUGHTY! 👿'
        else:
            return_message = 'not a bad word you are so nice 😇'
        # print(hey.search(message_content))
        # print('!!!')
        # print(message_content)
        # print('we got it :)')

        return render_template('solution.html', forward_message=return_message);
    else:
        return render_template('solution.html')



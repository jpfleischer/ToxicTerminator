file_name := bad-words.txt
url := https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/en.txt

run:
	if [ ! -f "$(file_name)" ]; then \
        curl -o "$(file_name)" "$(url)"; \
        echo "'$(file_name)' downloaded"; \
	else \
        echo "'$(file_name)' already exists"; \
    fi

	# g++ -o trie backend/trie.cpp
	# ./trie

serve:
	flask --app website/flask_app --debug run
	# python website/run.py

process:
	python backend/chats/process.py

# this is a makefile that allows us to use
# the make command
# so we can say make install
# or make requirements
# or make python
# and then this command will execute.
install requirements python:
	pip install -r requirements.txt
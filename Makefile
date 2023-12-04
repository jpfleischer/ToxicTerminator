file_name := bad-words.txt
url := https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/en.txt

run:
	if [ ! -f "$(file_name)" ]; then \
		curl -o "$(file_name)" "$(url)"; \
		echo "'$(file_name)' downloaded"; \
	else \
		echo "'$(file_name)' already exists"; \
	fi
	cd backend/chats & make;
	# g++ -o trie backend/trie.cpp
	# ./trie

test:
	# g++ hashmap.cpp -o hashmap.exe
	# ./hashmap.exe
	g++ backend/trie.cpp -o backend/trie.exe
	backend/trie.exe

serve:
	flask --app website/flask_app --debug run
	# python website/run.py

process:
	python backend/chats/process.py "Team Fortress 2"

# this is a makefile that allows us to use
# the make command
# so we can say make install
# or make requirements
# or make python
# and then this command will execute.
install requirements python:
	pip install -r requirements.txt
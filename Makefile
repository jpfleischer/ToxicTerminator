run:
	./get-data.sh
	g++ -o trie trie.cpp
	./trie

serve:
	flask --app website/flask_app --debug run
	# python website/run.py

# this is a makefile that allows us to use
# the make command
# so we can say make install
# or make requirements
# or make python
# and then this command will execute.
install requirements python:
	pip install -r requirements.txt
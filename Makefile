run:
	./get-data.sh
	g++ -o trie trie.cpp
	./trie

serve:
	flask --app website/flask_app --debug run
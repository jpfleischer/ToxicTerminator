test:
	# g++ hashmap.cpp -o hashmap.exe
	# ./hashmap.exe
	g++ trie.cpp -o trie.exe
	./trie.exe

compile:
	g++ hashmap.cpp -o hashmap.exe

pybind:
	# . ~/ENV3/bin/activate ; \
	# which python ; \
	# python3-config --extension-suffix ; \
	c++ -O3 -Wall -shared -std=c++11 -fPIC $(python -m pybind11 --includes) trie_pybind.cpp -o trie.cpython-310-x86_64-linux-gnu.so
	c++ -O3 -Wall -shared -std=c++11 -fPIC $(python -m pybind11 --includes) hashmap_pybind.cpp -o hashmap.cpython-310-x86_64-linux-gnu.so



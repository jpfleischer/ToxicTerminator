compile:
	g++ hashmap.cpp -o hashmap.exe

wsl:
	. ~/ENV3/bin/activate ; \
	which python ; \
	python3-config --extension-suffix ; \
	c++ -O3 -Wall -shared -std=c++11 -fPIC $(python -m pybind11 --includes) trie.cpp -o trie.cpython-310-x86_64-linux-gnu.so



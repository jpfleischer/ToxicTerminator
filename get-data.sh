#!/bin/bash

file_name="bad-words.txt"
url="https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/en.txt"

if [ ! -f "$file_name" ]; then
    curl -o "$file_name" "$url"
    echo "'$file_name' downloaded"
else
    echo "'$file_name' already exists"
fi

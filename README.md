# ToxicTerminator

first time setup:

```bash
# put it in your home dir or anywhere you want
cd 
# im in my home dir now
git clone git@github.com:jpfleischer/ToxicTerminator.git
cd ToxicTerminator
```

please make sure you have make on windows
then stand in the directory and say

```bash
make
```

this downloads the data and runs through the
trie to find if the inputted word is a bad word.

if you dont have make, and you dont have chocolatey,
you can get chocolatey https://chocolatey.org/
and then say `choco install make mingw -y`
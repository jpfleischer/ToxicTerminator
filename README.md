# ToxicTerminator

<font size=4>Visit our website at https://toxicterminator.pythonanywhere.com/</font>

![](demo.gif)

<font size=4><u>The question: can we quantify toxicity in online video games?</u></font>

ToxicTerminator is a fullstack app that is meant to demonstrate simple data structures that scan for blacklisted phrases within chat messages. It features a live sandbox for testing user-inputted messages as well as random video game messages taken from real datasets.

The app also has a page for comprehensively testing 100k datapoints from each game and measuring each game's total toxicity. This is made possible by the C++ backend sending live updates to the Python frontend, made with Flask.

This project is an example of use of the [cloudmesh toolkit](https://cloudmesh.github.io/), a Python library meant to make cloud computing easier.

## Setup

Setup is simple. The only prerequisite
is chocolatey https://chocolatey.org/

Then open a terminal. Git Bash is the best but
Powershell works just as well (run as Administrator)

```bash
choco install make git python visualstudio2019buildtools visualstudio2019-workload-vctools -y

# we assume you do not want to push directly to the
# repo, so we just give you HTTPS clone.
# lets put it in your home dir (doesnt matter)
cd 
# im in my home dir now!

git clone https://github.com/jpfleischer/ToxicTerminator.git
cd ToxicTerminator

# make and activate a venv
python -m venv ~/ENV3

# if using git bash
source ~/ENV3/Scripts/activate
# if using powershell
. ~/ENV3/Scripts/activate.ps1

pip install -r requirements.txt

# this will take around 350 MB
make
# now you have the bad words list and the chats.

make serve
```

Then open a browser and go to [127.0.0.1:5000](127.0.0.1:5000)
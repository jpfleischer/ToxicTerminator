# ToxicTerminator

setup is simple. the only prerequisite
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
make
# now you have the bad words list.

make serve
```

Then open a browser and go to 127.0.0.1:5000

import webbrowser as web
import pyperclip
from sys import argv
from os import getenv

def load_data(data):
    lines = data.split("\n")
    w = [] # words
    d = [] # definitions
    for i in range(0,len(lines),4):
        # ':-1' because each word ends in a :
        w.append(lines[i].split(" ")[1][:-1]) # splice syntax
        d.append(lines[i+1])
    return(w,d)

def read_data(paths):
    # Search a number of paths to read a file, so you can put it in whichever
    data = None
    for path in paths:
        try:
            with open(path,mode="r") as f:
                data = f.read()
    if data:
        return data
    else:
        raise Exception("No paths succeeded for 'data.txt':\n\tTried all in {paths}")

home = getenv("HOME") # The folder Desktop, Documents, etc. are in
f = "data.txt"
datapaths = [f"{home}/{f}",f"{home}/Documents/{f}",f"{home}/Desktop/{f}"]

if __name__ == "__main__":
    data = read_data(datapaths)

    # Sometimes there are extra lines of whitespace and it breaks because the number
    #  of lines is not a multiple of four
    data = data.strip()
    #  \n means start a new line
    #  what this means:
    #   hello\n
    #   a greeting\n
    #   \n # inserted by google docs as a page break
    #   - hello, person!
    #  ...
    #  number of lines is now not a multiple of four because there's an extra
    data.replace("\n\n","\n")

    words, defs = load_data(data)

    percent_done = 0.0
    increment = 100 / len(words)
    print(f"Percent: {round(percent_done,2)}")
    print(f"Increment: {increment}")

    # you can do 'python3 abra.py <word>', and it skips to that word
    if len(argv) > 1: # argv[0] = <program name>
        while words[0] != argv[1]:
            print(f"Skipping {words.pop(0)}")
            defs.pop(0)

            # make sure the percentage starts at right amount
            #  when you skip forward
            percent_done += increment
        print(f"Starting at {round(percent_done,2)}%")

    def newtab(url):
        web.open(url,new=2)

    for i in range(0,len(words)):
        input("press enter for next word")

        print(f"Now {round(percent_done,2)}% done")
        percent_done += increment

        print(words[i])

        pyperclip.copy(defs[i])
        print("copied definition")

        newtab(f"https://etymonline.com/search?q={words[i]}")
        newtab(f"https://www.google.com/search?q={words[i]}+synonyms&source=lmns&hl=en")
        newtab(f"https://www.google.com/search?q={words[i]}&tbm=isch")
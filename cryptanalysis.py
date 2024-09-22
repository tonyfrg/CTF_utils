import base64
from string import ascii_lowercase

default_table = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "J"],
    ["K", "L", "M", "N", "O"],
    ["P", "Q", "R", "S", "T"],
    ["U", "V", "X", "Y", "Z"]
    ]

def caesar(text: str, key: int):
    #ex : caesar("a",3)="d"
    text = text.lower()
    m = ""
    for t in text:
        m += ascii_lowercase[(ascii_lowercase.find(t)+key)%len(ascii_lowercase)]
    return m

def polybe(text: str, table=default_table):
    #rows indicated by abcde, and columns by 12345
    #not optimised but ok
    plain = ""
    block = ""
    for char in text:
        if char in " :/\n":
            plain += char
        if char in "abcde":
            block += char
        if char in "12345":
            plain += table["abcde".index(block)]["12345".index(char)]
            block =""
    return plain

def frequency_analysis(text: str, removing: str):
    #remove all char in removing string
    for char in removing:
        text = text.replace(char, "")
    freq = {}
    for letter in text:
        if letter not in freq:
            freq[letter] = 0
        freq[letter] += 1
    freq_percent = {char: ((count / len(text)) * 100) for char, count in freq.items()}
    return dict(sorted(freq_percent.items(), key=lambda x: x[1], reverse=True))
    

if __name__=="__main__":
    print(caesar("abdz", 3))
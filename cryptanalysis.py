import base64
from string import ascii_lowercase
from utils import *

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

def frequency_analysis(text: str, removing="", percent=True):
    #remove all char in removing string
    for char in removing:
        text = text.replace(char, "")
    freq = {}
    for letter in text:
        if letter not in freq:
            freq[letter] = 0
        freq[letter] += 1
    if percent:
        freq_percent = {char: round((count / len(text)) * 100, 2) for char, count in freq.items()}
        return dict(sorted(freq_percent.items(), key=lambda x: x[1], reverse=True))
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

#alphabet coming from a challenge
hill_alphabet = {'!': 8, ' ': 42, ',': 58, '.': 6, '1': 7, '0': 1, '3': 34, '2': 37, '5': 3, '4': 47, '7': 43, '6': 63,
            '9': 54, '8': 13, '?': 60, 'A': 35, 'C': 57, 'B': 16, 'E': 31, 'D': 64, 'G': 9, 'F': 23, 'I': 29, 'H': 32,
            'K': 55, 'J': 53, 'M': 21, 'L': 5, 'O': 52, 'N': 41, 'Q': 40, 'P': 26, 'S': 22, 'R': 18, 'U': 51, 'T': 15,
            'W': 17, 'V': 62, 'Y': 45, 'X': 66, 'Z': 50, 'a': 25, 'c': 38, 'b': 0, 'e': 30, 'd': 33, 'g': 14, 'f': 2,
            'i': 10, 'h': 4, 'k': 59, 'j': 39, 'm': 11, 'l': 28, 'o': 12, 'n': 19, 'q': 24, 'p': 49, 's': 46, 'r': 61,
            'u': 20, 't': 27, 'w': 36, 'v': 44, 'y': 56, 'x': 48, 'z': 65}

#doesn't work, or the word isn't in the plaintext
def hill_cipher_cracker(cipher: str, k_len: int, alphabet: dict, word=None):
    ### we will slide the known-word along the message until the crack show a good message
    N = len(alphabet) #we do operation mod N
    w_matrix = [[alphabet[word[i+k_len*j]] for i in range(k_len)] for j in range(k_len)] #plain reference
    k = k_len**2 + k_len - 1 #lenght of the sample
    n = len(cipher) - k #number of possible positions
    for a in range(n):
        print(f"Current sample: {a} over {n}.")
        sample = [alphabet[l] for l in cipher[a:a+k]]
        s_matrix = [[sample[i+k_len*j] for i in range(k_len)] for j in range(k_len)]
        #the key matrix will normally be S^{-1}*W
        K = matrix_mod_product(matrix_mod_inv(s_matrix, N), w_matrix, N)
        if K==None:
            print("Key can't be compute in this situation")
            continue
        #decryption of the message
        plain = ""
        for i in range(len(cipher)//k_len):
            block = [alphabet[cipher[j+3*i]] for j in range(k_len)]
            P = matrix_mod_product(K, block, N)
            for p in P:
                plain += next(k for k, v in alphabet.items() if v == p)
        #_ = input(plain)
        print(plain)
        if "cipher" in plain or "Hill" in plain or "pass" in plain:
            return plain



if __name__=="__main__":
    hilled = """EgiMbrC7AbHOTyCiRJTU4eWlQwfgK4?fGQvzcjXBBw?NpxK6rv3OsObp?N9vjIqzHC?O9WwOT1VVtu32my2CzNNkHTozl5W,nE7Lm4rBJucP8XezREIuzgl0C7ANnn.561s9jBIYgECq!8XezREBDQ6sOG2i44iQIligvf9.Auk5hgNMuzREcjXzvPWrieWlQwfgK4km0xS?o0tuPB7VJo0t,nOwCUZAyxYyf0LvcfrIFmbPJDoAs9xaJA!cQF8?ffkln7SKO.h CVdc?JqPiAK9c8jt5Ck9ZAyrVP.y13pyC6OdvrN1dkHTseEgnDHQGEfKjBIf90KjAyFNBBwtXMaTZpbycC3HiqFp07SK44inxH5YAvEEml?CKjNQoCJwzNNbHOTyCnE"""
    hill_back = hill_cipher_cracker(hilled, 3, hill_alphabet, "ciphertext")
    print(f"Plain text is: {hill_back}")
    print(len(hill_alphabet))
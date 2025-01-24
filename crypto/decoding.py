import os, subprocess
import base64
import re

morse_dict = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--',
    '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.', ' ': '/'
}

def decoding(text: str):
    if "." in text:
        print("morse")
        return decode_morse(text)
    if re.match(r'^[0-9A-Fa-f]+$', text):
        print("hex")
        return bytearray.fromhex(text).decode()
    try:
        print("b64")
        return base64.b32decode(text).decode()
    except:
        try:
            print("b32")
            return base64.b64decode(text).decode()
        except:
            print("b85")
            return base64.b85decode(text).decode()

def decode_morse(morsed: str):
    decoded = ""
    chars = morsed.split("/")
    for c in chars:
        for l, m in morse_dict.items():
            if c==m:
                decoded += l
    return decoded
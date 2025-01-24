from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import binascii
import requests

"""def find_iv(plaintext, ciphertext, key):
    key = base64.b64decode(key)
    ciphertext = base64.b64decode(ciphertext)
    plaintext = pad(plaintext.encode(), AES.block_size)
    block_size = AES.block_size
    first_cipher_block = ciphertext[:block_size]
    iv = bytes([a ^ b for a, b in zip(first_cipher_block, plaintext[:block_size])])
    
    return iv

# Données du challenge
plaintext = '''Marvin: "I am at a rough estimate thirty billion times more intelligent than you. Let me give you an example. Think of a number, any number."
Zem: "Er, five."
Marvin: "Wrong. You see?"'''
ciphertext = '''cY1Y1VPXbhUqzYLIOVR0RhUXD5l+dmymBfr1vIKlyqD8KqHUUp2I3dhFXgASdGWzRhOdTj8WWFTJ
PK0k/GDEVUBDCk1MiB8rCmTZluVHImczlOXEwJSUEgwDHA6AbiCwyAU58e9j9QbN+HwEm1TPKHQ6
JrIOpdFWoYjS+cUCZfo/85Lqi26Gj7JJxCDF8PrBp/EtHLmmTmaAVWS0ID2cJpdmNDl54N7tg5TF
TrdtcIplc1tDvoCLFPEomNa5booC'''
key = 'AQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRqrHB0eHyA='

# Calcul de l'IV
iv = find_iv(plaintext, ciphertext, key)
print(f"Vecteur d'initialisation (IV) : ", binascii.hexlify(iv).decode())
"""

url = "http://aes.cryptohack.org/"
block_size = 32

### work for cryptohack
def encrypt_web(plaintext):
    r = requests.get(url + plaintext.hex())
    return bytes.fromhex(r.json()["ciphertext"])

def oracle_padding_attack():
    known_flag = b""
    while len(known_flag) < block_size:
        padding_len = block_size - (len(known_flag) % block_size) - 1
        padding = b"A" * padding_len
        reference_ciphertext = encrypt_web(padding)[:block_size]
        for i in range(256):  # each byte value
            trial_input = padding + known_flag + bytes([i])
            trial_ciphertext = encrypt(trial_input)[:block_size]
            if trial_ciphertext == reference_ciphertext:
                known_flag += bytes([i])
                print(f"Flag so far: {known_flag}")
                break

    return known_flag

# Lancer l'attaque
flag = oracle_padding_attack()
print("Flag found:", flag)

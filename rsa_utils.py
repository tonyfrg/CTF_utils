from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
import os, subprocess
from Crypto.PublicKey import RSA
import base64
import rsa

def pb_pem_to_int(file):
    #We suppose either the file is in the same folder than the programm
    #return a tuple (n,e)
    command = f"openssl rsa -pubin -in {file} -text -noout"
    try:
        result = subprocess.check_output(command, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

    except subprocess.CalledProcessError as cpe:
        result = cpe.output
        os.abort()
    result = result.decode().replace(" ", "").replace("\n","").replace("\r","")
    e = int(result.split("Exponent:")[-1].split("(")[0])
    n_hex = result.split("Modulus:")[-1].split("Exponent:")[0]
    n = int(n_hex.replace(":",""), 16)
    print(f"n = {n}\ne = {e}")
    return n,e

def decipher_RSA(p,q,e,c):
    if type(c)==str:
        c = bytes_to_long(c)
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi)
    m = pow(c, d, p*q)
    return long_to_bytes(m)

def create_RSA_prv_key(n,d,e):
    key = RSA.construct((n, e, d))
    private_key_pem = key.export_key(format='PEM')
    with open("private_key.pem", "wb") as f:
        f.write(private_key_pem)
    print(private_key_pem.decode())

def decipher_RSA_formal(p,q,e,c):
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi)

    old_pub_key = {
        'e': e,
        'n': p*q
    }

    old_priv_key = {
        'd': d,
        'p': p,
        'q': q
    }
    pub_key = rsa.PublicKey(**old_pub_key)

    old_priv_key.update(old_pub_key)
    priv_key = rsa.PrivateKey(**old_priv_key)

    cipher_text = base64.b64decode(c)

    plain_text = rsa.decrypt(cipher_text, priv_key)
    print(f"Texte déchiffré : {plain_text.decode('utf-8')}")

    return plain_text



if __name__=="__main__":
    print("no entry")
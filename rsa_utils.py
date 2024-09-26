from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
import os, subprocess
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
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


def weiner_attack(n: int, e: int, l=10):
    #We suppose that d < 1/3 * sqrt(n, 4)
    #First : compute DFC of e/n
    p0, p1 = e, n
    q = p0//p1
    quotients = [q]
    convergents = [(q,1)]
    ppn, ppd = 1, 0  # pre-pre numerator and denominator of convergent
    pn, pd = q, 1  # pre numerator and denominator of convergent
    while q*p1!=p0:
        p0, p1 = p1, p0-q*p1
        q = p0//p1
        num, den = q*pn+ppn, q*pd+ppd
        quotients.append(q)
        ppn, ppd = pn, pd
        pn, pd = num, den
        convergents.append((num, den))
        if p1==0:
            break
    T = pow(2,E,n)
    for fract in convergents:
        d = fract[1]
        if pow(T,d, n)==2:
            print(f"d = {d} suceed the test")
            return d
    print("No solution")
    return 0

def bezout(a, b):
    s, t, u, v = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, s, t, b, u, v = b, u, v, a - q * b, s - q * u, t - q * v
    return (a, s, t) if a > 0 else (-a, -s, -t)

def choosen_plaintext_attack(n,e,c):
    #with an oracle which applie power d mod n to a given message, we can uncipher some message
    #output here is the candidate to give to the oracle
    #after that, we have to compute
    k = 2 #relatively prime to e
    d, s, r = bezout(e,k)
    print(k*r+e*s==d)
    if d>1:
        print("Error: k and e must be relatively prime")
        return 0
    c1 = pow(c,k,n)
    print(c1)
    m1 = int(input("What gives you the oracle ?"))
    mr = pow(m1, r, n)
    cs = pow(c, s, n)
    m = (mr * cs) % n
    if pow(m, e, n)==c:
        print("that's good")
    else:
        print("no no no")
    return m

def create_pem_key(n,p,q,e):
    phi = (p-1)*(q-1)
    d = pow(e,-1,phi)
    private_key = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=d%(p-1),
        dmq1=d%(q-1),
        iqmp=pow(q, -1, p),
        public_numbers=rsa.RSAPublicNumbers(e, n)
    ).private_key()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open('private_key.pem', 'wb') as pem_out:
        pem_out.write(pem)

    os.chmod('private_key.pem', 0o600) #suppose to make secure key (need to be tested)
    print(f"File privite_key.pem is create ! Well done")

if __name__=="__main__":
    print("...")
import subprocess, os

### CURL ### https://www.hostinger.fr/tutoriels/comment-utiliser-la-commande-curl-sous-linux

def curl_GET(website, options):
    command = f"curl {website}"
    try:
        result = subprocess.check_output(command, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

    except subprocess.CalledProcessError as cpe:
        result = cpe.output
        os.abort()
    print(result.decode())

def curl_output(website, file="ouput.txt"):
    # send the output in the specified file
    command = f"curl {website}/{file}"
    try:
        result = subprocess.check_output(command, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

    except subprocess.CalledProcessError as cpe:
        result = cpe.output
        os.abort()
    print(result.decode())

def curl_HTTP(website, request):
    command = f"curl -d {request} {website}"
    try:
        result = subprocess.check_output(command, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

    except subprocess.CalledProcessError as cpe:
        result = cpe.output
        os.abort()
    print(result.decode())
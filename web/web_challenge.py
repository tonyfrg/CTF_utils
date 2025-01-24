import requests
from bs4 import BeautifulSoup

"""
tools to use:
- pwntools: need config but that's great
- ffuf: enumerate chemins from wordlist (fuzzing)
- katana: enumerate chemins from HTTP response (crawling)
- nmap: enumarate open port (scanning)
- tdlr: similar to man

LEARN :
[Web-Server] : SQL Injection
[Web-Client] : Cross-Site Scripting
[Web-Server] : Local File Inclusion
[Web-Server] : File-Upload
[Web-Server] : OS Command Injection
[Web-Server] : Authentification
[Web-Client] : Cross-Site Request Forgery
[Web-Server] : Business Logic Errors
[Web-Server] : Server-Side Template Injection
"""

def get_html(url: str, raw=False):
    session = requests.Session()
    try:
        response = session.get(url)
        response.raise_for_status()  #connexion verification
    except requests.RequestException as e:
        print(f"Error during connexion on site: {e}")
        exit()

    soup = BeautifulSoup(response.text, 'html.parser') #all the htlm code
    if raw:
        return soup
    return str(soup).split("</sub>") #return a list

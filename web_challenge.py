import requests
from bs4 import BeautifulSoup


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

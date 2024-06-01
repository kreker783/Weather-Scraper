import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL
url = "https://www.google.com/search?q=weather+gdansk"
HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept-Language": "en-US,en;q=0.5",
}

def _get_soup(header, url):
    
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": header["User-Agent"],
            "Accept-Language": header["Accept-Language"]
        })
        html = session.get(url)
        return BeautifulSoup(html.text, "html.parser")
    except:
        print(f"ERROR: Unable to retrieve data from {url}")
        return None

soup = _get_soup(HEADER, url)
week = soup.find(id="wob_dp")
item = week.find_all(class_='wob_df')

week_temp = [item.find(class_='wob_t').get_text() for item in item]

print(item)
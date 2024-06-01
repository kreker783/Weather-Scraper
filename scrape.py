import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL
url = "https://www.google.com/search?client=firefox-b-d&start={}&q=weather+gdansk"
HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Language": "en-US,en;q=0.5",
}

r = requests.get(url)


def _get_soup(header, url):
    
    try:
        session = requests.Session()
        session.headers["User-Agent"] = header["User-Agent"]
        session.headers["Accept-Language"] = header["Language"]
        session.headers["Content-Language"] = header["Language"]
        html = session.get(url)
        return BeautifulSoup(html.text, "html.parser")
    except:
        print(f"ERROR: Unable to retrieve data from {url}")
        return None

soup = _get_soup(HEADER, url)
week = soup.find(id="wob_dp")
item = week.find_all(class_='wob_df')
# items = [item.find_all(class_='wob_t').()]

week_temp = [[item.find(class_='wob_t').get_text() for item in item]]

print(week_temp)
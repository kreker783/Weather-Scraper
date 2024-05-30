import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL
url = "https://www.google.com/search?client=firefox-b-d&start={}&q=weather+gdansk"
r = requests.get(url)


# def _get_soup(header, url):
#     """This functions simply gets the header and url, creates a session and
#        generates the "soup" to pass to the other functions.

#     Args:
#         header (dict): The header parameters to be used in the session.
#         url (string): The url address to create the session.

#     Returns:
#         bs4.BeautifulSoup: The BeautifoulSoup object.
#     """

#     # Try to read data from URL, if it fails, return None
#     try:
#         session = requests.Session()
#         session.headers["User-Agent"] = header["User-Agent"]
#         session.headers["Accept-Language"] = header["Language"]
#         session.headers["Content-Language"] = header["Language"]
#         html = session.get(url)
#         return bs(html.text, "html.parser")
#     except:
#         print(f"ERROR: Unable to retrieve data from {url}")
#         return None

soup = BeautifulSoup(r.content, 'html.parser')
# week = soup.find(id="wob_dp")
# items= soup.find_all("div", class_="wob_df")

# temp = soup.find("span", id="wob_tm")

print(soup)
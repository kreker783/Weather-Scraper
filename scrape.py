import requests
import pandas as pd
from bs4 import BeautifulSoup
import pprint
import re


HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept-Language": "en-US,en;q=0.5",
}

def _get_soup(header, city):
    
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": header["User-Agent"],
            "Accept-Language": header["Accept-Language"]
        })

        url = f"https://www.google.com/search?q=weather+{city}&hl=en"
        html = session.get(url)
        return BeautifulSoup(html.text, "html.parser")
    except:
        print(f"ERROR: Unable to retrieve data from {url}")
        return None
    
def get_todays_forecast(soup):
    
    temp = soup.find(id="wob_tm").get_text()
    con = soup.find(id="wob_dc").get_text()
    rain_chance = soup.find(id="wob_pp").get_text()
    wind = soup.find(id="wob_ws").get_text()

    result = {
        "Today": {
            "temperature": temp,
            "condition": con,
            "rain_chance": rain_chance,
            "wind": wind
        }
    } 
    
    return result

def get_week_forecast(soup):
    
    week = soup.find(id="wob_dp")
    item = week.find_all(class_='wob_df')
    week_forecast = dict()

    for value in item[1:]:
        week_forecast[value.find(class_='Z1VzSb').attrs['aria-label']] = {
            "temperature": value.find(class_='wob_t').get_text(),
            "condition": value.find(class_='YQ4gaf').attrs['alt']
        }
    
    return week_forecast

def convert_conditions(forecast):
    conditions = {
        "Sunny": ["Clear", "Sunny", "Mostly sunny", "Partly sunny"],
        "Cloudy": ["Partly cloudy", "Mostly cloudy", "Cloudy"],
        "Rainy": ["Light rain", "Isolated thunderstorms", "Scattered thunderstorms", 
                  "Rainy but periodically clear", "Thunderstorms and rain", "Scattered showers"],
        "Windy": ["Windy"],
    }


    for day in forecast:
        categorized = False
        for condition in conditions:
            if forecast[day]["condition"] in conditions[condition]:
                forecast[day]["condition"] = condition
                categorized = True
                break
        if not categorized:
            forecast[day]["condition"] = f"Unknown - {forecast[day]['condition']}"
    
    return forecast


def get_weather(city):
    soup = _get_soup(HEADER, city)
    forecast = {**get_todays_forecast(soup), **get_week_forecast(soup)}
    return convert_conditions(forecast)
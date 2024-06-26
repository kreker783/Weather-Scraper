import requests
from bs4 import BeautifulSoup


HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept-Language": "en-US,en;q=0.5",
}

def _get_soup(header, city):
    """
    Retrieves the BeautifulSoup object for the specified city's weather page.

    Args:
        header (dict): The header information for the HTTP request.
        city (str): The name of the city.

    Returns:
        BeautifulSoup: The BeautifulSoup object containing the parsed HTML.

    """
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
    """
    Retrieves the forecast for today from the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

    Returns:
        dict: A dictionary containing the forecast for today.

    """
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
    """
    Retrieves the forecast for the week from the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

    Returns:
        dict: A dictionary containing the forecast for the week.

    """
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
    """
    Converts the weather conditions in the forecast dictionary to a simplified format.

    Args:
        forecast (dict): A dictionary containing the weather forecast data.

    Returns:
        dict: The modified forecast dictionary with simplified weather conditions.

    """
    conditions = {
        "Sunny": ["Clear", "Sunny", "Mostly sunny", "Partly sunny", "Clear with periodic clouds"],
        "Cloudy": ["Partly cloudy", "Mostly cloudy", "Cloudy", "Cloudy with brief rain"],
        "Rainy": ["Light rain", "Isolated thunderstorms", "Scattered thunderstorms", 
                  "Rainy but periodically clear", "Thunderstorms and rain", "Scattered showers", 
                  "Showers", 'Rain', 'Thundershower'],
        "Windy": ["Windy"],
    }

    conditions_signs = {
        "Sunny": '<i class="fa-solid fa-sun"></i>',
        "Cloudy": '<i class="fa-solid fa-cloud-sun"></i>',
        "Rainy": '<i class="fa-solid fa-cloud-sun-rain"></i>',
        "Windy": '<i class="fa-solid fa-wind"></i>',
    }

    conditions_image = {
        "Sunny": 'clear-sky.jpg',
        "Cloudy": 'cloudy.jpg',
        "Rainy": 'rainy.jpg',
        "Windy": 'windy.jpg',
    }

    for day in forecast:
        categorized = False
        for condition in conditions:
            if forecast[day]["condition"] in conditions[condition]:
                forecast[day]["condition"] = condition
                forecast[day]["condition_sign"] = conditions_signs[condition] 
                forecast[day]["condition_image"] = conditions_image[condition]
                categorized = True
                break
        if not categorized:
            forecast[day]["condition"] = f"Unknown - {forecast[day]['condition']}"
    
    return forecast


def get_weather(city):
    """
    Retrieves the weather forecast for the specified city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: A dictionary containing the weather forecast.

    """
    soup = _get_soup(HEADER, city)
    try:
        forecast = {**get_todays_forecast(soup), **get_week_forecast(soup)}
    except:
        print(f"ERROR: Unable to retrieve data for {city}")
        return None
    return convert_conditions(forecast)
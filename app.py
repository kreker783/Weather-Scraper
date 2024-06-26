from flask import Flask, render_template, request
import json
import requests
from scrape import get_weather

app = Flask(__name__)

@app.route('/')
def weather_scrapper(message=""):
    """
    This function handles the root route of the Flask application.
    It retrieves the user's IP address, gets the city information from the IP address,
    and then calls the get_weather function to fetch the weather forecast for the city.
    Finally, it renders the index.html template with the forecast, city, and error message (if any).
    """
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    url = f"https://ipinfo.io/{ip}/json"
    r = requests.get(url)
    j = json.loads(r.text)
    city = j['city']
    forecast = get_weather(city)
    return render_template('index.html', forecast=forecast, city=city, error=message)

@app.route('/', methods=['POST'])
def get_city():
    """
    This function handles the POST request to the root route of the Flask application.
    It retrieves the city name from the form data, calls the get_weather function to fetch the weather forecast for the city,
    and then renders the index.html template with the forecast and city.
    If the forecast is None, it returns the weather_scrapper function with a "City not found" message.
    """
    city = request.form['txt']
    forecast = get_weather(city)
    if forecast == None:
        return weather_scrapper(message="City not found")
    return render_template('index.html', forecast=forecast, city=city)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

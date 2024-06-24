from flask import Flask, render_template, request
import scrape
import json
import requests
from scrape import get_weather

app = Flask(__name__)

@app.route('/')
def weather_scrapper(message=""):
    # if request.headers.getlist("X-Forwarded-For"):
    #     ip = request.headers.getlist("X-Forwarded-For")[0]
    # else:
    #     ip = request.remote_addr
    # url = f"https://ipinfo.io/{ip}/json"
    # r = requests.get(url)
    # j = json.loads(r.text)
    # city = j['city']
    city = "Warsaw"
    forecast = get_weather(city)
    return render_template('index.html', forecast=forecast, city=city, error=message)

@app.route('/', methods=['POST'])
def get_city():
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

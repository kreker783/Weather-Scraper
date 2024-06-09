from flask import Flask, render_template, request
import scrape
import json
import requests

app = Flask(__name__)

@app.route('/')
def weather_scrapper():
    ip = request.remote_addr
    url = f"https://ipinfo.io/{ip}/json"
    r = requests.get(url)
    j = json.loads(r.text)

    print(j)
    return render_template('index.html', j=j)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

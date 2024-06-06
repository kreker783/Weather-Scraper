from flask import Flask, render_template
import scrape

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def weather_scrapper():
    forecast = scrape.get_weather('New York')
    print(forecast)
    return render_template('index.html', forecast=forecast)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

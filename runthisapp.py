from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_function
import re

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    return "To scrape, type http://127.0.0.1:5000/scrape"

@app.route("/scraped")
def after_scrape():
    mars_database = mongo.db.mars_database.find_one()
    return render_template('index8.html', mars_database=mars_database)
    
    



@app.route("/scrape")
def scraper():
    mars = mongo.db.mars_database
    mars_data = scrape_function.scrape_everything()
    mars.update({}, mars_data, upsert=True)
    return "http://127.0.0.1:5000/scraped"




if __name__ == "__main__":
    app.run(debug=True)


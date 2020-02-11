from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():    

# Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.mars_db
    collection = db.articles

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    try:
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find_all('body')
        for result in results:
    # scrape the article header 
            news_title = result.find('div', class_='content_title').text
            news_p = result.find('div', class_='article_teaser_body').text
    except: 
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(2)

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find_all('body')
        for result in results:
    # scrape the article header 
            news_title = result.find('div', class_='content_title').text
            news_p = result.find('div', class_='article_teaser_body').text
    



    print (news_title)
    print (news_p)

    new_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(new_url)

    html_2 = browser.html
    soup = BeautifulSoup(html_2, "html.parser")
    results_2 = soup.find_all('body')
    for res in results_2:
        img_url = res.find('a', class_='button fancybox')['data-fancybox-href']
        print (img_url)


    x = (new_url.split ("spaceimages/?search=&category=Mars"))[0]
    actual_url = x + img_url
    print (actual_url)
    browser.visit(actual_url)
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    html_3 = browser.html
    soup = BeautifulSoup(html_3, "html.parser")
    results_3 = soup.find_all('body')
    for r in results_3:
        tweet = r.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    splitted = tweet.split("\n")
    split2 = splitted [2].split("pic.twitter.com/")
    weather_tweet = splitted [0] + " " + splitted [1] + " " +  split2 [0]
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    #html_1 = tables [0].to_html()
    #tables [0].to_html("mars.html")
    #html_2 = tables [1].to_html()
    #tables [1].to_html("mars2.html")
    #hempispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #browser.visit(hempispheres_url)
    #hemispheres = [
    #{"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    #{"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    #{"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    #{"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    #]



    return render_template("index8.html", news_title=news_title, news_p=news_p, actual_url=actual_url)

if __name__ == "__main__":
    app.run(debug=True)


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import urllib.request
import datetime as dt
import time
import pandas as pd
import re

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_database
collection = db.articles

def scrape_everything():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('body')
    for result in results:
    # scrape the article header 
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text
        print (news_title,news_p)
    new_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(new_url)
    html_2 = browser.html
    soup = BeautifulSoup(html_2, "html.parser")
    results_2 = soup.find_all('body')
    for res in results_2:
        img_url = res.find('a', class_='button fancybox')['data-fancybox-href']
    x = (new_url.split ("spaceimages/?search=&category=Mars"))[0]
    actual_url = x + img_url
    print(actual_url)
    browser.visit(actual_url)
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    time.sleep(3)
    #html_3 = browser.html
    #soup = BeautifulSoup(html_3, "html.parser")
    #results_3 = soup.find_all('body')
    #results2 = soup.body.findAll(text=re.compile('InSight sol'), limit=1)
    #weather_tweet = results2[0]
  
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    new_df = tables [0]
    new_df = new_df.rename(columns={0: "Fact", 1: "Stat"})
    html_1 = new_df.to_html(classes="table table-striped")
    new_df.to_html("mars.html")
    html_2 = tables [1].to_html(classes="table table-striped")
    tables [1].to_html("mars2.html")
    hempispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hempispheres_url)
    html_4 = browser.html
    h_soup = BeautifulSoup(html_4, "html.parser")
    new_list = []
    for ana in h_soup.findAll('a', class_= 'itemLink product-item'):
        if ana.parent.name == 'div':
            new_list.append(ana["href"])
    evens = new_list[1::2]
    h_urls = []
    new_url = hempispheres_url.split("/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")[0]
    for eve in evens:
        h_urls.append (new_url + eve)
    images = []
    titles = []
    for hur in h_urls:
        browser.visit(hur)
        html_5 = browser.html
        h_soup = BeautifulSoup(html_5, "html.parser")
        picture_link = h_soup.find('a',href=True,text="Sample").get('href')
        title = h_soup.find("h2", class_="title").get_text()
        title = title.split("Enhanced")[0]
        images.append(picture_link)
        titles.append(title)
    hemisphere = {
    "title": titles,
    "img_url": images
    }
    time_now = time.strftime('%A %b %d, %Y at %I:%M %p')
    
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url": actual_url,
        "hemispheres": hemisphere,
        "mars_facts": html_1,
        "time_scraped": time_now
    }

    browser.quit()


    return mars_data



# In[2]:


#scrape_everything()


# In[ ]:





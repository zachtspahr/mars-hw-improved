from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import re
import json
import json
from bson import ObjectId
from flask import Flask
from flask_pymongo import pymongo
import os 
import requests
from os import environ
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

#from "/Users/zspahr/Desktop/Bootcamp/config.py" import mongo

# Heroku check
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True

if is_heroku == False:
    from config import username, mot_de_passe
else:
   
    username = os.environ.get('username')
    mot_de_passe = os.environ.get('mot_de_passe')

#username = " "
#mot_de_passe =" "

zek_app = Flask(__name__)

CONNECTION_STRING = f'mongodb+srv://{username}:{mot_de_passe}@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('geojsons')
user_collection = pymongo.collection.Collection(db, 'test_collection')

class JSONEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)





@zek_app.route("/")
def index():
    return render_template('home_page.html')

@zek_app.route("/state_maps_api")
def api_senate_maps_endpoint():
    senate_map = db.senate_maps.find_one()
    return (JSONEncoder().encode(senate_map))


@zek_app.route("/senate_info_api")
def api_senate_info_endpoint():

    #This requests scores from 538
    response =requests.get("https://projects.fivethirtyeight.com/biden-congress-votes/")
    soup = BeautifulSoup(response.text, "html.parser")
    last_name = []
    results = soup.find_all("div",class_="last")
    for i in range(len(results)):
        last_name.append(results[i].text)
    margin = []
    results2 = soup.find_all("td",class_="margin")
    for i in range(len(results2)):
        margin.append(float(results2[i].text))
    state = []
    results3 = soup.find_all("td",class_="state")
    for i in range(len(results3)):
        state.append(results3[i].text)
    biden_score = []
    results4 = soup.find_all("td",class_="score")
    for i in range(len(results4)):
        biden_score.append(float(results4[i].text.split("%")[0]))
    biden_plus_minus = []
    results5 = soup.find_all("text",class_="bg")
    for i in range(len(results5)):
        biden_plus_minus.append(float(results5[i].text))
    #creates df for biden scores
    biden_score_dict = {
        "last_name": last_name,
        "state": state,
        "Biden_margin"  : margin,
        "Biden_score"  : biden_score,
        "Biden_plus_minus": biden_plus_minus}
    biden_score_df = pd.DataFrame(biden_score_dict)
    biden_score_df= biden_score_df.sort_values(by=['state',"last_name"])
    biden_score_df=biden_score_df.reset_index()
    biden_score_df.loc[63,"last_name"]="Lujan"
    biden_score_df["merge_id"]= biden_score_df["last_name"]+"-"+ biden_score_df["state"]
    biden_score_df= biden_score_df.drop(columns=['index',"last_name","state"])
    #merges this df with previous senate data
    new_senate_df= pd.read_csv("https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/senate_old_info.csv")
    new_senate_df= new_senate_df.drop(columns=["Unnamed: 0"])
    new_senate_df = new_senate_df.merge(biden_score_df)
    junior_sen = new_senate_df[new_senate_df['Ranking']=='junior']
    junior_sen=junior_sen.fillna(0)
    senior_sen = new_senate_df[new_senate_df['Ranking']=='senior']
    senior_sen=senior_sen.fillna(0)
    new_states_data = db.senate_2021_data.find_one()
    for i in range(len(new_states_data["features"])):
        new_states_data["features"][i]["properties"]["Junior_Senator"].update({"Biden_Score" : junior_sen["Biden_score"].values.tolist()[i],
                                                                            "Biden_plus_minus":junior_sen["Biden_plus_minus"].values.tolist()[i]
                                                                           })
        new_states_data["features"][i]["properties"]["Senior_Senator"].update({"Biden_Score" : senior_sen["Biden_score"].values.tolist()[i],
                                                                           "Biden_plus_minus":senior_sen["Biden_plus_minus"].values.tolist()[i]})

    return (JSONEncoder().encode(new_states_data))




@zek_app.route("/president_senate_api")
def president_senate_maps_endpoint():
    new_states_data2 = db.senate_2021_data.find_one()
    return (JSONEncoder().encode(new_states_data2))


@zek_app.route("/president_dc_api")
def dc_senate_maps_endpoint():
    dc_map = db.president_dc_maps.find_one()
    return (JSONEncoder().encode(dc_map))
@zek_app.route("/house_maps_api")
def api_house_maps_endpoint():
    house_map = db.house_maps.find_one()
    return (JSONEncoder().encode(house_map))

@zek_app.route("/states_api")
def api_senate_endpoint():
    states_data = db.states_data.find_one()
    return (JSONEncoder().encode(states_data))

@zek_app.route("/house_api")
def api_house_endpoint():
    house_data = db.house_districts.find_one()
    return (JSONEncoder().encode(house_data))

@zek_app.route("/president_map")
def api_senate_map():
    return render_template('president_maps2.html')
@zek_app.route("/president_map_2")
def api_senate_map2():
    return render_template('president_maps2.html')

@zek_app.route("/house_map")
def api_house_map():
    return render_template('house_maps.html')
@zek_app.route("/house_map2")
def api_house_map2():
    return render_template('house_maps2.html')
@zek_app.route("/house_districts_demographics")
def api_house_map_new():
    return render_template('house_maps_demographics.html')
@zek_app.route("/senate_maps")
def senate_maps_info():
    return render_template('senate_maps.html')

@zek_app.route("/president_cd_maps")
def api_president_cd_map():
    return render_template('president_cd_maps.html')

@zek_app.route("/house_pop_maps")
def api_house_pop_vote_map():
    return render_template('house_pop_vote_maps.html')

@zek_app.route("/test")
def insert():
    #db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == "__main__":
    zek_app.run(debug=True)



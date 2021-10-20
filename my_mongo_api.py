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
    return render_template('index.html')

@zek_app.route("/state_maps_api")
def api_senate_maps_endpoint():
    senate_map = db.senate_maps.find_one()
    return (JSONEncoder().encode(senate_map))
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
    return render_template('president_maps.html')
@zek_app.route("/president_map_2")
def api_senate_map2():
    return render_template('president_maps2.html')

@zek_app.route("/house_map")
def api_house_map():
    return render_template('house_maps.html')
@zek_app.route("/house_map2")
def api_house_map2():
    return render_template('house_maps2.html')
@zek_app.route("/house_map_new")
def api_house_map_new():
    return render_template('house_maps_no_dropdown.html')

@zek_app.route("/president_cd_maps")
def api_president_cd_map():
    return render_template('president_cd_maps.html')

@zek_app.route("/test")
def insert():
    #db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == "__main__":
    zek_app.run(debug=True)


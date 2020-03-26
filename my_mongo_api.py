from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import re
import json
import json
from bson import ObjectId
from flask import Flask
from flask_pymongo import pymongo

app = Flask(__name__)

CONNECTION_STRING = "mongodb+srv://zachtspahr:capsfan15@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('geojsons')
user_collection = pymongo.collection.Collection(db, 'test_collection')

class JSONEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



#app.config["MONGO_URI"] = "mongodb+srv://zachtspahr:capsfan15@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority"
#mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/senate_api")
def api_senate_endpoint():
    senate_map = db.senate_map.find_one()
    return (JSONEncoder().encode(senate_map))
@app.route("/house_api")
def api_house_endpoint():
    house_map = db.house_maps.find_one()
    return (JSONEncoder().encode(house_map))

@app.route("/president_map")
def api_senate_map():
    return render_template('president_maps.html')

@app.route("/house_map")
def api_house_map():
    return render_template('house_maps.html')

@app.route("/test")
def insert():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == "__main__":
    app.run(debug=True)


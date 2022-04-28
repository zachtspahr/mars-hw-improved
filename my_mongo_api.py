from flask import Flask, render_template, jsonify, url_for, request, redirect
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
import urllib.request
import math
import numpy as np
from patsy import dmatrices
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import random
from random import randrange

#from "/Users/zspahr/Desktop/Bootcamp/config.py" import mongo minor change

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




def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

@zek_app.route("/")
def index():
    return render_template('home_page.html')

@zek_app.route("/formula_1")
def formula_1():
    return render_template('formula_1_page.html')



@zek_app.route("/US_politics_writing")
def other_politics():
    return render_template('other_thoughts_page.html')

@zek_app.route("/other_thoughts")
def other_thoughts():
    return render_template('other_thoughts_page_copy.html')

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

@zek_app.route("/cds_model_president")
def good_ole_data():
    some_data = pd.read_csv("https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/models_edited_president.csv")
    return some_data.to_html()

@zek_app.route('/choose_regression', methods=['GET', 'POST'])
def regression_output():
  selected_variables = "zek"
  if request.method == 'POST':
    form = request.form
    dadumle = pd.DataFrame()
    selected_variables = var_list(form)
    #table = vif_tables(dadumle)
    #print(variance_factor)
    return render_template('index.html',selected_variables = selected_variables)
    #return redirect(url_for('success',name = user))
  else:
    selected_variables=("","","","","","","","","","","","","","","","","","","","","","","","")
    return render_template('index.html',selected_variables = selected_variables)
def var_list(form):
  #fix exceptions here
  reg_vars = []  
  cook_pvi = request.form['2018_Cook_PVI_Score']
  white_ba = request.form["white_ba_pct_pop"]
  white_no_ba = request.form['white_non_college_pct_pop']
  black_pct = request.form['black_pct_pop']
  asian_pct = request.form['asian_pct_pop']
  white_pct = request.form['white_pct_pop']
  hispanic_pct = request.form['hispanic_pct_pop']
  other_race_pct = request.form['other_race_pct_pop']
  black_ba = request.form['black_ba_pct_dis']
  black_no_ba = request.form['black_non_college_pct_dis']
  hispanic_ba  = request.form['hispanic_ba_pct_pop']
  hispanic_no_ba = request.form['hispanic_non_college_pct_pop']
  asian_ba = request.form['asian_ba_pct_pop']
  asian_no_ba = request.form['asian_non_college_pct_pop']
  city_lab = request.form['City_Lab_Congressional_Index_Pure rural']

  if cook_pvi=="0":
      print("cook pvi not checked")
  else:
        reg_vars.append(cook_pvi)
  
  if white_no_ba=="0":
      print("white_no_ba not checked")
  else:
        reg_vars.append(white_no_ba)
  
  if white_ba=="0":
      print("white_ba not checked")
  else:
        reg_vars.append(white_ba)
  if black_no_ba=="0":
      print("black_no_ba not checked")
  else:
        reg_vars.append(black_no_ba)
  
  if black_ba=="0":
      print("black_ba not checked")
  else:
        reg_vars.append(black_ba)
    
  if hispanic_no_ba=="0":
      print("hispanic_no_ba not checked")
  else:
        reg_vars.append(hispanic_no_ba)
  
  if hispanic_ba=="0":
      print("hispanic_ba not checked")
  else:
        reg_vars.append(hispanic_ba)

  if asian_no_ba=="0":
      print("asian_no_ba not checked")
  else:
        reg_vars.append(asian_no_ba)
  
  if asian_ba=="0":
      print("asian_ba not checked")
  else:
        reg_vars.append(asian_ba)

  if white_pct=="0":
      print("white_pct not checked")
  else:
        reg_vars.append(white_pct)

  if black_pct=="0":
      print("black_pct not checked")
  else:
        reg_vars.append(black_pct)
  
  if hispanic_pct=="0":
      print("hispanic_pct not checked")
  else:
        reg_vars.append(hispanic_pct)
    
  if asian_pct=="0":
      print("asian_pct not checked")
  else:
        reg_vars.append(asian_pct)
        
  if other_race_pct=="0":
      print("other_race_pct not checked")
  else:
        reg_vars.append(other_race_pct)
  
  if city_lab=="0":
      print("city_lab not checked")
  else:
        reg_vars.append("City_Lab_Congressional_Index_Dense suburban")
        reg_vars.append("City_Lab_Congressional_Index_Pure urban")
        reg_vars.append("City_Lab_Congressional_Index_Rural-suburban mix")
        reg_vars.append("City_Lab_Congressional_Index_Sparse suburban")
        reg_vars.append("City_Lab_Congressional_Index_Urban-suburban mix")
  letters =""
  for i in range(5):
    randomUpperLetter = chr(random.randint(ord('A'), ord('Z')))
    letters= letters= letters + randomUpperLetter
  numbers = randrange(0, 10000000)
  new_id= f'{letters}{numbers}'
  vars_dict = {'_id':new_id,
      "selected_variables":reg_vars}
  print(vars_dict)
  CONNECTION_STRING = f'mongodb+srv://{username}:{mot_de_passe}@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority'
  print(username)
  client = pymongo.MongoClient(CONNECTION_STRING)
  #print(username)
  db = client.get_database('geojsons')
  #db.user_variables.delete_many({})
  user_variables = db.regression_variables.find()    
  db.user_variables.insert_one(vars_dict)

 
  # Note that I need to make some checks here to make sure number of variables is computed and avoid errors
  # with exceptions   Issues are if no variables are selected for everything and 1 variable selected for vifs
  
  
  recent_variables = reg_vars
  print(len(recent_variables))

  some_data = pd.read_csv("https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/models_edited_president.csv")
  if len(recent_variables)==0:
      reg_variables=("No variables selected","No variables selected",
      "No variables selected","","","","","","","","","","","","")
      print("no variables selected")
  elif len(recent_variables)==1:
      vif_list=[]
      vif_list.append(None) 
      vif_list.append(None)
      X = some_data[recent_variables]
      y = some_data["Biden_Vote"]
      Z= some_data["Trump_Vote_20"]
      zek = some_data["Biden_margin"]
      X2 = sm.add_constant(X)
      est = sm.OLS(y, X2)
      est2 = est.fit()
      est2_html = est2.summary().as_html()
      est3 = sm.OLS(Z, X2)
      est4= est3.fit()
      est4_html = est4.summary().as_html()
      est5 = sm.OLS(zek, X2)
      est6= est5.fit()
      est6_html = est6.summary().as_html()
      columns=['Variables','Coefficients','Standard Error',"T Stat","P-Value","Lower 95%","Upper 95%"]

      bob = pd.read_html(est2.summary().tables[1].as_html())[0]
      bob = bob.rename(columns={0: columns[0], 1: columns[1],2: columns[2], 3: columns[3],4: columns[4], 5: columns[5],
                   6:columns[6]})
      bob = bob.iloc[1:,:]
      bob["Variance Inflation Factor"]=vif_list
      bob["P-Value"]=bob["P-Value"].astype(float)
      bob["Variance Inflation Factor"]=bob["Variance Inflation Factor"].astype(float)
      bob.loc[bob['P-Value'] <= .05, 'Significant?'] = 'Yes' 
      bob.loc[bob['P-Value'] > .05, 'Significant?'] = 'No'
      bob.loc[bob['Variance Inflation Factor'] <= 5, 'Covariance Problem?'] = 'No' 
      bob.loc[bob['Variance Inflation Factor'] > 5, 'Covariance Problem?'] = 'Yes'
      bob = bob.to_html()

      bob2 = pd.read_html(est4.summary().tables[1].as_html())[0]
      bob2 = bob2.rename(columns={0: columns[0], 1: columns[1],2: columns[2], 3: columns[3],4: columns[4], 5: columns[5],
                   6:columns[6]})
      bob2 = bob2.iloc[1:,:]
      bob2["Variance Inflation Factor"]=vif_list
      bob2["P-Value"]=bob2["P-Value"].astype(float)
      bob2["Variance Inflation Factor"]=bob2["Variance Inflation Factor"].astype(float)
      bob2.loc[bob2['P-Value'] <= .05, 'Significant?'] = 'Yes' 
      bob2.loc[bob2['P-Value'] > .05, 'Significant?'] = 'No'
      bob2.loc[bob2['Variance Inflation Factor'] <= 5, 'Covariance Problem?'] = 'No' 
      bob2.loc[bob2['Variance Inflation Factor'] > 5, 'Covariance Problem?'] = 'Yes'
      bob2 = bob2.to_html()

      bob3 = pd.read_html(est6.summary().tables[1].as_html())[0]
      bob3 = bob3.rename(columns={0: columns[0], 1: columns[1],2: columns[2], 3: columns[3],4: columns[4], 5: columns[5],
                   6:columns[6]})
      bob3 = bob3.iloc[1:,:]
      bob3["Variance Inflation Factor"]=vif_list
      bob3["P-Value"]=bob3["P-Value"].astype(float)
      bob3["Variance Inflation Factor"]=bob3["Variance Inflation Factor"].astype(float)
      bob3.loc[bob3['P-Value'] <= .05, 'Significant?'] = 'Yes' 
      bob3.loc[bob3['P-Value'] > .05, 'Significant?'] = 'No'
      bob3.loc[bob3['Variance Inflation Factor'] <= 5, 'Covariance Problem?'] = 'No' 
      bob3.loc[bob3['Variance Inflation Factor'] > 5, 'Covariance Problem?'] = 'Yes'
      bob3 = bob3.to_html()
      params_df = pd.DataFrame(est2.params).reset_index()
      params_df2 = pd.DataFrame(est4.params).reset_index()
      params_df3 = pd.DataFrame(est6.params).reset_index()
      constant =truncate(params_df.iloc[0,1],3)
      constant2 = truncate(params_df2.iloc[0,1],3)
      constant3 = truncate(params_df3.iloc[0,1],3)
      rsq1= truncate(est2.rsquared,3)
      rsq2= truncate(est4.rsquared,3)
      rsq3= truncate(est6.rsquared,3)
      zek=f"{constant}"
      zek2 = f"{constant2}"
      zek3=f"{constant3}" 
      for i in range(len(params_df["index"].tolist())-1):
          zek= zek + f' + {params_df.loc[i+1,0].round(2)} * {params_df.loc[i+1,"index"]}'
          zek2= zek2 + f' + {params_df2.loc[i+1,0].round(2)} * {params_df2.loc[i+1,"index"]}'
          zek3= zek3 + f' + {params_df3.loc[i+1,0].round(2)} * {params_df3.loc[i+1,"index"]}'
      f_pval1 = truncate(est2.f_pvalue,3)
      if f_pval1 <=0.05:
          model_sig1 = "Overall Model is Signficant"
      else:
          model_sig1= "Overall Model is not significant"
      f_pval2 = truncate(est4.f_pvalue,3)
      if f_pval2 <=0.05:
          model_sig2 = "Overall Model is Signficant"
      else:
          model_sig2= "Overall Model is not significant"
      f_pval3 =truncate(est6.f_pvalue,3)
      if f_pval3 <=0.05:
          model_sig3 = "Overall Model is Signficant"
      else:
          model_sig3= "Overall Model is not significant"
      reg_variables=(bob,bob2,bob3,zek,zek2,zek3,rsq1,rsq2,rsq3,f_pval1, f_pval2, f_pval3,model_sig1,
      model_sig2,model_sig3)
      print("Only One Variable Selected")
  else:
      print("Multiple variables selected")
      X = some_data[recent_variables]
      vif = pd.DataFrame()
      vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
      vif["features"] = X.columns
      vif_dict = {"vifs":vif.to_dict(orient="records")}
      vifs = db.vif_tables.find()    
      db.vifs.insert_one(vif_dict)
      vif_list=[]
      vif_list.append(None)
      for new_vif in vif.iloc[:,0].to_list():
          vif_list.append(new_vif)
      X = some_data[recent_variables]
      y = some_data["Biden_Vote"]
      Z= some_data["Trump_Vote_20"]
      zek = some_data["Biden_margin"]
      X2 = sm.add_constant(X)
      est = sm.OLS(y, X2)
      est2 = est.fit()
      est2_html = est2.summary().as_html()
      est3 = sm.OLS(Z, X2)
      est4= est3.fit()
      est4_html = est4.summary().as_html()
      est5 = sm.OLS(zek, X2)
      est6= est5.fit()
      est6_html = est6.summary().as_html()
      columns=['Variables','Coefficients','Standard Error',"T Stat","P-Value","Lower 95%","Upper 95%"]

      bob = pd.read_html(est2.summary().tables[1].as_html())[0]
      bob = bob.rename(columns={0: columns[0], 1: columns[1],2: columns[2], 3: columns[3],4: columns[4], 5: columns[5],
                   6:columns[6]})
      bob = bob.iloc[1:,:]
      bob["Variance Inflation Factor"]=vif_list
      bob["P-Value"]=bob["P-Value"].astype(float)
      bob["Variance Inflation Factor"]=bob["Variance Inflation Factor"].astype(float)
      bob.loc[bob['P-Value'] <= .05, 'Significant?'] = 'Yes' 
      bob.loc[bob['P-Value'] > .05, 'Significant?'] = 'No'
      bob.loc[bob['Variance Inflation Factor'] <= 5, 'Covariance Problem?'] = 'No' 
      bob.loc[bob['Variance Inflation Factor'] > 5, 'Covariance Problem?'] = 'Yes'
      bob = bob.to_html()

      bob2 = pd.read_html(est4.summary().tables[1].as_html())[0]
      bob2 = bob2.rename(columns={0: columns[0], 1: columns[1],2: columns[2], 3: columns[3],4: columns[4], 5: columns[5],
                   6:columns[6]})
      bob2 = bob2.iloc[1:,:]
      bob2["Variance Inflation Factor"]=vif_list
      bob2["P-Value"]=bob2["P-Value"].astype(float)
      bob2["Variance Inflation Factor"]=bob2["Variance Inflation Factor"].astype(float)
      bob2.loc[bob2['P-Value'] <= .05, 'Significant?'] = 'Yes' 
      bob2.loc[bob2['P-Value'] > .05, 'Significant?'] = 'No'
      bob2.loc[bob2['Variance Inflation Factor'] <= 5, 'Covariance Problem?'] = 'No' 
      bob2.loc[bob2['Variance Inflation Factor'] > 5, 'Covariance Problem?'] = 'Yes'
      bob2 = bob2.to_html()

      bob3 = pd.read_html(est6.summary().tables[1].as_html())[0]
      bob3 = bob3.rename(columns={0: columns[0], 1: columns[1],2: columns[2], 3: columns[3],4: columns[4], 5: columns[5],
                   6:columns[6]})
      bob3 = bob3.iloc[1:,:]
      bob3["Variance Inflation Factor"]=vif_list
      bob3["P-Value"]=bob3["P-Value"].astype(float)
      bob3["Variance Inflation Factor"]=bob3["Variance Inflation Factor"].astype(float)
      bob3.loc[bob3['P-Value'] <= .05, 'Significant?'] = 'Yes' 
      bob3.loc[bob3['P-Value'] > .05, 'Significant?'] = 'No'
      bob3.loc[bob3['Variance Inflation Factor'] <= 5, 'Covariance Problem?'] = 'No' 
      bob3.loc[bob3['Variance Inflation Factor'] > 5, 'Covariance Problem?'] = 'Yes'
      bob3 = bob3.to_html()

      params_df = pd.DataFrame(est2.params).reset_index()
      params_df2 = pd.DataFrame(est4.params).reset_index()
      params_df3 = pd.DataFrame(est6.params).reset_index()
      constant = truncate(params_df.iloc[0,1],3)
      constant2 = truncate(params_df2.iloc[0,1],3)
      constant3 = truncate(params_df3.iloc[0,1],3)
      rsq1= truncate(est2.rsquared,3)
      rsq2= truncate(est4.rsquared,3)
      rsq3= truncate(est6.rsquared,3)
      zek=f"{constant}"
      zek2 = f"{constant2}"
      zek3=f"{constant3}" 
      for i in range(len(params_df["index"].tolist())-1):
          zek= zek + f' + {params_df.loc[i+1,0].round(2)} * {params_df.loc[i+1,"index"]}'
          zek2= zek2 + f' + {params_df2.loc[i+1,0].round(2)} * {params_df2.loc[i+1,"index"]}'
          zek3= zek3 + f' + {params_df3.loc[i+1,0].round(2)} * {params_df3.loc[i+1,"index"]}'
      f_pval1 = truncate(est2.f_pvalue,3)
      if f_pval1 <=0.05:
          model_sig1 = "Overall Model is Signficant"
      else:
          model_sig1= "Overall Model is not significant"
      f_pval2 = truncate(est4.f_pvalue,3)
      if f_pval2 <=0.05:
          model_sig2 = "Overall Model is Signficant"
      else:
          model_sig2= "Overall Model is not significant"
      f_pval3 =truncate(est6.f_pvalue,3)
      if f_pval3 <=0.05:
          model_sig3 = "Overall Model is Signficant"
      else:
          model_sig3= "Overall Model is not significant"
      reg_variables=(bob,bob2,bob3,zek,zek2,zek3,rsq1,rsq2,rsq3,f_pval1, f_pval2, f_pval3,model_sig1,
      model_sig2,model_sig3)
  # this is tuple with 3 data frames and 3 equations, 3 r squared value

  return (reg_variables)

def vif_tables(dadumle):
    #fix exceptions here

    CONNECTION_STRING = f'mongodb+srv://{username}:{mot_de_passe}@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority'
    print(username)
    client = pymongo.MongoClient(CONNECTION_STRING)
    #print(username)
    db = client.get_database('geojsons')

    vifs_dict={"vifs":[]}
    vifs = db.vifs.find()
    for item in vifs:
        vifs_dict["vifs"].append(item["vifs"])
    zek = len(vifs_dict["vifs"])-1

    vifs_df = pd.DataFrame(vifs_dict["vifs"][zek]).to_html()
    return vifs_df

@zek_app.route("/most_recent_selected_data")
def user_selected_data():
    #fix exceptions here
    user_data = db.user_variables.find()
    user_dict = {"variables":[]}

    user_dict ["variables"]
    for item in user_data:
        user_dict["variables"].append(item)
    last_entry = user_dict["variables"][len(user_dict["variables"])-1]
    return (jsonify(last_entry))

@zek_app.route("/map_model_geojson")
#fix exceptions here
def user_input_geojson():
    CONNECTION_STRING = f'mongodb+srv://{username}:{mot_de_passe}@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.get_database('geojsons')
    user_collection = pymongo.collection.Collection(db, 'test_collection')


    user_data = db.user_variables.find()
    user_dict = {"variables":[]}

    user_dict ["variables"]
    for item in user_data:
        user_dict["variables"].append(item)
    recent_variables = user_dict["variables"][len(user_dict["variables"])-1]["selected_variables"]
    if len(recent_variables)==0:
        url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"
        response = requests.get(url)
        cd_json = response.json()
    else:
        some_data = pd.read_csv("https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/models_edited_president.csv")
    #some_data[recent_variables]

        X = some_data[recent_variables]
        y = some_data["Biden_Vote"]
        Z= some_data["Trump_Vote_20"]
        zek = some_data["Biden_margin"]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        est3 = sm.OLS(Z, X2)
        est4= est3.fit()
        est5 = sm.OLS(zek, X2)
        est6= est5.fit()

    
   


        coef = pd.DataFrame(est2.params).iloc[:,0].tolist()
        new_df = X
        biden_expected_vote = []
        constant = coef[0]
        for i in range(len(new_df.iloc[:,0].tolist())):
            zek = constant
            for j in range(len(coef)-1):
                zek = zek + (new_df.iloc[i,j]*coef[j+1])
            biden_expected_vote.append(zek)
    
        trying = pd.DataFrame()
        trying["CD_ID"]= some_data["CD_ID"]
        trying["Biden_Expected_Vote"]= biden_expected_vote
        trying["Biden_Actual_Vote"] = some_data["Biden_Vote"]
        trying["Biden_Residual"]= trying["Biden_Actual_Vote"]-trying["Biden_Expected_Vote"]


        coef2 = pd.DataFrame(est4.params).iloc[:,0].tolist()
        new_df2 = X
        trump_expected_vote = []
        constant2 = coef2[0]
        for k in range(len(new_df2.iloc[:,0].tolist())):
            zek2 = constant2
            for l in range(len(coef2)-1):
                zek2 = zek2 + (new_df2.iloc[k,l]*coef2[l+1])
            trump_expected_vote.append(zek2)
        trying["Trump_Expected_Vote"]= trump_expected_vote
        trying["Trump_Actual_Vote"] = some_data["Trump_Vote_20"]
        trying["Trump_Residual"]= trying["Trump_Actual_Vote"]-trying["Trump_Expected_Vote"]

        coef3 = pd.DataFrame(est6.params).iloc[:,0].tolist()
        new_df3 = X
        biden_predicted_margin = []
        constant3 = coef3[0]
        for w in range(len(new_df3.iloc[:,0].tolist())):
            zek3 = constant3
            for v in range(len(coef3)-1):
                zek3 = zek3 + (new_df3.iloc[w,v]*coef3[v+1])
            biden_predicted_margin.append(zek3)
        trying["Predicted_Biden_Margin"]= biden_predicted_margin
        trying["Actual_Biden_Margin"] = some_data["Biden_margin"]
        trying["Margin_Residual"]= trying["Actual_Biden_Margin"]-trying["Predicted_Biden_Margin"]
        model_list = trying.to_dict(orient="records")
        url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"
        response = requests.get(url)
        cd_json = response.json()
        for i in range(len(cd_json["features"])):
            cd_json["features"][i]["properties"].update(model_list[i])
    return (JSONEncoder().encode(cd_json))

@zek_app.route("/regression_table")
#fix exceptions here
def user_input_table():
    CONNECTION_STRING = f'mongodb+srv://{username}:{mot_de_passe}@cluster0-zgmov.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.get_database('geojsons')
    user_collection = pymongo.collection.Collection(db, 'test_collection')


    user_data = db.user_variables.find()
    user_dict = {"variables":[]}

    user_dict ["variables"]
    for item in user_data:
        user_dict["variables"].append(item)
    recent_variables = user_dict["variables"][len(user_dict["variables"])-1]["selected_variables"]
    if len(recent_variables)==0:
        url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"
        response = requests.get(url)
        cd_json = response.json()
        reg_tables =("No Variables Selected","No Variables Selected","No Variables Selected")
        equations= ["No Variables Selected","No Variables Selected","No Variables Selected"]
        cd_merged = pd.read_csv("https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/models_edited_president.csv").to_html()
        cov_params = ("","","")
    else:


        some_data = pd.read_csv("https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/models_edited_president.csv")
        some_data[recent_variables]

        X = some_data[recent_variables]
        y = some_data["Biden_Vote"]
        Z= some_data["Trump_Vote_20"]
        zek = some_data["Biden_margin"]
        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        est2_html = est2.summary().as_html()
        est3 = sm.OLS(Z, X2)
        est4= est3.fit()
        est4_html = est4.summary().as_html()
        est5 = sm.OLS(zek, X2)
        est6= est5.fit()
        est6_html = est6.summary().as_html()
        reg_tables =(est2_html,est4_html,est6_html)
    
        coef = pd.DataFrame(est2.params).iloc[:,0].tolist()
        new_df = X
        biden_expected_vote = []
        constant = coef[0]
        for i in range(len(new_df.iloc[:,0].tolist())):
            zek = constant
            for j in range(len(coef)-1):
                zek = zek + (new_df.iloc[i,j]*coef[j+1])
            biden_expected_vote.append(zek)
    
        trying = pd.DataFrame()
        trying["CD_ID"]= some_data["CD_ID"]
        trying["Biden_Expected_Vote"]= biden_expected_vote
        trying["Biden_Actual_Vote"] = some_data["Biden_Vote"]
        trying["Biden_Residual"]= trying["Biden_Actual_Vote"]-trying["Biden_Expected_Vote"]


        coef2 = pd.DataFrame(est4.params).iloc[:,0].tolist()
        new_df2 = X
        trump_expected_vote = []
        constant2 = coef2[0]
        for k in range(len(new_df2.iloc[:,0].tolist())):
            zek2 = constant2
            for l in range(len(coef2)-1):
                zek2 = zek2 + (new_df2.iloc[k,l]*coef2[l+1])
            trump_expected_vote.append(zek2)
        trying["Trump_Expected_Vote"]= trump_expected_vote
        trying["Trump_Actual_Vote"] = some_data["Trump_Vote_20"]
        trying["Trump_Residual"]= trying["Trump_Actual_Vote"]-trying["Trump_Expected_Vote"]

        coef3 = pd.DataFrame(est6.params).iloc[:,0].tolist()
        new_df3 = X
        biden_predicted_margin = []
        constant3 = coef3[0]
        for w in range(len(new_df3.iloc[:,0].tolist())):
            zek3 = constant3
            for v in range(len(coef3)-1):
                zek3 = zek3 + (new_df3.iloc[w,v]*coef3[v+1])
            biden_predicted_margin.append(zek3)
        trying["Predicted_Biden_Margin"]= biden_predicted_margin
        trying["Actual_Biden_Margin"] = some_data["Biden_margin"]
        trying["Margin_Residual"]= trying["Actual_Biden_Margin"]-trying["Predicted_Biden_Margin"]
        cd_ids=some_data["CD_ID"].tolist()
        new_df_copy = X.copy()
        for i in range(len(cd_ids)):
            new_df_copy.loc[i,"CD_ID"]= cd_ids[i]
        cd_merged = pd.merge(trying,new_df_copy,on= "CD_ID",sort=False).to_html()

        params_df = pd.DataFrame(est2.params).reset_index() 
        params_df2 = pd.DataFrame(est4.params).reset_index()
        params_df3 = pd.DataFrame(est6.params).reset_index()
        cov_params_df = pd.DataFrame(est2.normalized_cov_params).reset_index() 
        cov_params_df = cov_params_df.rename(columns={"index": "Variables"})
        cov_params_df2 = pd.DataFrame(est4.normalized_cov_params).reset_index() 
        cov_params_d2 = cov_params_df2.rename(columns={"index": "Variables"})
        cov_params_df3 = pd.DataFrame(est6.normalized_cov_params).reset_index() 
        cov_params_df3 = cov_params_df3.rename(columns={"index": "Variables"})
        
        zek=f"{constant}"
        zek2 = f"{constant2}"
        zek3=f"{constant3}" 
        for i in range(len(params_df["index"].tolist())-1):
            zek= zek + f' + {params_df.loc[i+1,0].round(2)} * {params_df.loc[i+1,"index"]}'
            zek2= zek2 + f' + {params_df2.loc[i+1,0].round(2)} * {params_df2.loc[i+1,"index"]}'
            zek3= zek3 + f' + {params_df3.loc[i+1,0].round(2)} * {params_df3.loc[i+1,"index"]}'
    



#params_df
        equations= [zek,zek2,zek3]
        cov_params =(cov_params_df.to_html(),cov_params_df2.to_html(),cov_params_df3.to_html())

    return render_template("big_table_rendering.html",cd_merged = cd_merged,reg_tables=reg_tables,equations=equations,cov_params=cov_params)

if __name__ == "__main__":
    zek_app.run(debug=True)



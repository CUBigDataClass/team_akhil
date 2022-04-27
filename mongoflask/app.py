from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

import pandas as pd
import pickle
import numpy as np
import requests

from food_extractor.food_model import FoodModel

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
model_IL = pickle.load(open('../new_pickles/kmeans_IL.pkl', 'rb'))

db = client['bda_yelp']
df_restaurants = db['yelprestaurants']
df_reviews = db['yelpreviews']

fooditemModel = FoodModel("chambliss/distilbert-for-food-extraction")

latitude = 38.601675
longitude = -89.992291
state = 'IL'

@app.route('/', methods=('GET', 'POST'))
def index():
    global latitude, longitude, state
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    if request.method=='POST':
        location = request.form['location']
        location = location.strip()
        if(location != ''):
            location_detail = {'address':location, 'key':'AIzaSyClROwvuayCE59aN8OXSwJxNF5zGkIRCb4'}
            print(location_detail)
            r = requests.get(url = URL, params = location_detail)
            print("lets gooo")
            print(r.json())
            data = r.json()
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            state = data['results'][0]['formatted_address'][-13:-11]
            formatted_address = data['results'][0]['formatted_address']
        else:
            latitude = "No input given"
            longitude = "No input given"
            formatted_address = "No input given"
        return redirect(url_for('index'))

    #lat = 38.601675
    #lon = -89.992291
    # 67 Ludwig Dr, Fairview Heights, IL 62208
    # clus = model_IL.predict(np.array([latitude,longitude]).reshape(1,-1))[0]
    # print(clus)
    # 'cluster' : clus.item(),
    #     res = []
    best_foods = []
    #all_todos = df_restaurants.find({'state' : state_temp, 'cluster' : clus.item()})
    all_res = df_restaurants.find({
        'state' : state, 
        'loc': {'$near': {
        '$geometry': {
        'type': 'Point' ,
        'coordinates': [ longitude , latitude ]
        },
        }}
        })
    for todo in all_res[0:1]:
        res_id = todo['business_id']
        res_name = todo['name']
        b_food = set()
        #all_5_reviews = df_reviews.find({'business_id' : res_id, 'stars' : 5})
        print("Processing Restaurant...")
        #print(all_5_reviews[0]['text'])
        foodrecs = []
        for r in df_reviews.find({'business_id' : res_id, 'stars' : 5}):
            foodrecs.append(fooditemModel.extract_foods(r['text']))

        #foodrecs = fooditemModel.extract_foods(all_5_reviews_list)
        for i in foodrecs:
            for k in i:    
                for j in k['Ingredient']:
                    if j['conf'] > 0.95:
                        b_food.add(j['text'])
        best_foods.append({res_name : b_food})
        print(best_foods)
    return render_template('index.html', todos=best_foods)

@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


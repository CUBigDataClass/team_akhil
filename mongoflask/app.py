from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

import pandas as pd
import pickle
import numpy as np


from food_extractor.food_model import FoodModel

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
model_IL = pickle.load(open('../new_pickles/kmeans_IL.pkl', 'rb'))

db = client['bda_yelp']
df_restaurants = db['yelprestaurants']
df_reviews = db['yelpreviews']

fooditemModel = FoodModel("chambliss/distilbert-for-food-extraction")

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))

    lat = 38.601675
    lon = -89.992291
    state_temp = 'IL'
    clus = model_IL.predict(np.array([38.601675,-89.992291]).reshape(1,-1))[0]
    print(clus)
    res = []
    best_foods = []
    all_todos = df_restaurants.find({'state' : state_temp, 'cluster' : clus.item()})
    for todo in all_todos[0:5]:
        res_id = todo['business_id']
        res_name = todo['name']
        b_food = []
        #all_5_reviews = df_reviews.find({'business_id' : res_id, 'stars' : 5})
        print("Im here")
        #print(all_5_reviews[0]['text'])
        all_5_reviews_list = []
        for r in df_reviews.find({'business_id' : res_id, 'stars' : 5}):
            all_5_reviews_list.append(r['text'])

        foodrecs = fooditemModel.extract_foods(all_5_reviews_list)
        for i in foodrecs:
            for j in i['Ingredient']:
                if j['conf'] > 0.95:
                    b_food.append(j['text'])
        best_foods.append({res_name : b_food})
        print(best_foods)
    return render_template('index.html', todos=best_foods)

@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


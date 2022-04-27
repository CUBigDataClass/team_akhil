from pymongo import MongoClient
from bson.objectid import ObjectId

import pandas as pd
import pickle
import numpy as np
import requests

from food_extractor.food_model import FoodModel


fooditemModel = FoodModel("chambliss/distilbert-for-food-extraction")
client = MongoClient("mongodb://localhost:27017/")


db = client['bda_yelp']
#df_restaurants = db['yelprestaurants']

df_reviews = db['yelpreviews']
df_reviews_new = db['yelpreviewsNew4']

#all_res = df_restaurants.find({})
all_res = open('4.csv', 'r').readlines()
count = 0
for todo in range(len(all_res)):
    count += 1
    tododo = all_res[todo].split(',')
    res_id = tododo[0]
    res_name = tododo[1]
    latitude = tododo[3]
    longitude = tododo[4]
    
    b_food = set()
        #all_5_reviews = df_reviews.find({'business_id' : res_id, 'stars' : 5})
    print("Processing Restaurant..." + str(count))
    #print(all_5_reviews[0]['text'])
    foodrecs = []
    for r in df_reviews.find({'business_id' : res_id, 'stars' : 5})[1000:5000]:
        foodrecs.append(fooditemModel.extract_foods(r['text']))
    #foodrecs = fooditemModel.extract_foods(all_5_reviews_list)
    flag = 0
    for i in foodrecs:
        for k in i:    
            for j in k['Ingredient']:
                if j['conf'] > 0.95:
                    b_food.add(j['text'])
                    if len(b_food) == 5:
                    	flag = 1
                    	break
            if flag == 1:
            	break
        if flag == 1:
        	break
    record = {
    'business_id' : res_id,
    'name' : res_name,
    'latitude' : latitude,
    'longitude':longitude,
    'best_foods' : list(b_food)
    }
    record_id = df_reviews_new.insert_one(record)
    #best_foods.append({res_name : b_food})
    print(record_id)

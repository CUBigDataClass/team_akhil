# Imports
import pandas as pd
from sqlalchemy import create_engine

# This CSV doesn't have a header so pass
# column names as an argument
columns = ['review_id', 'business_id', 'stars', 'useful', 'funny', 'cool', 'text']

# Instantiate sqlachemy.create_engine object
engine = create_engine('postgresql://team_akhil:team_akhil@localhost:5432/bda_yelp')

# Create an iterable that will read "chunksize=1000" rows
# at a time from the CSV file
for df in pd.read_csv("../../restaurant_reviews.csv",names=columns,chunksize=1000):
  df.to_sql(
    'restaurant_reviews', 
    engine,
    index=False,
    if_exists='append' # if the table already exists, append this data
  )

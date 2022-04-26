# Imports
import pandas as pd
from sqlalchemy import create_engine

# This CSV doesn't have a header so pass
# column names as an argument
columns = ['business_id', 'state', 'latitude', 'longitude', 'stars',
       'review_count', 'cluster']

# Instantiate sqlachemy.create_engine object
engine = create_engine('postgresql://team_akhil:team_akhil@localhost:5432/bda_yelp')

# Create an iterable that will read "chunksize=1000" rows
# at a time from the CSV file
for df in pd.read_csv("restaurant_kmeans.csv",names=columns,chunksize=1000):
  df.to_sql(
    'restaurant_cluster', 
    engine,
    index=False,
    if_exists='append' # if the table already exists, append this data
  )

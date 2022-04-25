import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def add_location(state,latitude, longitude):
  app_tables.locations.add_row(state = state, latitude = latitude, longitude = longitude)
  restaurants = anvil.server.call('add_restaurant', state, latitude, longitude)
  print(restaurants)
  
@anvil.server.callable
def get_restaurants():
  return app_tables.restaurants.search()
  

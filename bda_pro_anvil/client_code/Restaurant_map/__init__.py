from ._anvil_designer import Restaurant_mapTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class Restaurant_map(Restaurant_mapTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    restaurants = anvil.server.call('get_restaurants')
    self.markers = {}
    self.items = {}

    for restaurant in restaurants:
      position = GoogleMap.LatLng(restaurant['latitude'],restaurant['longitude'])
      marker = GoogleMap.Marker(position = position)
      self.map.add_component(marker)
      marker.set_event_handler("click",self.marker_click)
      self.markers[marker] = restaurant['name']
      self.items[marker] = restaurant['items']
      
  def marker_click(self,sender,**event_args):
    i=GoogleMap.InfoWindow(content = Label(text=self.markers[sender]+ " - \n best item is " +self.items[sender]))
    i.open(self.map,sender)
    

  def go_to_form1(self, **event_args):
    app_tables.restaurants.delete_all_rows()
    open_form('Form1')


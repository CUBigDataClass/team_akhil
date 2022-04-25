from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.state = None
    #self.token = "AIzaSyBfvmJwUlwQpzb5chg3S4RPoAPkLKrNafQ"
    # Any code you write here will run when the form opens.
    

  def search_for_location(self, **event_args):
    results = GoogleMap.geocode(address=self.location_name.text)
    self.state = results[0].formatted_address[-13:-11]
    result = results[0].geometry.location
    marker = GoogleMap.Marker(position = result)
    self.map.add_component(marker)
    self.map.center = result
    self.map.zoom = 15
    self.map.visible = True
    self.latitude = result.lat()
    self.longitude = result.lng()
    self.restaurant_search.enabled = True
    
    
  def restaurant_search_click(self, **event_args):
    anvil.server.call('add_location', self.state, self.latitude, self.longitude)
    open_form('Restaurant_map')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.launch_background_task('store_data',file)





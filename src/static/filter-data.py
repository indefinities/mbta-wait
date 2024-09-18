import pandas as pd
from pandas import json_normalize
import json

# read text file into pandas DataFrame
df = pd.read_csv("stops.txt")
data = df[["stop_id", "stop_name", "vehicle_type"]]
stops = data[data["vehicle_type"] == 1]

trips = []

# Open the JSON file and load its contents
with open('trip_updates.json', 'r') as file:
    json_data = json.load(file)

# Access the "entity" key
entity_data = json_data.get('entity', [])

# Process each item in the entity list
for item in entity_data:
    trip_update = item.get('trip_update', {})
    trip = trip_update.get('trip')
    route_id = trip.get('route_id')
    
    stop_time_update = trip_update.get('stop_time_update')
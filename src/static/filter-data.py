import pandas as pd
from pandas import json_normalize
import json

lines = ['Red', 'Green', 'Blue', 'Orange']
nonlines = ['CR', 'Shuttle']

# read text file into pandas DataFrame
df = pd.read_csv("stops.txt")
data = df[["stop_id", "stop_name", "vehicle_type"]]
stops = data[data["vehicle_type"] == 1]

print(stops)

df1 = pd.read_csv("directions.txt")

lpatt = '|'.join(lines)
nlpatt = '|'.join(nonlines)

dir = df1[(df1['route_id'].str.contains(lpatt, case=False, na=False)) & (~df1['route_id'].str.contains(nlpatt, regex=True))]
# Shuttles will be a future iteration
print(dir)

trips = []

# Open the JSON file and load its contents
with open('trip_updates.json', 'r') as file:
    json_data = json.load(file)

# Access the "entity" key
entity = json_data.get('entity', [])

# Process each item in the entity list
# TODO: append entries to trips array as an object
# and match ids with route and direction names
for entry in entity:
    trip_update = entry.get('trip_update', {})
    trip = trip_update.get('trip', {})
    route_id = trip.get('route_id')
    direction_id = trip.get('direction_id')
    stop_time_update = trip_update.get('stop_time_update', [])

    for stop in stop_time_update:
        stop_id = stop.get('stop_id')
        arrival = stop.get('arrival')
        departure = stop.get('departure')
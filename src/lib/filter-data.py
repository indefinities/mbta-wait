import pandas as pd
from pandas import json_normalize
from datetime import datetime
import json

# General MBTA subway lines
line_colors = ['Red', 'Green', 'Blue', 'Orange']
# Other MBTA trains that are not subway lines
nonlines = ['CR', 'Shuttle']

# Read stops text file as csv into pandas dataframe
df = pd.read_csv("data/stops.txt")
data = df[["stop_id", "stop_name", "vehicle_type"]]
# Find a better way to identify if the stop is a subway stop?
stops = data[(data["vehicle_type"] == 1) | (data["vehicle_type"] == 0)]

# Read directions text file as csv into pandas dataframe
df1 = pd.read_csv("data/directions.txt")

# Regex patterns for detecting subway vs non-subway lines
lines_pattern = '|'.join(line_colors)
nonlines_pattern = '|'.join(nonlines)

dir = df1[(df1['route_id'].str.contains(lines_pattern, case=False, na=False)) & (~df1['route_id'].str.contains(nonlines_pattern, regex=True))]
# Shuttles will be a future iteration

# Open the JSON file and load its contents
with open('data/trip_updates.json', 'r') as file:
    json_data = json.load(file)

# Access the "entity" key
entity = json_data.get('entity', [])

trips = list()

# Process each item in the entity list
# and match ids with route and direction names
for entry in entity:
    id = entry.get('id')
    trip_update = entry.get('trip_update', {})
    trip = trip_update.get('trip', {})
    route_id = trip.get('route_id')
    direction_id = trip.get('direction_id')
    start_date = trip.get('start_date')
    start_time = trip.get('start_time')
    stop_time_update = trip_update.get('stop_time_update', [])
    schedule_relationship = trip.get('schedule_relationship', '')
    
    if (schedule_relationship != 'CANCELED') and (route_id in dir['route_id'].values):
        route_name = dir.loc[dir['route_id'] == route_id, 'direction_destination'].values[0]
        direction = dir.loc[dir['direction_id'] == direction_id, 'direction'].values[0]
        route_entry = {
            'id': id,
            'route_id': route_id,
            'route_name': route_name,
            'direction': direction,
            'start_date': start_date,
            'start_time': start_time,
            'schedule': list()
        }

        for stop in stop_time_update:
            # if there's no schedule_relationship cancellation
            if 'schedule_relationship' not in stop:
                stop_id = stop.get('stop_id')
                stop_name = stops.loc[stops['stop_id'] == stop_id, 'stop_name'].values[0]
                start_ms = datetime.strptime(f'{start_date} {start_time}',
                            '%Y%m%d %H:%M:%S').timestamp() * 1000
                arrival = stop.get('arrival', dict(time = start_ms)).get('time', 0)
                departure = stop.get('departure', dict(time = 0)).get('time', 0)
                wait_time = int(departure) - int(arrival) if departure > arrival > 0 else int(start_ms) - int(departure)
                stop_entry = {
                    'stop_name': stop_name,
                    'arrival': arrival,
                    'departure': departure,
                    'wait_time': wait_time if departure > 0 else 0
                }
                route_entry['schedule'].append(stop_entry)

        # Add the route entry to trips once all functions are iterated through
        trips.append(route_entry)

# Change dictionary into json.dumps to export JSONs
colors_obj = json.dumps(dict(colors = line_colors))

with open("data/colors.json", "w") as outfile:
    outfile.write(colors_obj)

trips_obj = json.dumps(dict(trips = trips))

with open("data/filtered_trips.json", "w") as outfile:
    outfile.write(trips_obj)
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

# Check if the route_id follows the regex pattern (if the route_id includes the subway name colors)
dir = df1[(df1['route_id'].str.contains(lines_pattern, case=False, na=False)) & (~df1['route_id'].str.contains(nonlines_pattern, regex=True))]
# Shuttles will be a future iteration

# Open the existing trips JSON file and load its contents
with open('data/trip_updates.json', 'r') as file:
    json_data1 = json.load(file)

# Access the "entity" key
entity = json_data1.get('entity', [])

# Open the new trips JSON file and load its contents
with open('data/new_trip_updates.json', 'r') as file:
    json_data2 = json.load(file)

# Access the "entity" key as "new_entity"
new_entity = json_data2.get('entity', [])

# Combine both entity arrays together using +
all_entity = entity + new_entity;

# Create a new dictionary with the "entity" key as JSON format
all_entity_obj = { "entity": all_entity }

# Turn the dictionary into a str using json/dumps
all_entity_json = json.dumps(all_entity_obj)

# TODO: before exporting this file, cross check with dates.json 
# to remove entries before a week ago
# Export all entities into trip_updates.json
with open("data/trip_updates.json", "w") as outfile:
    outfile.write(all_entity_json)

# Create an empty list to gather all trips as the 
# arr is being iterated through
all_trips = list()
# Process each item in the entity list
# and match ids with route and direction names
for entry in all_entity:
    trip_update = entry.get('trip_update', {})
    trip = trip_update.get('trip', {})
    route_id = trip.get('route_id')
    direction_id = trip.get('direction_id')
    stop_time_update = trip_update.get('stop_time_update', [])
    route_id = trip.get('route_id')
    direction_id = trip.get('direction_id')
    schedule_relationship = trip.get('schedule_relationship', '')

    # if the trip isn't cancelled
    # if the route_id is a subway line in the dir dataframe (all subway routes)
    if (schedule_relationship != 'CANCELED') and (route_id in dir['route_id'].values):
        route_name = dir.loc[dir['route_id'] == route_id, 'direction_destination'].values[0]
        direction = dir.loc[dir['direction_id'] == direction_id, 'direction'].values[0]
        start_date = trip.get('start_date')
        start_time = trip.get('start_time')

        for stop in stop_time_update:
            stop_id = stop.get('stop_id')
            stop_name = stops.loc[stops['stop_id'] == stop_id, 'stop_name'].values[0]
            arrival = stop.get('arrival', dict(time = 0)).get('time', 0)
            departure = stop.get('departure', dict(time = 0)).get('time', 0)
            wait_time = int(departure) - int(arrival) if departure > arrival > 0 else 0
            # Combine route, direction, and stop into one dictionary 
            # For easy use with pandas dataframe
            new_entry = {
                'route_id': route_id,
                'route_name': route_name,
                'direction_id': direction_id,
                'direction': direction,
                'start_date': start_date,
                'start_time': start_time,
                'stop_id': stop_id,
                'stop_name': stop_name,
                'arrival': arrival,
                'departure': departure,
                'wait_time': wait_time
            }
            all_trips.append(new_entry)

# Create a new dataframe from the array of dictionaries 
# (this should be easier because dictionaries are not nested and have same column names)
all_trips_df = pd.DataFrame(all_trips)
all_trips_df['avg_wait_time'] = all_trips_df.groupby(['start_date', 'route_id', 'direction_id', 'stop_id'])['wait_time'].transform('mean')
last_stop_arrivals = all_trips_df.groupby(['start_date', 'route_id', 'direction_id'])['arrival'].transform('max')
first_stop_departures = all_trips_df.groupby(['start_date', 'route_id', 'direction_id'])['departure'].transform(lambda x: x[x>0].min())
all_trips_df['total_trip_time'] = last_stop_arrivals - first_stop_departures
all_trips_df['avg_total_trip_time'] = all_trips_df.groupby(['start_date', 'route_id', 'direction_id'])['total_trip_time'].transform('mean')
grouped_trips = all_trips_df[['route_id', 'route_name', 'direction_id', 'direction', 'start_date', 'avg_total_trip_time', 'stop_name', 'avg_wait_time']].drop_duplicates()
# Initialize an empty dictionary for the JSON structure
grouped_trips_obj = {"trips": []}

with open('data/mbta_lines.json', 'r') as file:
    json_data3 = json.load(file)

# Access the "entity" key
mbta_lines = json_data3.get('lines', [])

def order_subset(subset, superset, dir_id):
    for element in superset:
        if set(subset).issubset(set(element)):
            return order_subset_by_superset(subset, element, dir_id)
    return subset

def order_subset_by_superset(subset, superset, dir_id):
    order = superset.copy()
    if dir_id > 0: order.reverse()
    index_map = {element: i for i, element in enumerate(order)}
    sorted_subset = [element for element in subset if element in index_map]
    result = sorted(sorted_subset, key=lambda x: index_map[x])
    return result

# checks if all avg_wait_times are int32
def change_int(i):
    return dict(stop_name=i['stop_name'], avg_wait_time=int(i['avg_wait_time']))

def sort_stops(dir_id, arr):
    all_stops = [l.get('stops') for l in mbta_lines]
    stop_list = [a.get('stop_name') for a in arr]
    order = order_subset(stop_list, all_stops, dir_id)
    sorted_result = sorted(arr, key=lambda i: order.index(i['stop_name']))
    result_int_wait = map(change_int, sorted_result)
    result = list(result_int_wait)
    return result

# Iterate through the unique combinations of 'route_name', 'direction', and 'start_date'
for (route_id, route_name, direction_id, direction, start_date, avg_total_trip_time), group in grouped_trips.groupby(['route_id', 'route_name', 'direction_id', 'direction', 'start_date', 'avg_total_trip_time']):
    trip = {
        "route_id": route_id,
        "route_name": route_name,
        'direction_id': int(direction_id),
        "direction": direction,
        "start_date": start_date,
        "total_trip_time": int(avg_total_trip_time),
        "stops": sort_stops(direction_id, group[["stop_name", "avg_wait_time"]].to_dict(orient='records'))
    }
    grouped_trips_obj["trips"].append(trip)

# Get the current dates available for the data
curr_dates_df = all_trips_df[['start_date']].drop_duplicates()
curr_dates = curr_dates_df['start_date'].tolist()
curr_dates_json = json.dumps(dict(dates=curr_dates))

with open("data/curr_dates.json", "w") as outfile:
    outfile.write(curr_dates_json)

# Change dictionary into json.dumps to export JSONs
grouped_trips_json = json.dumps(grouped_trips_obj)

with open("data/grouped_trips.json", "w") as outfile:
    outfile.write(grouped_trips_json)
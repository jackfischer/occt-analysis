import json, csv
from geopy.distance import distance

def load_points():
  reader = csv.reader(open("coordinates.csv"), quoting=csv.QUOTE_NONNUMERIC)
  points = [(lat, lng) for i,lat,lng in reader]
  return points

def map_point(s): 
  running_min = float("inf")
  point_index = None #index of closest point on map
  for i, p in enumerate(points):
    dist = distance(p, s).miles
    if dist < running_min:
      running_min = dist
      point_index = i
  return point_index


points = load_points()
f = open("dump1")

#loop through json's here
for line in f:
  doc = json.loads(line)
  shuttles = [] #list of tuples of lat longs
  for v in doc['get_vehicles']:
    # if Campus shuttle, and in service
    if v['routeID'] == 8 and v['scheduleNumber'] != 'NIS': 
      shuttles.append( (v['lat'], v['lng']) )
  
  if len(shuttles) > 1: #more than 1 bus on map right now
    indicies = [map_point(s) for s in shuttles] #map points of buses
    print(indicies)
  
  

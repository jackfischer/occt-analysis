import json, csv, time
from geopy.distance import great_circle as distance
from multiprocessing import Pool

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


def distance_wrapper(x):
  #perform distance calculation based on tuple of points
  return distance(x[0], x[1]).miles

def parallel_map_point(s):
  pairs = [(s,p) for p in points]
  dists = pool.map(distance_wrapper, pairs)
  min_dist = min(dists) 
  index = dists.index(min_dist)
  return index








points = load_points()
pool = Pool()
f = open("dump1")

#loop through json's here
start = time.time()
#for line in f:
for _ in range(1000):
  line = f.readline()
  doc = json.loads(line)
  shuttles = [] #list of tuples of lat longs
  for v in doc['get_vehicles']:
    # if Campus shuttle, and in service
    if v['routeID'] == 8 and v['scheduleNumber'] != 'NIS': 
      shuttles.append( (v['lat'], v['lng']) )
  
  if len(shuttles) > 1: #more than 1 bus on map right now
    indicies = [map_point(s) for s in shuttles] #map points of buses
    print(indicies)
    #indicies = [parallel_map_point(s) for s in shuttles] #map points of buses
    #print(indicies)  
  
print(time.time() - start)

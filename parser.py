import json, csv, time
from geopy.distance import great_circle as distance
#from multiprocessing import Pool

def load_points():
  '''read coordinates of route points from coordinates.csv into memory'''
  reader = csv.reader(open("coordinates.csv"), quoting=csv.QUOTE_NONNUMERIC)
  points = [(lat, lng) for i,lat,lng in reader]
  return points

def load_graph():
  '''Calculate graph of distances between route points
  Each index i holds distance from i to i+1'''
  dists = []
  for i in range(len(points)):
    d = distance(points[i], points[(i+1) % len(points)])
    dists.append(d.miles)
  return dists

def sum_graph(i, j):
  '''sum graph [i,j) to determine distance b/w indicies i and j
  Automatically perform wraparound'''
  if i < j: #normal case, no wraparound
    return sum(graph[i:j])
  elif i > j: #destination point is earlier in list, wrap around
    return sum(graph[i:]) + sum(graph[:j])
  else:
      return 0


def map_point(s): 
  '''Map point s to closest point on route, return index of route point'''
  running_min = float("inf")
  point_index = None #index of closest point on map
  for i, p in enumerate(points):
    dist = distance(p, s).miles
    if dist < running_min:
      running_min = dist
      point_index = i
  return point_index


"""
def distance_wrapper(x):
  #perform distance calculation based on tuple of points
  return distance(x[0], x[1]).miles

def parallel_map_point(s):
  pairs = [(s,p) for p in points]
  dists = pool.map(distance_wrapper, pairs)
  min_dist = min(dists) 
  index = dists.index(min_dist)
  return index
  """






points = load_points() #read route into memory
graph = load_graph() #load graph of distances between points
f = open("dump1")
distribution = []
distribution_f = open("distribution.txt", 'w')
heat_points = []
heat_points_f = open("heat_points.txt", 'w')

start = time.time()
#for line in f: #loop through JSONs in file
for _ in range(1000):
  line = f.readline()
  doc = json.loads(line)
  shuttles = [] #list of tuples of lat longs
  for v in doc['get_vehicles']: # if Campus shuttle, and in service
    if v['routeID'] == 8 and v['scheduleNumber'] != 'NIS':
      shuttles.append( (v['lat'], v['lng']) )
  
  #if len(shuttles) > 1: #more than 1 bus on map right now
  if len(shuttles) == 2: #only look at two bus situations now
    heat_points.extend(shuttles)
    for s in shuttles:
        heat_points_f.write('%s,%s\n' % (s))
    indicies = [map_point(s) for s in shuttles] #map points of buses
    distribution.append(sum_graph(*indicies))
    distribution_f.write(str(distribution[-1]) + '\n')
    
  
print(time.time() - start)



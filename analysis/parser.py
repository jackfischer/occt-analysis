import json, csv, time
from geopy.distance import great_circle as distance
#from multiprocessing import Pool

def load_points():
  '''read coordinates of route points from coordinates.csv into memory'''
  reader = csv.reader(open("coordinates.csv"), quoting=csv.QUOTE_NONNUMERIC)
  points = [(lat, lng) for i,lat,lng in reader]
  return points


def load_stops():
  '''Load csv of stop id,route index into dictionary by next
  stop ids, so that it can be easily queried to grab next route point'''
  f = open('stop_correspondences.txt')
  stops = {}
  for stop in f:
    stop_id, route_index, name = stop.split(',')
    stops[int(stop_id)] = int(route_index)
  return stops


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


def smart_map_point(s):
  '''Map point s to closets point on route conscious of nextStopID'''
  #Calculate range of indexes of points to check
  half = int(len(points) / 3)
  lat, lng, nextStopID = s
  print(s)
  destination_index = stops[nextStopID]
  if (destination_index - half) >= 0: #chuck to check is in higher half
    check = [i for i in range(destination_index - half, destination_index)]
  else: #chunk to check dips below 0
    check = [i for i in range(0, destination_index)]
    delta = -(destination_index - half)
    check.extend( [i for i in range(len(points) - delta, len(points))])
  check.extend([i % len(points) for i in range(destination_index,
    destination_index + 3)])

  #Actual search
  running_min = float("inf")
  point_index = None #index of closest point on map
  for i in check:
    dist = distance(points[i], s).miles
    if dist < running_min:
      running_min = dist
      point_index = i
  return point_index


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




points = load_points() #read route into memory
graph = load_graph() #load graph of distances between points
stops = load_stops() #load correspondence of stops and routes
f = open("dump6")
distribution = []
distribution_f = open("distribution.txt", 'a')
heat_points = []
heat_points_f = open("heat_points.txt", 'a')

start = time.time()
#for _ in range(10000):
for line in f: #loop through JSONs in file
  #line = f.readline()
  doc = json.loads(line)
  shuttles = [] #list of tuples of lat longs
  for v in doc['get_vehicles']: # if Campus shuttle, and in service
    if v['routeID'] == 8 and v['scheduleNumber'] != 'NIS':
      shuttles.append( (v['lat'], v['lng'], v['nextStopID']) )
  
  #if len(shuttles) > 1: #more than 1 bus on map right now
  if len(shuttles) == 2: #only look at two bus situations now
    heat_points.extend(shuttles)
    for s in shuttles:
        heat_points_f.write('%s,%s\n' % (s[0], s[1]))
    indicies = [map_point(s) for s in shuttles] #map points of buses
    print(indicies)
    distribution.append(sum_graph(*indicies))
    distribution_f.write(str(distribution[-1]) + '\n')
    
  
print(time.time() - start)



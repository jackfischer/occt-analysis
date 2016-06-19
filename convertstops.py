import json
from geopy.distance import great_circle as distance

#load route point ids and coordinates into memory
f = open("coordinates.csv")
route = []
for coord in f:
  id_, lat, lng, = coord.split(',')
  route.append((int(id_), float(lat), float(lng)))


#load stops and filter by campus shuttle (route id = 8)
f = open("get_stops.json")
doc = json.loads(f.readline())
stops = doc['get_stops']
cs_stops = []
for stop in stops: #TODO: swap with filter
  if stop['rid'] == 8: #campus shuttle stops
    cs_stops.append((stop['id'], stop['lat'], stop['lng'], stop['name']))


#n^2 find closest route point for each stop, record stop_id,route_point_id
f = open("stop_correspondences.txt", 'w')
for stop in cs_stops:
  dists = [distance((stop[1],stop[2]), (r[1],r[2])).miles for r in route]
  r_index = dists.index(min(dists))
  r_id = route[r_index][0]
  f.write('%d,%d,%s\n' % (stop[0], r_id, stop[3]))


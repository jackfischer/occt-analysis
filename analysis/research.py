import json
from collections import defaultdict
ids = [256, 257, 258, 260, 261, 263, 264, 265, 266, 267, 268, 269]
f=open("get_stops.json")
stops = json.loads(f.readline())['get_stops']


f = open("dump1")
s = defaultdict(int)
for _ in range(1000):
  line = f.readline()
  doc = json.loads(line)
  for v in doc['get_vehicles']: # if Campus shuttle, and in service
    nsi = v['nextStopID']
    if nsi and v['routeID'] == 8:
      if int(nsi) not in ids:
        s[int(nsi)] += 1
      else:
        print("GOOD")

print(s)
for i in s:
  print(s[i])
  print(stops[i])
  print()




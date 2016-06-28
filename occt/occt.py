from pymongo import MongoClient
import requests, time

mongo_url="mongodb://occt:occtbus@ds019638.mlab.com:19638/occt"
collection = MongoClient(mongo_url).occt.scrape

while True:
  start = time.time()

  r = requests.get("http://bupublic.etaspot.net/service.php?service=get_vehicles&includeETAData=1&orderedETAArray=1&token=TESTING")
  content = r.json()
  content["time"] = int(time.time())
  collection.insert_one(content)

  print "inserted at %f" % start
  delta = time.time() - start
  if 5 > delta:
    time.sleep(5 - delta)


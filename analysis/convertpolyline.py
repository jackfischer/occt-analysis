import polyline, csv

f = open("CSpolyline.txt")
p = f.readline()
print(p)
coords = polyline.decode(p)

f = open("coordinates.csv", 'w')
writer = csv.writer(f)

for i, (lat, lng) in enumerate(coords):
  writer.writerow( [i, lat, lng] )


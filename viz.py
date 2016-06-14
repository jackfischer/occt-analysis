import matplotlib.pyplot as plt    
import matplotlib.mlab as mlab     
import matplotlib.colors as colors 
import numpy as np                 

x = []
y = []
for point in open("heat_points.txt"):
  lat, lng = point.split(',')
  x.append(float(lng))
  y.append(float(lat))

distribution = [float(i) for i in open("distribution.txt")]

rnge = [[-75.979, -75.962], [42.082, 42.093]] #cut off outliers
counts, xedges, yedges, image = plt.hist2d(x, y, bins=100, range=rnge, norm=colors.LogNorm())
plt.show()

n, bins, patches = plt.hist(distribution, 50, normed=True, facecolor='green')
mu = np.mean(distribution)
sigma = np.std(distribution)
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y, 'r--', linewidth=1)
plt.show()


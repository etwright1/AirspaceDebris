#
# Created by etwright1 (2024)
# 

import matplotlib.pylab as plt
import numpy as np
import cartopy.crs as ccrs

max_density = 5.419e-8
max_aircraft_density = np.genfromtxt('Output data/Max aircraft density 1 sep 2023 10 second.csv')

list = []
map2 = np.zeros((360,720))

for i in range(0,360):
    for j in range(0,720):
        if max_aircraft_density[i][j] <= max_density/50:
            map2[i][j] = 0
        if max_aircraft_density[i][j] > max_density/50 and max_aircraft_density[i][j] < max_density/20:
            map2[i][j] = 1
        if max_aircraft_density[i][j] > max_density/20 and max_aircraft_density[i][j] < max_density/10:
            map2[i][j] = 2
        if max_aircraft_density[i][j] > max_density/10 and max_aircraft_density[i][j] < max_density/2:
            map2[i][j] = 3
        if max_aircraft_density[i][j] > max_density/2: 
            map2[i][j] = 4

from pylab import *

fontsize = 6
lats = np.arange(-90, 90, 0.5)
lons = np.arange(0, 360, 0.5)

plt.figure(figsize=(6,3), dpi=300)
cmap = cm.get_cmap('Spectral_r', 5)  
ax = plt.axes(projection=ccrs.Robinson(central_longitude=-96, globe=None)) #-96 long for zoom

# define the coordinate system that the grid lons and grid lats are on
rotated_pole = ccrs.RotatedPole()
plt.pcolormesh(lons, lats, map2, cmap = cmap, transform=rotated_pole)
cbar = plt.colorbar(shrink=0.7)
tick_locs = np.linspace(0, 4, 23)[1::5]
cbar_tick_label = ['<0.0011', '>0.0011', '>0.0027', '>0.054', '>0.027']
cbar.set_ticks(tick_locs)
cbar.ax.tick_params(size=0)
cbar.set_ticklabels(cbar_tick_label, fontsize=fontsize)
ax.set_extent([-127, -65, 22, 48]) #for zoom
#plt.annotate(text='Aircraft km$^{-2}$', xy=[500,-85], annotation_clip=False, transform=rotated_pole, fontsize=fontsize)
#ax.coastlines()
     
plt.tight_layout()
plt.savefig('Output plots/Global airspace contours zoom')
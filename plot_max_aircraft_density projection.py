import matplotlib.pylab as plt
import numpy as np
import cartopy.crs as ccrs

max_aircraft_density = np.genfromtxt('Output data/Max aircraft density 1 Sep 2023 10 second.csv')

fontsize = 6
lats = np.arange(-90, 90, 0.5)
lons = np.arange(0, 360, 0.5)

plt.figure(figsize=(6,3), dpi=300)
ax = plt.axes(projection=ccrs.Robinson(central_longitude=-45, globe=None))#adjust longitude for zoom

# define the coordinate system that the grid lons and grid lats are on
rotated_pole = ccrs.RotatedPole()
plt.pcolormesh(lons, lats, max_aircraft_density*1e6, vmax=0.005,cmap = 'Spectral_r', transform=rotated_pole)
cbar = plt.colorbar(shrink=0.7, extend='max')
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(fontsize)
ax.set_extent([-120, +30, 0, 50]) #for zoom
#plt.annotate(text='Aircraft km$^{-2}$', xy=[500,-85], annotation_clip=False, transform=rotated_pole, fontsize=fontsize)
#ax.coastlines()
plt.tight_layout()
plt.savefig('Output plots/Max aircraft density 1 sep 10 seconds projection zoom')
plt.show()
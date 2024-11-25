#
# Created by etwright1 (2024)
# 

import matplotlib.pylab as plt
import numpy as np

percent_threshold = 0.02 #change as required for each density 
max_aircraft_density_distribution = np.genfromtxt('Output data/Max aircraft density 1 sep 2023 10 second.csv')
max_density = 5.41900732078688e-8 #from fort worth 
threshold = percent_threshold*max_density
weighting_function = np.genfromtxt('Output data/10 year weighting function.csv') #reentry weights for past 10 years
daily_weighting_function = weighting_function / (10 * 365.25) #weighting function for 1 day

weighting_function_2d = np.ones((360,720))
list = []
map_mask = np.zeros((360,720))
aircraft_expectation = np.zeros((360,720))

for x in range(720):
    weighting_function_2d[:,x] = daily_weighting_function / 720 #split across the map

for i in range(0,360):
    for j in range(0,720):
        if max_aircraft_density_distribution[i][j] > threshold:
            map_mask[i][j] = 1
        aircraft_expectation[i][j] = weighting_function_2d[i][j] * map_mask[i][j]

print(max_density)
print(threshold)
annual_cas_exp = np.sum(np.sum(aircraft_expectation))*365.25
print(annual_cas_exp)
risk = 1 - np.exp(-annual_cas_exp)
print(risk*100)


#plots to show affected area
fontsize = 6
plt.figure(figsize=(4.75, 2.375),dpi=300)
plt.rc('font', size=fontsize)
plt.pcolormesh(map_mask, cmap = 'Spectral_r')
plt.colorbar(shrink=0.9)
plt.axis('off')
plt.show()
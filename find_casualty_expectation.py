#
# Created by etwright1 (2024)
# 

import numpy as np
import matplotlib.pylab as plt

casualty_expectations = []
aircraft_area = 1000 #m^2

for i in range(0,24,1):

    year = '2023'
    month = '09'
    if i < 10:
        time = '0'+str(i)+'0000Z'
    else:
        time = str(i)+'0000Z'

    file_details = year+ '_'+month + '_01_' + time +'.json.csv'
    density_file = 'Output data/density_'+time+'.json.csv'

    aircraft_density = np.genfromtxt(density_file) #aircraft density at a specific time
    weighting_function = np.genfromtxt('Output data/10 year weighting function.csv') #reentry weights for past 10 years
    hourly_weighting_function = weighting_function / (10 * 365.25 * 24) #weighting function for 1 hour

    weighting_function_per_grid = np.ones((360,720))

    for x in range(720):
        weighting_function_per_grid[:,x] = hourly_weighting_function / 720 #split across the map

    casualty_expectation = weighting_function_per_grid * aircraft_density * aircraft_area

    casualty_expectations.append(sum(sum(casualty_expectation)))

print('The average hourly casualty expectation is = ', np.mean(casualty_expectations))
print('The total day casualty expectation is = ', np.sum(casualty_expectations))
print('The equivalent annual casualty expectation is = ', 365.25*np.sum(casualty_expectations))
    
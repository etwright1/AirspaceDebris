#
# Created by etwright1 (2024)
# 

import matplotlib.pylab as plt
import numpy as np
import csv
import datetime
import casualty as cs

satcat_file = 'GCAT14Mar24.csv'
years = 10

RBGCAT = []
today = '2024 Mar 14'
today = datetime.datetime.strptime(today,'%Y %b %d')
cutoff_date = today - datetime.timedelta(days=years*365.25)
print(f'Todays date is {today}')
print(f'{years} years ago cutoff date is {cutoff_date}')

upper_stages = 0
components = 0

with open(satcat_file, 'r') as csvfile:
    readit = csv.reader(csvfile, delimiter=',')
    for line in readit:
        type = line[3]
        if 'R1' in type or 'R2' in type or 'R3' in type or 'R4' in type or 'R5' in type:
            if line[11] == 'R':
                reentry_date = line[10][:11]
                try: 
                    reentry_date = datetime.datetime.strptime(reentry_date,'%Y %b %d')
                    if reentry_date > cutoff_date:
                        RBGCAT.append(line)
                        upper_stages += 1
                except ValueError:
                    pass  
        elif type[0] == 'C' and type[3] == 'A' or type[0] == 'C' and type[3] == 'M':
            if line[11] == 'R':
                reentry_date = line[10][:11]
                try: 
                    reentry_date = datetime.datetime.strptime(reentry_date,'%Y %b %d')
                    if reentry_date > cutoff_date:
                        RBGCAT.append(line)
                        components += 1
                except ValueError:
                    pass  

print(f'There are {upper_stages} upper stages selected')
print(f'There are {components} components selected')

RE=6378000 # equatorial radius in m

weighting_function = np.zeros(360)
num_of_satellites = len(RBGCAT)
timer = 0

for line in RBGCAT:
    inclination = int(float(line[36]))
    drymass = line[20]
    if inclination > 90:
        inclination = 180 - inclination

    vals, lats = cs.latWeights(0.5, 550e3+RE, inclination) # get latitude weights

    weighting_function += vals # add the normalised times

    timer +=1
    print("Working on satellite:", timer, "of", num_of_satellites)

np.savetxt('Output data/10 year weighting function.csv', weighting_function)
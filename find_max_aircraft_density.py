#
# Created by etwright1 (2024)
# 

import matplotlib.pylab as plt
import numpy as np
import json
from collections import Counter
import os 

RE=6378000 # equatorial radius in m
max_aircraft_density = np.zeros((360,720))
folder_path = "5 second data/2023/data_2023_09_01"

for time in range(0, 240000, 10000): #adjust for resolution as required - 10000 for hourly collision expectation, 10 for max density 

    # Format the time to have leading zeros
    formatted_time = "{:06d}".format(time)
    formatted_time = formatted_time

    # Construct the filename
    filename = f"{formatted_time}Z.json"

    # Check if the file exists
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        print(f"Processing {filename}")

        f = open(file_path)

        data = json.load(f)
        count = 0
        error_count = 0
        aircraft = 0
        total_aircraft=[]
        no_data = 0
        types = []
        all_flights = []

        for i in data['aircraft']: #this bit finds the coordinates of each plane, if they have an appropriate transponder
            count += 1
            try:
                latitude = float(i['lat'])
                longitude = float(i['lon'])
                
            except KeyError: #this nesting is bad form sorry
                try:
                    latitude = float(i['lastPosition']['lat']) #if signal not received within 60 seconds this format used
                    longitude = float(i['lastPosition']['lon'])
                except KeyError:
                    try:
                        latitude = float(i['rr_lat']) #if no signal received estimated coordinates used 
                        longitude = float(i['rr_lon'])
                    except KeyError:
                        error_count += 1
                        pass
                    
            aircraft += 1
            try:
                type = i['t']
                flightno = i['flight']
                flight = [type, flightno, latitude, longitude]
                all_flights.append(flight)
            except KeyError:
                no_data += 1
                pass

        #print('Total aircraft', count)
        #print('Aircraft with data = ', len(all_flights))
        #print('Aircraft without data = ', no_data)
        #print('Lat/lon error count = ', error_count)
            
        total_aircraft = np.append(total_aircraft, count)

        w, h = 2, len(all_flights)
        coordinates = [[0 for x in range(w)] for y in range(h)] 

        j = 0
        for i in range(0,len(all_flights)): 
            coordinates[i][0] = float(all_flights[i][2]*2)/2
            coordinates[i][1] = float(all_flights[i][3]*2)/2

        map = np.zeros((360,721))

        for i in coordinates: #converting coordinates so they plot nicely
            maplat = int(i[0]*2)+180
            maplong = int(i[1]*2)+360
            map[maplat][maplong] = map[maplat][maplong]+1

        latitudes = list(reversed(np.arange(-90, 90, 0.5))) #create latitudes list
        area_of_grid = np.zeros(len(latitudes))
        aircraft_density = np.zeros((360,720))

        for x in range(0,len(latitudes)): #get area
            upper_latitude = abs(90 - x/2) 
            lower_latitude = abs(90 - x/2 + 0.5)
            area_of_grid[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_latitude)) - np.sin(np.deg2rad(lower_latitude)))) / 720 # this is divided by 720 to get the area of each grid cell. In other modelling we have done, we have used area of the entire latitude band and not needed to split it up.

        print('Sensecheck: area of earth =', np.sum(area_of_grid)*720) 

        for x in range(0,len(latitudes)):  
            for y in range(0,720):
                aircraft_density[x][y] =  map[x][y] / area_of_grid[x]
                if aircraft_density[x][y] > max_aircraft_density[x][y]:
                    max_aircraft_density[x][y] = aircraft_density[x][y]
        
        outputfile = 'Output data/density_'+filename+'.csv'
        np.savetxt(outputfile, aircraft_density)

np.savetxt('Output data/Max aircraft density 1 Sep 2023 1 hour.csv', max_aircraft_density)
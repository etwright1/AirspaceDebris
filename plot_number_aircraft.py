#
# Created by etwright1 (2024)
# 

import matplotlib.pylab as plt
import numpy as np
import json
from cycler import cycler

plt.figure(figsize=(4,3), dpi=300)

year = '2023'
font = {'size': 7}
plt.rc('font', **font,)
plt.rc('axes', prop_cycle=(cycler(color=[ '#3DC000', '#00C531', '#00C0AD', '#0084C5', '#001EC5', '#5200C5', '#BC00C5', '#C0000D','#C53800', '#C56D00','#C59B00','#C5C500'])))
fontsize=6

labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

for i in range(1, 13):
    #print('Processing month: '+str(i))
    numbers_of_flights = []
    if i < 10:
        folder = 'Hourly data/'+year+'/Hourly_data_'+year+'_0'+str(i)+'_01'
    else:    
        folder = 'Hourly data/'+year+'/Hourly_data_'+year+'_'+str(i)+'_01'
    for j in range(0,24):
        if j < 10:
            filename = folder+'/0'+str(j)+'0000Z.json'
        else:
            filename = folder+'/'+str(j)+'0000Z.json'
        count=0
        f = open(filename)
        data = json.load(f)
        for line in data['aircraft']:
            count += 1
        numbers_of_flights.append(count)
    print(np.mean(numbers_of_flights)) #mean average number of aircraft in air that day
    plt.plot(numbers_of_flights, label=labels[i-1])

plt.legend(prop={'size': 6}, ncol=2)
plt.xlabel('UTC hour')
plt.ylabel('Number of aircraft with transmitting transponders')
plt.xlim((0,24))
plt.xticks(np.arange(0,25,4))
plt.tight_layout()
plt.savefig('Output plots/Number of aircraft transmitting.png')
plt.show()
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import numpy as np
import matplotlib.transforms as mtransforms

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
with open("/Users/kat/Documents/XCODE/graphPython/dataLessFrequent.txt", "r") as f:
    data = f.read()

data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

for item in data:
    m = findOccurences(item, "|")  
    updateData['timestamp'].append(dt.datetime.fromtimestamp(float(item[11:23][6:])))
    updateData['x'].append(item[24:m[1]])
    updateData['y'].append(item[m[1]+1:m[2]])
    updateData['z'].append(item[m[2]+1:])

ax = plt.gca()
xfmt = md.DateFormatter('%H:%M:%S.%f')
ax.set_color_cycle(['purple', 'green', 'blue', 'black'])
ax.xaxis.set_major_formatter(xfmt)

for i in range(0,len(updateData['x'])):
    updateData['x'][i] = float(updateData['x'][i])
    updateData['y'][i] = float(updateData['y'][i])
    updateData['z'][i] = float(updateData['z'][i])

for i in range(0,len(updateData['z'])):
    if (abs(float(updateData['z'][i]) - float(updateData['z'][i-1])) < .02):
        updateData['z'][i] = -1.0;

start = dt.datetime.fromtimestamp(float(data[0][11:23][6:]))
end = dt.datetime.fromtimestamp(float(data[len(data)-1][11:23][6:]))
interval = int(str(end)[17:19]) - int(str(start)[17:19])

i = 0
sec = updateData['timestamp'][0]
for item in range(0,interval):
    plt.axvline(x=sec, color='r', linestyle='-')
    if (i%2 == 0):
        ax.axvspan(sec, sec + dt.timedelta(0,1), alpha = 0.5, color='red')
    sec += dt.timedelta(0,1) 
    i+=1
                                      
plt.plot(updateData['timestamp'],updateData['x'])
plt.plot(updateData['timestamp'],updateData['y'])
plt.plot(updateData['timestamp'],updateData['z'])

with open("/Users/kat/Documents/XCODE/graphPython/touchLessFrequent.txt", "r") as f:
    data = f.read()

data = data.split('\n')
touch = []

trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)

for item in data:
    i = dt.datetime.fromtimestamp(float(item[11:23][6:]))
    i += dt.timedelta(0,0.1)    
    ax.axvline(i, color = 'k', linestyle='--')
    
#plt.legend(['x', 'y', 'z', 'touch event'], loc='upper left')
fig = plt.gcf()

fig.set_size_inches(18.5, 10.5, forward=True)
plt.show()

#for i in range(1,len(updateData['x'])):
#    if (abs(float(updateData['x'][i]) - float(updateData['x'][i-1])) < .05):
#        updateData['x'][i] = updateData['x'][i-1]
#
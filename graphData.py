import matplotlib.pyplot as plt
import matplotlib.dates as md
#import datetime as dt
import numpy as np
import matplotlib.transforms as mtransforms

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
with open("/Users/kat/Documents/XCODE/graphPython/dataWorking.txt", "r") as f:
    data = f.read()

data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

for item in data:
    m = findOccurences(item, "|")  
    updateData['timestamp'].append(float(item[:m[0]]))
    updateData['x'].append(item[m[0]+1:m[1]])
    updateData['y'].append(item[m[1]+1:m[2]])
    updateData['z'].append(item[m[2]+1:])

ax = plt.gca()
ax.set_color_cycle(['purple', 'green', 'blue', 'black'])


for i in range(0,len(updateData['x'])):
    updateData['x'][i] = float(updateData['x'][i])
    updateData['y'][i] = float(updateData['y'][i])
    updateData['z'][i] = float(updateData['z'][i])

filteredX = [None]*len(updateData['z'])
filteredY = [None]*len(updateData['z'])
filteredZ = [None]*len(updateData['z'])
filteredX[0] = 0.0
filteredY[0] = 0.0
filteredZ[0] = 0.0

for i in range(1,len(updateData['z'])):
    #print filteredZ[i-1]
    filteredX[i] = 0.1 * (filteredX[i-1] + updateData['x'][i] - updateData['x'][i-1]) 
    filteredY[i] = 0.1 * (filteredY[i-1] + updateData['y'][i] - updateData['y'][i-1]) 
    filteredZ[i] = 0.1 * (filteredZ[i-1] + updateData['z'][i] - updateData['z'][i-1]) 


start = float(updateData['timestamp'][0])
end = float(updateData['timestamp'][len(data)-1])
interval = int(end - start)

i = 0
sec = updateData['timestamp'][0]
for item in range(0,interval):
    plt.axvline(x=sec, color='r', linestyle='-')
    if (i%2 == 0):
        #ax.axvspan(sec, sec + 1, alpha = 0.5, color='red')
        pass
    sec += 1
    i+=1

#plt.plot(updateData['timestamp'],filteredX)
#plt.plot(updateData['timestamp'],filteredY)
plt.plot(updateData['timestamp'],filteredZ)


with open("/Users/kat/Documents/XCODE/graphPython/touchWorking.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split('\n')

for item in touchData:   
    ax.axvline(float(item), color = 'k', linestyle='--')
    
#plt.legend(['x', 'y', 'z', 'touch event'], loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()


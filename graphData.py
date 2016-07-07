import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import time

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
with open("/Users/kat/Documents/XCODE/graphPython/data.txt", "r") as f:
    data = f.read()

data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

for item in data:
    m = findOccurences(item, "|")  
    updateData['timestamp'].append(dt.datetime.fromtimestamp(float(item[11:23][6:])))
    updateData['x'].append(item[24:m[1]])
    updateData['y'].append(item[m[1]+1:m[2]])
    updateData['z'].append(item[m[2]+1:])

ax=plt.gca()
xfmt = md.DateFormatter('%H:%M:%S.%f')
ax.xaxis.set_major_formatter(xfmt)
print type(updateData['timestamp'][0])
plt.plot(updateData['timestamp'],updateData['x'])
plt.show()

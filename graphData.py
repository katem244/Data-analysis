import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

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
ax.set_color_cycle(['red', 'green', 'blue'])
ax.xaxis.set_major_formatter(xfmt)
plt.plot(updateData['timestamp'],updateData['x'])
plt.plot(updateData['timestamp'],updateData['y'])
plt.plot(updateData['timestamp'],updateData['z'])

plt.legend(['x', 'y', 'z'], loc='upper left')

plt.show()

import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import numpy as np

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
with open("/Users/kat/Documents/XCODE/graphPython/dataNotMoving2.txt", "r") as f:
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
ax.set_color_cycle(['red', 'green', 'blue', 'black'])
ax.xaxis.set_major_formatter(xfmt)

for i in range(0,len(updateData['x'])):
    updateData['x'][i] = float(updateData['x'][i])
    updateData['y'][i] = float(updateData['y'][i])
    updateData['z'][i] = float(updateData['z'][i])
    
#for i in range(1,len(updateData['x'])):
#    if (abs(float(updateData['x'][i]) - float(updateData['x'][i-1])) < .05):
#        updateData['x'][i] = updateData['x'][i-1]
#
#for i in range(1,len(updateData['z'])):
#    if (abs(float(updateData['z'][i]) - float(updateData['z'][i-1])) < .05):
#        updateData['z'][i] = updateData['z'][i-1] 
        
medianValues = []
for i in range(5, len(updateData['z'])-5):
    items = updateData['z'][i-5:i+5]
    medianValues.append(np.median(items))
#    items = updateData['x'][i:i+5])
#    print numpy.median(items)




#print len(updateData['timestamp'][5:len(updateData['x'])-5])
#print len(medianValues)        
plt.plot(updateData['timestamp'],updateData['x'])
    
    
plt.plot(updateData['timestamp'],updateData['y'])
plt.plot(updateData['timestamp'][5:len(updateData['z'])-5],medianValues)

#print updateData['timestamp']
with open("/Users/kat/Documents/XCODE/graphPython/touch_data2.txt", "r") as f:
    data = f.read()

data = data.split('\n')
touch = []

for item in data:
    i = dt.datetime.fromtimestamp(float(item[11:23][6:]))
    ax.axvline(i, color = 'k', linestyle='--')


#a = [1,2,3,4]
#b = [17,12,11,10]
#c = [-1,-4,5,9]
#print map(lambda x,y:x+y, a,b)
#
#fib = [0,1,1,2,3,5,8,13,21,34,55]
#result = filter(lambda x: x % 2, fib)
#print result
#
#print reduce(lambda x,y:x-y, fib)
#f = lambda x: b - a
#print f
##print filter(f, [47,11,42,102,13])
#
##print reduce(f, [47,11,42,102,13])

plt.legend(['x', 'y', 'z', 'touch event'], loc='upper left')

plt.show()

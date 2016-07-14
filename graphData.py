import matplotlib.pyplot as plt
import matplotlib.dates as md
#import datetime as dt
import numpy as np
import matplotlib.transforms as mtransforms

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
with open("/Users/kat/Documents/XCODE/graphPython/highFreqData.txt", "r") as f:
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
ax.set_color_cycle(['purple','black'])


for i in range(0,len(updateData['x'])):
    updateData['x'][i] = float(updateData['x'][i])
    updateData['y'][i] = float(updateData['y'][i])
    updateData['z'][i] = float(updateData['z'][i])


lowpX = [None]*len(updateData['z'])
lowpY = [None]*len(updateData['z'])
lowpZ = [None]*len(updateData['z'])
lowpX[0] = 0.0
lowpY[0] = 0.0
lowpZ[0] = 0.0

filteredX = [None]*len(updateData['z'])
filteredY = [None]*len(updateData['z'])
filteredZ = [None]*len(updateData['z'])
filteredX[0] = 0.0
filteredY[0] = 0.0
filteredZ[0] = 0.0

#for i in range(1,len(updateData['z'])):
#    #print filteredZ[i-1]
#    lowpX[i] = lowpX[i-1] + 0.2 * (updateData['x'][i] - lowpX[i-1])
#    lowpY[i] = lowpY[i-1] + 0.2 * (updateData['y'][i] - lowpY[i-1])
#    lowpZ[i] = lowpZ[i-1] + 0.2 * (updateData['z'][i] - lowpZ[i-1])

for i in range(1,len(updateData['z'])):
    filteredX[i] = 0.1 * (filteredX[i-1] + updateData['x'][i] - updateData['x'][i-1]) 
    filteredY[i] = 0.1 * (filteredY[i-1] + updateData['y'][i] - updateData['y'][i-1]) 
    filteredZ[i] = 0.1 * (filteredZ[i-1] + updateData['z'][i] - updateData['z'][i-1]) 

for i in range(1,len(updateData['z'])):
    if (abs(filteredZ[i] - filteredZ[i-1]) < .009):
        filteredZ[i] = 0.0



start = float(updateData['timestamp'][0])
end = float(updateData['timestamp'][len(data)-1])
interval = int(end - start)

i = 0
sec = updateData['timestamp'][0]

with open("/Users/kat/Documents/XCODE/graphPython/highFreqTouch.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split('\n')

for item in touchData:   
    ax.axvline(float(item), color = 'k', linestyle='--')


for item in range(0,interval/2):
    plt.axvline(x=sec, color='r', linestyle='-')
    #if (i%2 == 0):
        #ax.axvspan(sec, sec + 1, alpha = 0.5, color='red')
        #pass
    time = sec
    #print "time is " + str(time)
    #print "sec is " + str(sec)
    color = 0
    while time < (sec + 2):
        point =  np.interp(time, updateData['timestamp'], filteredZ)
        if point != 0:
            color += 1
        time += .01
        
    if (color != 0):
        right = 0;
        for touch in touchData:
            #print type(touch)
            #print type(sec)
            #print "item is " + str(touch) + ", sec is " + str(sec) + ", sec + 1 is " + str(sec + 1)
            #print touch > sec
            #print touch < (sec + 1)
            if (float(touch) > sec and float(touch )< (sec + 2)):
                right += 1
        if right > 0:    
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
                
    i+=2
    sec += 2
    #print "time is " + str(sec) + ", color is " + str(color) + ", 'time' is " + str(time)
    
#plt.plot(updateData['timestamp'],filteredX)
#plt.plot(updateData['timestamp'],filteredY)
plt.plot(updateData['timestamp'],filteredZ)



    
plt.legend(['z', 'touch event'], loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()


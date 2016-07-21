import matplotlib.pyplot as plt
import numpy as np


# Finds instances of a certain character in a string
def findInstances(s, c):
    return [i for i, letter in enumerate(s) if letter == c]
  
# Filters the data given an alpha value and a set of data from a certain time 
# interval (brokenUpData) and the filtered array thus far
def filtering(brokenUpData, alpha, filteredZ):
    filteredZ.append(0.0)
    
    for i in range(1,len(brokenUpData)):
        # High pass filter equation
        filteredZ.append(alpha * (filteredZ[len(filteredZ)-1] + brokenUpData[i] - brokenUpData[i-1]))
        
        # Thresholding
        if (abs(filteredZ[len(filteredZ)-1] - filteredZ[len(filteredZ)-2]) < .0004):
            filteredZ[len(filteredZ)-1] = 0.0
    return filteredZ
   
# Analyzes the data to see if detected touch matches actual touch event. 
# touchData is a list of all timestamps of touch events.
# sec is the timestamp beginning the given 2 second interval
# color is the number of times a spike was recognized from the filteredData
# legend1 and legend2 are booleans that will be used in order for value to only
# appear on the legend once
def analysis(num, touchData, sec, color, legend1, legend2):

    # Initialize right and wrong variables to false
    right = False; wrong = False
    
    # Number of spikes has to pass a minumum number, specified by user
    if (color > num):
        for x in range(0, len(touchData)-1):
            # If there was an touch event in that time interval ...
            if (float(touchData[x]) > sec and float(touchData[x] ) < (sec + 2)):
                # Change the value right to true
                right = True
        
        if right and legend1: 
            # Detected touch + actual touch (true positive)
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green', label = 'True positive/negative')
            legend1 = False
        elif right:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green')
        elif legend2:
            # Detected touch + no touch (false positive)
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red', label = 'False positive/negative')
            legend2 = False 
        else: 
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
    else:
        for x in range(0, len(touchData)-1):
            # If there was an touch event in that time interval ...
            if (float(touchData[x]) > sec and float(touchData[x]) < (sec + 2)):
                # Change the value wrong to true
                wrong = True
        
        if wrong and legend2:
            # Did not detect touch + actual touch (false negative)    
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red', label = 'False positive/negative') 
            legend2 = False
        elif wrong:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 

        elif legend1:
            # Did not detect touch + no touch (true negative)            
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green', label = 'True positive/negative') 
            legend1 = False
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 

    return legend1, legend2

# Open accelerometer data file
with open("/Users/kat/Desktop/newTouch4.txt", "r") as f:
    data = f.read()
 
# Modify file to get       
data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

for item in data:
    m = findInstances(item, "|")  
    updateData['timestamp'].append(float(item[:m[0]]))
    updateData['z'].append(float(item[m[2]+1:]))

ax = plt.gca()

with open("/Users/kat/Desktop/touchDataNewTouch4.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split(' ')

legend1 = True
# Plot dashed vertical lines whenever a touch event happened
for i in range (0,len(touchData)-1): 
    if legend1:
        # Only want value on legend to appear once
        ax.axvline(float(touchData[i]), color = 'k', linestyle='--', label='Touch event')
        legend1 = False
    else:
        ax.axvline(float(touchData[i]), color = 'k', linestyle='--')

# Get the time interval of data collection to split up in 2 second intervals
start = updateData['timestamp'][0]; end = updateData['timestamp'][len(data)-1]; 
interval = int(end - start)

avgs = []; secs = []; colors = []; brokenUpData={}; newTime = [];
sec = updateData['timestamp'][0]

legendSec = True
for item in range(0,interval/2 + 1):
    brokenUpData[item] = []       
    if legendSec:
        # Only want value on legend to appear once
        plt.axvline(x=sec, color='r', linestyle='-', label = 'Two second mark')
        legendSec = False
    else:
        plt.axvline(x=sec, color='r', linestyle='-')
    
    time = sec
    avg = 0
    m = 0
    while time < (sec + 2):
        # Get the exact point at given time
        point =  np.interp(time, updateData['timestamp'], updateData['z'])
        avg += point
        time += .002
        m += 1
        # Add to the dictionary an entry with the index of the time interval as key
        # and the array of points during that interval as value
        # This will help with filtering the data more accurately
        brokenUpData[item].append(point)
        newTime.append(time)
   
    # Get the average of all points in the 2 sec interval 
    avg /= m
    avgs.append(avg)
    secs.append(sec)                                                 
    sec += 2
 
filteredZ = []

total = 0
for n in range(0,len(brokenUpData)):
    if n == 0:
        # Ignore walking / activities with too high acceleration (alpha is very small)
        if avgs[n] > 0:
            filteredZ = filtering(brokenUpData[n], 0.00003, filteredZ)
        # If two time intervals are closer together, user is relatively stable,
        # so small differences are more important (alpha is bigger)
        elif abs(avgs[n] - avgs[n+1]) < 0.02: 
            filteredZ = filtering(brokenUpData[n], 0.1, filteredZ)
        else:
        # Otherwise filter out more
            filteredZ = filtering(brokenUpData[n], 0.02, filteredZ)
    elif n < len(brokenUpData)-1:
        if avgs[n] > 0:
            filteredZ = filtering(brokenUpData[n], 0.00003, filteredZ)
        elif (avgs[n] < -0.9 and avgs[n] > -1.1) or abs(avgs[n] - avgs[n+1]) < 0.02 or abs(avgs[n] - avgs[n-1]) < 0.02: 
            filteredZ = filtering(brokenUpData[n], 0.1, filteredZ)
        else:
            filteredZ = filtering(brokenUpData[n], 0.02, filteredZ)
    else:
        if avgs[n] > 0:
            filteredZ = filtering(brokenUpData[n], 0.00003, filteredZ)
        elif abs(avgs[n] - avgs[n-1]) < 0.02: 
            filteredZ = filtering(brokenUpData[n], 0.1, filteredZ)
        else:
            filteredZ = filtering(brokenUpData[n], 0.02, filteredZ)
    for x in range(0, len(brokenUpData[n])):
        total += 1

# For each time interval, check whether or not a spike was detected (var color)    
for item in range(0,interval/2):
    time = secs[item]
    color = 0
    while time < (secs[item] + 2):
        point =  np.interp(time, newTime, filteredZ)
        if point != 0:
            color += 1
        # If the spike is too big, assume user made a sudden movement and should
        # not be counted as user interaction
        if abs(point) > 0.0065:
            color = -1
            break
        time += .002
    colors.append(color)
        
legend1 = True; legend2 = True;                       
for x in range(0,len(avgs)-1):
    if x == 0:
        # If avg of intervals are close to each other, the minumum # of spikes 
        # to detect interaction is lower
        if abs(avgs[x] - avgs[x+1]) < 0.015:
            legend1, legend2 = analysis(10, touchData, secs[x], colors[x], legend1, legend2)
        else:
            legend1, legend2 = analysis(50, touchData, secs[x], colors[x], legend1, legend2)            
    elif x < len(avgs) - 1:
        if abs(avgs[x] - avgs[x+1]) < 0.015 or abs(avgs[x-1] - avgs[x]) < 0.015:
            legend1, legend2 = analysis(10, touchData, secs[x], colors[x], legend1, legend2)
        else:
            legend1, legend2 = analysis(50, touchData, secs[x], colors[x], legend1, legend2) 
    else:
        if abs(avgs[x] - avgs[x-1]) < 0.015:
            analysis(10, touchData, secs[x], colors[x], legend1, legend2)
        else:
            analysis(50, touchData, secs[x], colors[x], legend1, legend2)
            
plt.plot(newTime, filteredZ, color = 'purple', linestyle = '-', label = 'Stage 3 analyzed data')
#plt.plot(updateData['timestamp'],updateData['z'])
 
# Modify graph display
plt.xlabel('Seconds')
plt.title('Stage 3 Analysis')     
plt.legend(loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()
import matplotlib.pyplot as plt
import numpy as np

# Finds instances of a certain character in a string
def findInstances(s, c):
    return [i for i, letter in enumerate(s) if letter == c]

# Open txt file with accelerometer data        
with open("/Users/kat/Desktop/newTouch4.txt", "r") as f:
    data = f.read()

data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

# Make a dictionary updateData with timestamp and z data
for item in data:
    m = findInstances(item, "|")  
    updateData['timestamp'].append(float(item[:m[0]]))
    updateData['z'].append(float(item[m[2]+1:]))

ax = plt.gca()

filteredZ = [None]*len(updateData['z'])
filteredZ[0] = 0.0

for i in range(1,len(updateData['z'])):
    # High pass filter with alpha = 0.1
    filteredZ[i] = 0.1 * (filteredZ[i-1] + updateData['z'][i] - updateData['z'][i-1]) 
    # Thresholding at .009
    if (abs(filteredZ[i] - filteredZ[i-1]) < .009):
         filteredZ[i] = 0.0
         

with open("/Users/kat/Desktop/touchDataNewTouch4.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split(' ')

legend1 = True
# Graph touch events as black dashed lines
for i in range (0,len(touchData)-1): 
    if legend1:
        ax.axvline(float(touchData[i]), color = 'k', linestyle='--', label='Touch event')
        legend1 = False
    else:
        ax.axvline(float(touchData[i]), color = 'k', linestyle='--')

legend2 = True; legendGreen = True; legendRed = True;

start = float(updateData['timestamp'][0]); end = float(updateData['timestamp'][len(data)-1])
interval = int(end - start)

sec = updateData['timestamp'][0]

for item in range(0,interval/2 + 1):
    # Mark two second intervals with red solid line
    if legend2:
        plt.axvline(x=sec, color='r', linestyle='-', label = 'Two second mark')
        legend2 = False
    else:
        plt.axvline(x=sec, color='r', linestyle='-')
    time = sec
    color = 0
    
    # Get all points in interval and check if they are 0 or not. If not, a touch 
    # has been detected
    while time < (sec + 2):
        point =  np.interp(time, updateData['timestamp'], filteredZ)
        if point != 0:
            color += 1
        # If value is over 0.05 assume sudden movement and discard as user interaction
        if abs(point) > 0.05:
            color = -1
            break
        time += .002
    
    right = False; wrong = False;
    
    if (color > 0):
        for x in range(0, len(touchData)-1):
            # Check if there was an event in that interval
            if (float(touchData[x]) > sec and float(touchData[x] ) < (sec + 2)):
                right = True
        if right and legendGreen: 
            # Detected touch + real touch (true positive)  
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green', label = 'True positive/negative') 
            legendGreen = False
        elif right: 
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
        elif legendRed:
            # Detected touch + no touch (false positive)
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red', label = 'False positive/negative')   
            legendRed = False
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
    else:
        for x in range(0, len(touchData)-1):
            if (float(touchData[x]) > sec and float(touchData[x]) < (sec + 2)):
                wrong = True
        if wrong and legendRed:  
            # Did not detect touch + real touch (false negative) 
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red', label = 'False positive/negative')   
            legendRed = False
        elif wrong: 
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
        elif legendGreen:
            # Did not detect touch + no touch (true negative)
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green', label = 'True positive/negative') 
            legendGreen = False
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
                                        
    sec += 2

plt.plot(updateData['timestamp'],filteredZ, color = 'purple', linestyle = '-', label = 'Stage 2 analyzed data') 

#plt.plot(updateData['timestamp'],updateData['z'], color = 'purple', linestyle = '-', label = 'Z-axis accelerometer data')
 
# Modify graph display 
plt.xlabel('Seconds')
plt.title('Stage 2 Analysis')     
plt.legend(loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()
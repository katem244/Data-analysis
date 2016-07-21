import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import matplotlib.transforms as mtransforms

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
with open("/Users/kat/Desktop/newTouch4.txt", "r") as f:
    data = f.read()

data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

for item in data:
    m = findOccurences(item, "|")  
    updateData['timestamp'].append(float(item[:m[0]]))
    updateData['z'].append(item[m[2]+1:])

ax = plt.gca()
#ax.set_color_cycle(['purple','black'])


for i in range(0,len(updateData['z'])):
    updateData['z'][i] = float(updateData['z'][i])

filteredZ = [None]*len(updateData['z'])
filteredZ[0] = 0.0

for i in range(1,len(updateData['z'])):
    filteredZ[i] = 0.1 * (filteredZ[i-1] + updateData['z'][i] - updateData['z'][i-1]) 

for i in range(1,len(updateData['z'])):
    if (abs(filteredZ[i] - filteredZ[i-1]) < .009):
         filteredZ[i] = 0.0


start = float(updateData['timestamp'][0])
end = float(updateData['timestamp'][len(data)-1])
interval = int(end - start)

sec = updateData['timestamp'][0]

with open("/Users/kat/Desktop/touchDataNewTouch4.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split(' ')

legend1 = True
for i in range (0,len(touchData)-1): 
    if legend1:
        ax.axvline(float(touchData[i]), color = 'k', linestyle='--', label='Touch event')
        legend1 = False
    else:
        ax.axvline(float(touchData[i]), color = 'k', linestyle='--')

legend2 = True; legendGreen = True; legendRed = True;
for item in range(0,interval/2 + 1):
    if legend2:
        plt.axvline(x=sec, color='r', linestyle='-', label = 'Two second mark')
        legend2 = False
    else:
        plt.axvline(x=sec, color='r', linestyle='-')
    time = sec
    color = 0
    
    while time < (sec + 2):
        point =  np.interp(time, updateData['timestamp'], filteredZ)
        if point != 0:
            color += 1
        if abs(point) > 0.05:
            color = -1
            break
        time += .002
    
    right = False; wrong = False;
    if (color > 0):
        for x in range(0, len(touchData)-1):
            if (float(touchData[x]) > sec and float(touchData[x] ) < (sec + 2)):
                right = True
        if right and legendGreen:   
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green', label = 'True positive/negative') 
            legendGreen = False
        elif right: 
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
        elif legendRed:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red', label = 'False positive/negative')   
            legendRed = False
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
    else:
        for x in range(0, len(touchData)-1):
            if (float(touchData[x]) > sec and float(touchData[x]) < (sec + 2)):
                wrong = True
        if wrong and legendRed:   
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red', label = 'False positive/negative')   
            legendRed = False
        elif wrong: 
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
        elif legendGreen:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green', label = 'True positive/negative') 
            legendGreen = False
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
                                        
    sec += 2

plt.plot(updateData['timestamp'],filteredZ, color = 'purple', linestyle = '-', label = 'Stage 2 analyzed data') 

#plt.plot(updateData['timestamp'],updateData['z'], color = 'purple', linestyle = '-', label = 'Z-axis accelerometer data')
 
plt.xlabel('Seconds')
   
plt.title('Stage 2 Analysis')     
         
plt.legend(loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()
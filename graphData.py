import matplotlib.pyplot as plt
import matplotlib.dates as md
#import datetime as dt
import numpy as np
import matplotlib.transforms as mtransforms

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
    
def analysis(num, touchData, sec, color):
    right = 0
    wrong = 0
    if (color > num):
        #print sec
        #print color
        for x in range(0, len(touchData)-1):
            if (float(touchData[x]) > sec and float(touchData[x] ) < (sec + 2)):
                right += 1
        if right > 0:    
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
            #print "option 1"
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
    else:
        for x in range(0, len(touchData)-1):
            if (float(touchData[x]) > sec and float(touchData[x]) < (sec + 2)):
                wrong += 1
        if wrong > 0:    
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='red') 
        else:
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
            #print "option 2" 
            #print num   
            #print color    



def filtering(updateData):
    filteredZ = [None]*len(updateData['z'])
    filteredZ[0] = 0.0

    for i in range(1,len(updateData['z'])): 
        filteredZ[i] = 0.1 * (filteredZ[i-1] + updateData['z'][i] - updateData['z'][i-1]) 
        if (abs(filteredZ[i] - filteredZ[i-1]) < .009):
            filteredZ[i] = 0.0
    
    return filteredZ

        
with open("/Users/kat/Desktop/tableAndNot.txt", "r") as f:
    data = f.read()
    

data = data.split('\n')
updateData = {'timestamp':[], 'x':[], 'y':[], 'z':[]}

for item in data:
    m = findOccurences(item, "|")  
    updateData['timestamp'].append(float(item[:m[0]]))
    updateData['z'].append(item[m[2]+1:])

ax = plt.gca()
ax.set_color_cycle(['purple','black'])


for i in range(0,len(updateData['x'])):
    updateData['z'][i] = float(updateData['z'][i])

#

start = float(updateData['timestamp'][0])
end = float(updateData['timestamp'][len(data)-1])
interval = int(end - start)

i = 0
sec = updateData['timestamp'][0]

with open("/Users/kat/Desktop/touchDataTableAndNot.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split(' ')

for i in range (0,len(touchData)-1): 
    ax.axvline(float(touchData[i]), color = 'k', linestyle='--')


avgs = []
secs = []
colors = []
for item in range(0,interval/2 + 1):
    plt.axvline(x=sec, color='r', linestyle='-')
    time = sec
    color = 0
    avg = 0
    m = 0
    #print sec
    while time < (sec + 2):
        avg += np.interp(time, updateData['timestamp'], updateData['z'])
        time += .002
        m += 1
    avg /= m
    avgs.append(avg)
    secs.append(sec)                                                 
    #i+=2
    sec += 2
    
for n in range(0,len(avgs)-1):
    if i == 0:
        if abs(avgs[n] - avgs[n+1]) < 0.015:
            
            analysis(0, touchData, secs[n], colors[n])
        else:
            #print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(64, touchData, secs[n], colors[n])    
    elif n < len(avgs) - 1:
        if abs(avgs[n] - avgs[n+1]) < 0.015 or abs(avgs[n-1] - avgs[n]) < 0.015:
            #print "heyyaaaaaaaaa, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(0, touchData, secs[n], colors[n])
            #print x
        else:
            #print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(64, touchData, secs[n], colors[n]) 
    else:
        if abs(avgs[n] - avgs[n-1]) < 0.015:
            #print "heyy, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(0, touchData, secs[n], colors[n])
        else:
            #print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(64, touchData, secs[n], colors[n])
                



for item in range(0,interval/2 + 1):
    time = sec
    color = 0
    avg = 0
    m = 0
    #print sec
    while time < (sec + 2):
        point =  np.interp(time, updateData['timestamp'], filteredZ)
        avg += np.interp(time, updateData['timestamp'], updateData['z'])
        if point != 0:
            color += 1
        if abs(point) > 0.07:
            color = -1
            break
        time += .002
        m += 1    
        
            
                
                    
                            
for x in range(0,len(avgs)-1):
    if i == 0:
        
        if abs(avgs[x] - avgs[x+1]) < 0.015:
            #print "heyy, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(0, touchData, secs[x], colors[x])
        else:
            #print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(64, touchData, secs[x], colors[x])    
    elif x < len(avgs) - 1:
        if abs(avgs[x] - avgs[x+1]) < 0.015 or abs(avgs[x-1] - avgs[x]) < 0.015:
            #print "heyyaaaaaaaaa, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(0, touchData, secs[x], colors[x])
            #print x
        else:
            #print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(64, touchData, secs[x], colors[x]) 
    else:
        if abs(avgs[x] - avgs[x-1]) < 0.015:
            #print "heyy, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(0, touchData, secs[x], colors[x])
        else:
            #print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(64, touchData, secs[x], colors[x])
                
#plt.plot(updateData['timestamp'],filteredX)
#plt.plot(updateData['timestamp'],filteredY)
plt.plot(updateData['timestamp'],filteredZ)
#plt.plot(updateData['timestamp'],updateData['z'])

      
plt.legend(['z', 'touch event'], loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()


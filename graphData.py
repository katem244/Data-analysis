import matplotlib.pyplot as plt
import matplotlib.dates as md
#import datetime as dt
import numpy as np
import matplotlib.transforms as mtransforms

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]
    
    
def analysis(num, touchData, sec, color):
    right = 0; wrong = 0
    if (color > num):
        for x in range(0, len(touchData)-1):
            if (float(touchData[x]) > sec and float(touchData[x] ) < (sec + 2)):
                right += 1
        if right > 0:    
            ax.axvspan(sec, sec + 2, alpha = 0.5, color='green') 
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



def filtering(brokenData, alpha, filteredZ):
    #filteredZ[0] = 0.0  
    #print "hi"
    filteredZ.append(0.0)

    for i in range(1,len(brokenData)): 
        #print brokenData[i]
        #print len(filteredZ)
        ##filteredZ.append("hi")
        #print len(filteredZ)
        #print filteredZ
        #print type(filteredZ[len(filteredZ)-1])
        filteredZ.append(alpha * (filteredZ[len(filteredZ)-1] + brokenData[i] - brokenData[i-1]))
        if (abs(filteredZ[len(filteredZ)-1] - filteredZ[len(filteredZ)-2]) < .0004):
            filteredZ[len(filteredZ)-1] = 0.0
    #print filteredZ
    #print len(filteredZ)
    return filteredZ

        
with open("/Users/kat/Desktop/newTouch4.txt", "r") as f:
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

start = float(updateData['timestamp'][0]); end = float(updateData['timestamp'][len(data)-1]); interval = int(end - start)

i = 0; sec = updateData['timestamp'][0]

with open("/Users/kat/Desktop/touchDataNewTouch4.txt", "r") as f:
    touchData = f.read()

touchData = touchData.split(' ')

for i in range (0,len(touchData)-1): 
    ax.axvline(float(touchData[i]), color = 'k', linestyle='--')


avgs = []; secs = []; colors = []; brokenData={}; newTime = [];
for item in range(0,interval/2):
    brokenData[item] = []       
    plt.axvline(x=sec, color='r', linestyle='-')
    time = sec
    avg = 0
    m = 0
    while time < (sec + 2):
        point =  np.interp(time, updateData['timestamp'], updateData['z'])
        avg += point
        time += .002
        m += 1
        brokenData[item].append(point)
        newTime.append(time)
    avg /= m
    avgs.append(avg)
    secs.append(sec)                                                 
    sec += 2
 
filteredZ = []

total = 0
for n in range(0,len(brokenData)):
    print avgs[n]
    if n == 0:
        if abs(avgs[n] - avgs[n+1]) < 0.02: 
            filteredZ = filtering(brokenData[n], 0.1, filteredZ)
            print "ey"
        else:
            filteredZ = filtering(brokenData[n], 0.02, filteredZ)
            print "eyyyyy"       
    elif n < len(brokenData)-1:
        if (avgs[n] < -0.9 and avgs[n] > -1.1) or abs(avgs[n] - avgs[n+1]) < 0.02 or abs(avgs[n] - avgs[n-1]) < 0.02: 
            filteredZ = filtering(brokenData[n], 0.1, filteredZ)
            print "ey"
        else:
            filteredZ = filtering(brokenData[n], 0.02, filteredZ)
            print "eyyyyy"  
    else:
        if abs(avgs[n] - avgs[n-1]) < 0.02: 
            filteredZ = filtering(brokenData[n], 0.1, filteredZ)
        else:
            filteredZ = filtering(brokenData[n], 0.02, filteredZ)
    for x in range(0, len(brokenData[n])):
        total += 1
    
print total    
print len(filteredZ)
print len(newTime)    
#print filteredZ
    
for item in range(0,interval/2):
    time = secs[item]
    color = 0
    while time < (secs[item] + 2):
        point =  np.interp(time, newTime, filteredZ)
        if point != 0:
            color += 1
        if abs(point) > 0.0065:
            color = -1
            break
        time += .002
    colors.append(color)
        
print "alldone"           

                    
                                        
                                                                                
#filteredZ = [None]*len(updateData['z'])
#filteredZ[0] = 0.0
#
#for n in range(0,len(avgs)-1):
#    if n == 0:
#        if abs(avgs[n] - avgs[n+1]) < 0.015:
#            filtering(updateData, 0.1, filteredZ, n)
#        else:
#            filtering(updateData, 0.65, filteredZ, n)
#
#                
#
#
#
#for item in range(0,interval/2 + 1):
#    time = sec
#    color = 0
#    avg = 0
#    m = 0
#    #print sec
#    while time < (sec + 2):
#        point =  np.interp(time, updateData['timestamp'], filteredZ)
#        avg += np.interp(time, updateData['timestamp'], updateData['z'])
#        if point != 0:
#            color += 1
#        if abs(point) > 0.07:
#            color = -1
#            break
#        time += .002
#        m += 1    
#        
#            
#                
#                    
#                            
for x in range(0,len(avgs)-1):
    print colors[x]
    if x == 0:
    #analysis(0, touchData, secs[x], colors[x])  
        if abs(avgs[x] - avgs[x+1]) < 0.015:
            print "heyy1, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(15, touchData, secs[x], colors[x])
        else:
            print "old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(50, touchData, secs[x], colors[x])    
    elif x < len(avgs) - 1:
        if abs(avgs[x] - avgs[x+1]) < 0.015 or abs(avgs[x-1] - avgs[x]) < 0.015:
            print "heyyaaaaaaaaa, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(15, touchData, secs[x], colors[x])
            #print x
        else:
            print "heyaaaaaaaa2 old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(50, touchData, secs[x], colors[x]) 
    else:
        if abs(avgs[x] - avgs[x-1]) < 0.015:
            print "heyy, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(15, touchData, secs[x], colors[x])
        else:
            print "heyy2, old av: " + str(avgs[x]) + ", new av: " + str(avgs[x+1])
            analysis(50, touchData, secs[x], colors[x])
                



plt.plot(newTime, filteredZ)
#plt.plot(updateData['timestamp'],updateData['z'])
#
#      
#plt.legend(['z', 'touch event'], loc='upper left')
plt.gcf().set_size_inches(18.5, 10.5, forward=True)
plt.show()


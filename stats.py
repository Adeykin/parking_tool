import math
import numpy as np
import matplotlib.pyplot as plt

def getLine(poligon, index):
    return [poligon[index], poligon[(index+1)%4]]

def length(point0, point1):
    return math.sqrt( math.pow(point0[0]-point1[0], 2) + math.pow(point0[1]-point1[1], 2) )

def linesLengths(poligon):
    lengths = range(4)
    for i in range(4):
        line = getLine(poligon,i)
        lengths[i] = length(line[0], line[1])
    #lengths[0] = length(poligon[0], poligon[1])
    #lengths[1] = length(poligon[1], poligon[2])
    #lengths[2] = length(poligon[2], poligon[3])
    #lengths[3] = length(poligon[3], poligon[0])
    return lengths

def getAngle(line):
    x = line[1][0] - line[0][0];
    y = line[1][1] - line[0][1];
    if y < 0:
        x = -1 * x
        y = -1 * y
    angle = np.arctan( float(y)/x )
    angle = angle * 180 / np.pi
    return angle;

print "hello"

#inputDir = "/home/adeykin/projects/parking/115000004/901000012/list.txt"
listPath = "/home/adeykin/projects/parking/115000004/images/1/list.txt"

listFile = open(listPath, 'r')

poligons = []
for line in listFile:
    lineArr = line.split(' ')
    imgName = lineArr[0]
    lineArr = map(int,lineArr[1:])
    print lineArr
    assert len(lineArr)%8 == 0
    number = len(lineArr) / 8    
    
    for i in range(number):
        offset = i*8;
        poligon = [(lineArr[offset+0], lineArr[offset+1]),
                   (lineArr[offset+2], lineArr[offset+3]),
                   (lineArr[offset+4], lineArr[offset+5]),
                   (lineArr[offset+6], lineArr[offset+7])]
        poligons.append(poligon)
    
    print "line " + str(len(poligons))
        
print "analising poligons"
print "poligons number: " + str(len(poligons))


perim = []
shortLine = []
longLine = []
mShortLine = []
mLongLine = []
angles = []
for poligon in poligons:
    #print poligon
    lengths = linesLengths(poligon)
    idx = sorted(range(len(lengths)),key=lengths.__getitem__)
    #print idx
    #print lengths
    longLine1 = getLine(poligon, idx[2])
    longLine2 = getLine(poligon, idx[3])
    angle1 = getAngle(longLine1)
    angle2 = getAngle(longLine2)
    angles.append(np.mean([angle1,angle2]))
    #angles.append(angle1)
    #angles.append(angle2)
    #print str(angle1) + ' - ' + str(angle2)
    lengths.sort()
    shortLine.append(lengths[0])
    shortLine.append(lengths[1])
    longLine.append(lengths[2])
    longLine.append(lengths[3])
    perim.append(sum(lengths))
    mShortLine.append(np.mean([lengths[0],lengths[1]]))
    mLongLine.append(np.mean([lengths[2],lengths[3]]))
    #print lengths
    
print "SL mean = " + str(np.mean(shortLine))
print "SL std = " + str(np.std(shortLine))
print "SL min = " + str(np.min(shortLine))
print "SL max = " + str(np.max(shortLine))

print "LL mean = " + str(np.mean(longLine))
print "LL std = " + str(np.std(longLine))
print "LL min = " + str(np.min(longLine))
print "LL max = " + str(np.max(longLine))

print "P mean = " + str(np.mean(perim))
print "P std = " + str(np.std(perim))
print "P min = " + str(np.min(perim))
print "P max = " + str(np.max(perim))

print "mSL mean = " + str(np.mean(mShortLine))
print "mSL std = " + str(np.std(mShortLine))
print "mSL min = " + str(np.min(mShortLine))
print "mSL max = " + str(np.max(mShortLine))

print "mLL mean = " + str(np.mean(mLongLine))
print "mLL std = " + str(np.std(mLongLine))
print "mLL min = " + str(np.min(mLongLine))
print "mLL max = " + str(np.max(mLongLine))

plt.scatter(mLongLine,mShortLine)
plt.show()

plt.hist(longLine, bins=20, histtype='stepfilled', label='longLine')
plt.hist(shortLine, bins=20, histtype='stepfilled', label='shortLine')
plt.show()

plt.hist(mLongLine, bins=20, histtype='stepfilled', label='longLine')
plt.hist(mShortLine, bins=20, histtype='stepfilled', label='shortLine')
plt.show()

plt.hist(angles, bins=20, histtype='stepfilled', label='shortLine')
plt.show()

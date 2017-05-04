import math
import numpy as np
import matplotlib.pyplot as plt
import common

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
    lengths = common.linesLengths(poligon)
    idx = sorted(range(len(lengths)),key=lengths.__getitem__)
    #print idx
    #print lengths
    longLine1 = common.getLine(poligon, idx[2])
    longLine2 = common.getLine(poligon, idx[3])
    angle1 = common.getAngle(longLine1)
    angle2 = common.getAngle(longLine2)
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

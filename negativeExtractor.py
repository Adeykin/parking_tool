"""
Description: extract negative examples from images
"""

from shapely.geometry import Polygon
import math
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os.path
import random
from matplotlib.testing.compare import crop_to_same


# cam 1
refRects = [[(-65,-30),(-65,30),(65,30),(65,-30)],
            [(-55,-25),(-55,25),(55,25),(55,-25)],
            [(-45,-25),(-45,25),(45,25),(45,-25)],
            [(-45,-20),(-45,20),(45,20),(45,-20)]]
refOffsets = [(65,30),(55,25),(45,25),(45,20)]
    
refP = [380, 320, 280, 260]
refAngles = [80,-10,45,-45]

"""
#cam 2
refRects = [[(-65,-30),(-65,30),(65,30),(65,-30)],
            [(-55,-25),(-55,25),(55,25),(55,-25)],
            [(-45,-20),(-45,20),(45,20),(45,-20)]]
refOffsets = [(65,30),(55,25),(45,20)]
    
refP = [380, 320, 260]
refAngles = [-60,-30,30,60]
"""

def getLine(poligon, index):
    return [poligon[index], poligon[(index+1)%4]]

def length(point0, point1):
    return math.sqrt( math.pow(point0[0]-point1[0], 2) + math.pow(point0[1]-point1[1], 2) )

#def shiftPoligon():

def linesLengths(poligon):
    lengths = range(4)
    for i in range(4):
        line = getLine(poligon,i)
        lengths[i] = length(line[0], line[1])
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

def rotateVector(angle, x0=1, y0=0):
    radAngle = float(angle)*np.pi/180
    x = x0*np.cos(radAngle) - y0*np.sin(radAngle);
    y = x0*np.sin(radAngle) + y0*np.cos(radAngle);
    return (x,y)

def drawPoligons(img, poligons, color = (255,255,255)):
    for poligon in poligons:
        for i in range(4):
            line = getLine(poligon,i)
            cv2.line(img, line[0], line[1], color)
        
def drawAngles(img, refLocalCentres, refLocalAngles):
    for i in range(len(refLocalAngles)):
        center = refLocalCentres[i]
        angle = refLocalAngles[i]
        vec = rotateVector(angle)
        vec = (vec[0]*50, vec[1]*50)
        center = np.array(center).astype(int)
        vec = np.array(vec).astype(int)
        end = center+vec
        cv2.line(img, (center[0], center[1]), (end[0], end[1]), (0,255,0))

def extractCrop(img, poligonOld, size):
    poligon = np.asarray(poligonOld, dtype=np.float32)
    
    cropH, cropW = size
    cropSizeMat = np.asarray( [(0,0),(cropH,0),(cropH,cropW),(0,cropW)], dtype=np.float32 )
    
    #T = cv2.findHomography(poligon, cropSizeMat)
    T = cv2.getPerspectiveTransform(poligon,cropSizeMat)        
    #crop = cv2.perspectiveTransform(img, T)
    crop = cv2.warpPerspective(img, T, size)
    return crop

#===========================================================================================
"""
inputDir = "/home/adeykin/projects/parking/115000004/901000012"
outputDir = "/home/adeykin/projects/parking/115000004/images/2/negative"
listPath = "/home/adeykin/projects/parking/115000004/images/2/list.txt"
"""
inputDir = "/home/adeykin/projects/parking/115000004/901000011_crop"
outputDir = "/home/adeykin/projects/parking/115000004/images/1/negativeExtend"
listPath = "/home/adeykin/projects/parking/115000004/images/1/list.txt"


listFile = open(listPath, 'r')

poligons = []
for line in listFile:
    lineArr = line.split(' ')
    imgName = lineArr[0]
    imgNameBase = os.path.splitext(imgName)[0]
    lineArr = map(int,lineArr[1:])
    assert len(lineArr)%8 == 0
    number = len(lineArr) / 8
    
    img = cv2.imread(inputDir + '/' + imgName, cv2.CV_LOAD_IMAGE_GRAYSCALE)    
    
    localPoligons = []
    refPoligons = []
    refLocalAngles = []
    refLocalCentres = []
    refLocalPoligons = []
    for i in range(number):
        offset = i*8;
        poligon = [(lineArr[offset+0], lineArr[offset+1]),
                   (lineArr[offset+2], lineArr[offset+3]),
                   (lineArr[offset+4], lineArr[offset+5]),
                   (lineArr[offset+6], lineArr[offset+7])]
        localPoligons.append(poligon)
        
        lengths = linesLengths(poligon)
        idx = sorted(range(len(lengths)),key=lengths.__getitem__)
        longLine1 = getLine(poligon, idx[2])
        longLine2 = getLine(poligon, idx[3])
        angle = np.mean([getAngle(longLine1),getAngle(longLine2)])
        qAngle = min(refAngles, key=lambda x:abs(x-angle))
        meanCoord = ( np.array(poligon)[:,0].mean(), np.array(poligon)[:,1].mean() )
        
        refLocalAngles.append(qAngle)
        refLocalCentres.append(meanCoord)
        
        perim = sum(lengths)
        rectIndex = refP.index( min(refP, key=lambda x:abs(x-perim)) )
        refPoligon = refRects[rectIndex]
        #refOffset = refOffsets[rectIndex]        
        
        refPoligonTr = []
        for point in refPoligon:
            rotPoint = rotateVector(qAngle, point[0], point[1])
            trPoint = (int(rotPoint[0]+meanCoord[0]),int(rotPoint[1]+meanCoord[1]))
            refPoligonTr.append(trPoint)
            
        refLocalPoligons.append(refPoligonTr)
    
    drawPoligons(img, refLocalPoligons, (0,255,0))    
    #Poligins in Shapely format
    shapelyPoligons = []
    for poligon in refLocalPoligons:
        pol = Polygon(poligon)
        shapelyPoligons.append(pol)
        
    #Generating random poligons
    negativeNum = 800
    outPoligon = [(0,0),
                  (img.shape[1],0),
                  (img.shape[1], img.shape[0]),
                  (0,img.shape[0])]
    imgPolygonShapely = Polygon(outPoligon)
    drawPoligons(img, [outPoligon], (255,0,0))
    #shapelyPoligons.append(imgPolygonShapely) 
    for i in range(negativeNum):
        negAngle = random.random() * 90;
        negIndex = int(random.random() * len(refRects))
        negX = int(random.random() * img.shape[1])
        negY = int(random.random() * img.shape[0])
        
        #rotate and transpose
        negPoligon = list(refRects[negIndex]) #to copy list
        for j in range(4):
            point = negPoligon[j]
            point = rotateVector(negAngle, point[0], point[1])
            point = int(point[0]+negX), int(point[1]+negY)
            negPoligon[j] = point
        negPolygonShapely = Polygon(negPoligon)
                
        #Check collision
        noCollisions = True
        if not imgPolygonShapely.contains(negPolygonShapely):
            noCollisions = False
        for shapelyPoligon in shapelyPoligons:
            if shapelyPoligon.intersects(negPolygonShapely):
                noCollisions = False
        
        """
        if noCollisions:
            drawPoligons(img, [negPoligon], (255,0,0))
        else:
            drawPoligons(img, [negPoligon], (0,0,255))
        """ 
        
        if noCollisions:
            crop = extractCrop(img, negPoligon, (100,200))
            cv2.imwrite(outputDir + '/' + imgNameBase + '_' + str(i) + '.png', crop)
            #cv2.imshow('crop', crop)
            #cv2.waitKey()

        
    poligons = poligons + localPoligons
        

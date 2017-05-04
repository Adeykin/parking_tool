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
import common

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
        
        lengths = common.linesLengths(poligon)
        idx = sorted(range(len(lengths)),key=lengths.__getitem__)
        longLine1 = common.getLine(poligon, idx[2])
        longLine2 = common.getLine(poligon, idx[3])
        angle = np.mean([common.getAngle(longLine1), common.getAngle(longLine2)])
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
            rotPoint = common.rotateVector(qAngle, point[0], point[1])
            trPoint = (int(rotPoint[0]+meanCoord[0]),int(rotPoint[1]+meanCoord[1]))
            refPoligonTr.append(trPoint)
            
        refLocalPoligons.append(refPoligonTr)
    
    common.drawPoligons(img, refLocalPoligons, (0,255,0))    
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
    common.drawPoligons(img, [outPoligon], (255,0,0))
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
            point = common.rotateVector(negAngle, point[0], point[1])
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
            crop = common.extractCrop(img, negPoligon, (100,200))
            cv2.imwrite(outputDir + '/' + imgNameBase + '_' + str(i) + '.png', crop)
            #cv2.imshow('crop', crop)
            #cv2.waitKey()

        
    poligons = poligons + localPoligons
        

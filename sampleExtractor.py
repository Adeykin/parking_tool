"""
Description: extract positive examples from input images
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os.path
from matplotlib.testing.compare import crop_to_same
import common
import markParser
from negativeExtractor import refLocalPoligons


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
"""
inputDir = "/home/adeykin/projects/parking/115000004/901000012"
outputDir = "/home/adeykin/projects/parking/115000004/images/2/marked"
listPath = "/home/adeykin/projects/parking/115000004/images/2/list.txt"
outListPath = "/home/adeykin/projects/parking/115000004/images/2/outList.txt"
"""

inputDir = "/home/adeykin/projects/parking/115000004/901000011_crop"
outputDir = "/home/adeykin/projects/parking/115000004/images/1/marked"
listPath = "/home/adeykin/projects/parking/115000004/images/1/list.txt"
outListPath = "/home/adeykin/projects/parking/115000004/images/1/outList.txt"

# TODO
# 1) save cropts as coords
# 2) migrate to numpy
# 3) args
#    inputList, outputList, algorithm, metadata

parser = markParser.MarkParser()
parser.load(listPath)
outParser = markParser.MarkParser()

for mark in parser.marks:
    refLocalPoligons = []
    for poligon in mark.poligons:
        
        lengths = common.linesLengths(poligon)
        idx = sorted(range(len(lengths)),key=lengths.__getitem__)
        longLine1 = common.getLine(poligon, idx[2])
        longLine2 = common.getLine(poligon, idx[3])
        angle = np.mean([common.getAngle(longLine1), common.getAngle(longLine2)])
        qAngle = min(refAngles, key=lambda x:abs(x-angle))
        meanCoord = ( np.array(poligon)[:,0].mean(), np.array(poligon)[:,1].mean() )

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
        
    outParser.marks.append( markParser.Mark(mark.imageName, refLocalPoligons) )

outParser.save(outListPath)
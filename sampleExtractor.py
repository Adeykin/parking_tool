"""
Description: extract positive examples from input images
"""

from shapely.geometry import Polygon
import math
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os.path
from matplotlib.testing.compare import crop_to_same
import common
import markParser
#from detector import trPoligon

"""
inputDir = "/home/adeykin/projects/parking/115000004/901000012"
listPath = "/home/adeykin/projects/parking/115000004/images/2/list.txt"
outListPath = "/home/adeykin/projects/parking/115000004/images/2/outList.txt"

inputDir = "/home/adeykin/projects/parking/115000004/901000011_crop"
listPath = "/home/adeykin/projects/parking/115000004/images/1/list.txt"
outListPath = "/home/adeykin/projects/parking/115000004/images/1/outList.txt"
paramsPath = "/home/adeykin/projects/parking/115000004/images/1/params.txt"
"""
inputDir = "/home/adeykin/projects/parking/data/115000004/901000011_9"
listPath = "/home/adeykin/projects/parking/data/115000004/901000011_9/listF.txt"
outListPath = "/home/adeykin/projects/parking/data/115000004/901000011_9/listSmall.txt"
paramsPath = "/home/adeykin/projects/parking/data/115000004/params11.txt"
maskPath = "/home/adeykin/projects/parking/data/115000004/mask11_small.png"
masked = True

mask = cv2.imread(maskPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)

outPoligon = [(0,0),
              (mask.shape[1],0),
              (mask.shape[1], mask.shape[0]),
              (0,mask.shape[0])]
imgPolygonShapely = Polygon(outPoligon)

# TODO
# 3) args
#    inputList, outputList, algorithm, metadata

parser = markParser.MarkParser()
parser.load(listPath)
outParser = markParser.MarkParser()

refRects, refP, refAngles = common.loadParams(paramsPath)

for mark in parser.marks:
    refLocalPoligons = []
    for poligon in mark.poligons:        
        longLine1, longLine2 = common.getLongLines(poligon)
        angle = np.mean([common.getAngle(longLine1), common.getAngle(longLine2)])
        qAngle = min(refAngles, key=lambda x:abs(x-angle))
        meanCoord = poligon.mean(axis=0)

        perim = common.perim(poligon)
        rectIndex = refP.index( min(refP, key=lambda x:abs(x-perim)) )
        refPoligon = refRects[rectIndex]        

        refPoligonTr = common.rotate(refPoligon, qAngle)
        refPoligonTr = common.transpose(refPoligonTr, meanCoord)
        
        refPoligonTrShapely = Polygon(refPoligonTr)
        if not imgPolygonShapely.contains(refPoligonTrShapely):
            continue

        if masked:
            cropH,cropW = 10,10
            cropSizeMat = np.asarray( [(0,0),(cropH,0),(cropH,cropW),(0,cropW)], dtype=np.float32 )
            T = cv2.getPerspectiveTransform(refPoligonTr.astype(dtype='float32'), cropSizeMat)
            
            crop = cv2.warpPerspective(mask, T, (cropH, cropW))
            whitePart = float(cv2.countNonZero(crop)) / 100
            if whitePart < 0.9:
                continue
        
        refLocalPoligons.append(refPoligonTr)
        
    outParser.marks.append( markParser.Mark(mark.imageName, refLocalPoligons) )

outParser.save(outListPath)
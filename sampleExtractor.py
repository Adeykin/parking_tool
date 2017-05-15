"""
Description: extract positive examples from input images
"""

import os, sys
from shapely.geometry import Polygon
import math
import numpy as np
import cv2
import common
import markParser

if len(sys.argv) < 4:
    print "USAGE: python sampleExtracotr.py <listFile> <outListFile> <paramsFile> [<maskFile>]"
    print "\t <listFile> - path to list.txt file with labels"
    print "\t <outListFile> - path to list.txt which will contain crops"
    print "\t <paramsFile> - file with camera params"
    print "\t <maskFile> - binary image with mask (optional)"    
    quit()

listPath = sys.argv[1]
inputDir = os.path.dirname(listPath)
outListPath = sys.argv[2]
paramsPath = sys.argv[3]
masked = False
if len(sys.argv) == 5:
    maskPath = sys.argv[4]
    masked = True
    
print 'listFile: ' + listPath
print 'outListFile: ' + outListPath
print 'params: ' + paramsPath
print 'masked: ' + masked
if masked:
    print 'maskPath: ' + maskPath

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

        if masked and not common.checkMaskContains(mask, refPoligonTr):
            continue
        
        refLocalPoligons.append(refPoligonTr)
        
    outParser.marks.append( markParser.Mark(mark.imageName, refLocalPoligons) )

outParser.save(outListPath)
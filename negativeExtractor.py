"""
Description: extract negative examples from images
"""

import os, sys
from shapely.geometry import Polygon
import math
import numpy as np
import cv2
import random
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

listFile = open(listPath, 'r')

parser = markParser.MarkParser()
parser.load(listPath)
outParser = markParser.MarkParser()

refRects, refP, refAngles = common.loadParams(paramsPath)

negativeNum = 300

for mark in parser.marks:
    img = cv2.imread(inputDir + '/' + mark.imageName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    outPoligon = [(0,0),
                  (img.shape[1],0),
                  (img.shape[1], img.shape[0]),
                  (0,img.shape[0])]
    imgPolygonShapely = Polygon(outPoligon)
    
    shapelyPoligons = []
    for poligon in mark.poligons:
        pol = Polygon(poligon)
        shapelyPoligons.append(pol)
    
    #Generating random poligons
    refLocalPoligons = []
    for i in range(negativeNum):
        negAngle = random.random() * 90;
        negIndex = int(random.random() * len(refRects))
        shift = (np.random.rand(2)*img.shape).astype(dtype=int)[::-1]
        
        #rotate and transpose
        negPoligon = refRects[negIndex].copy()
        negPoligon = common.rotate(negPoligon, negAngle)
        negPoligon = common.transpose(negPoligon, shift)
        
        negPolygonShapely = Polygon(negPoligon)
            
        #Check collision
        noCollisions = True
        if not imgPolygonShapely.contains(negPolygonShapely):
            noCollisions = False
        for shapelyPoligon in shapelyPoligons:
            if shapelyPoligon.intersects(negPolygonShapely):
                noCollisions = False
        
        if masked and not common.checkMaskContains(mask, negPoligon):
            noCollisions = False
        
        if noCollisions:
            refLocalPoligons.append(negPoligon)
            
        
    if len(refLocalPoligons) > 0:
        outParser.marks.append( markParser.Mark(mark.imageName, refLocalPoligons) )
    
outParser.save(outListPath)
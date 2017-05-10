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
import markParser

"""
inputDir = "/home/adeykin/projects/parking/115000004/901000012"
outputDir = "/home/adeykin/projects/parking/115000004/images/2/negative"
listPath = "/home/adeykin/projects/parking/115000004/images/2/list.txt"

inputDir = "/home/adeykin/projects/parking/115000004/901000011_crop"
listPath = "/home/adeykin/projects/parking/115000004/images/1/list.txt"
outListPath = "/home/adeykin/projects/parking/115000004/images/1/negative1.txt"
paramsPath = "/home/adeykin/projects/parking/115000004/images/1/params.txt"
"""

inputDir = "/home/adeykin/projects/parking/data/115000004/901000011_9"
listPath = "/home/adeykin/projects/parking/data/115000004/901000011_9/listF.txt"
outListPath = "/home/adeykin/projects/parking/data/115000004/901000011_9/negative.txt"
paramsPath = "/home/adeykin/projects/parking/data/115000004/params11.txt"
maskPath = "/home/adeykin/projects/parking/data/115000004/mask11_small.png"
masked = True

mask = cv2.imread(maskPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)

listFile = open(listPath, 'r')

parser = markParser.MarkParser()
parser.load(listPath)
outParser = markParser.MarkParser()

refRects, refP, refAngles = common.loadParams(paramsPath)

negativeNum = 800

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
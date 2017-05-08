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
#from detector import trPoligon

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
paramsPath = "/home/adeykin/projects/parking/115000004/images/1/params.txt"

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

        refLocalPoligons.append(refPoligonTr)
        
    outParser.marks.append( markParser.Mark(mark.imageName, refLocalPoligons) )

outParser.save(outListPath)
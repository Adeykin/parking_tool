"""
Descriontion: Extract descriptors from examples and save it to .csv file
"""

import csv
import math
import numpy as np
import cv2
import os.path
import common
import markParser

inputDir = "/home/adeykin/projects/parking/data/115000004/901000011_9"
listPath = "/home/adeykin/projects/parking/data/115000004/901000011_9/positiveSmallMasked.txt"
output = "/home/adeykin/projects/parking/data/115000004/901000011_9/positiveSmallMasked.csv"

f = open(output, 'w')
spamwriter = csv.writer(f, delimiter=';')

size = 40,120
#locations = ((20,60))

locations = ((10,20),)    
winSize = size
blockSize = (16,16)
blockStride = (8,8)
cellSize = (8,8)
nbins = 9

hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins)

parser = markParser.MarkParser()
parser.load(listPath)

#hog = cv2.HOGDescriptor(winSize = size, nbins = 9)

for mark in parser.marks:
    img = cv2.imread(inputDir + '/' + mark.imageName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    #imgNameBase = os.path.splitext(mark.imageName)[0]
    #i = 0
    crops = []
    for poligon in mark.poligons:
        crop = common.extractCrop(img, poligon, size)
        crops.append( crop )
        crops.append( cv2.flip(crop, 0) )
        crops.append( cv2.flip(crop, 1) )
        crops.append( cv2.flip(crop, -1) )
        
    for crop in crops:
        hist = hog.compute(crop)
        spamwriter.writerow(hist.transpose().tolist()[0])
    
    #print hist.transpose()
    
    #break
    #print hist.shape
    
    #print hist.transpose().tolist()
    #print 'Size of list to write: ' + str(len(hist.transpose().tolist()[0])) 
    
    
    #np.savetxt(f, hist.transpose(), delimiter=';')
    #cv2.waitKey()
    #break
"""
Descriontion: Extract descriptors from examples and save it to .csv file
"""

import os
import cv2
import numpy as np
import csv

inputDir = '/home/adeykin/projects/parking/115000004/images/1/negativeExtend'
output = '/home/adeykin/projects/parking/115000004/images/1/negativeExtend.csv'

"""
inputDir = '/home/adeykin/projects/parking/115000004/images/2/negative'
output = '/home/adeykin/projects/parking/115000004/images/2/negative.csv'
"""

f = open(output, 'w')
spamwriter = csv.writer(f, delimiter=';')

for file in os.listdir(inputDir):
    img = cv2.imread(inputDir + '/' + file, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    winSize = (64,64)
    blockSize = (16,16)
    blockStride = (8,8)
    cellSize = (8,8)
    nbins = 9
    derivAperture = 1
    winSigma = 4.
    histogramNormType = 0
    L2HysThreshold = 2.0000000000000001e-01
    gammaCorrection = 0
    nlevels = 64
    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                            histogramNormType,L2HysThreshold,gammaCorrection,nlevels)

    winStride = (8,8)
    padding = (8,8)
    locations = ((10,20),)
    hist = hog.compute(img,winStride,padding,locations)
    
    #print hist.transpose()
    
    #break
    #print hist.shape
    
    #print hist.transpose().tolist()
    #print 'Size of list to write: ' + str(len(hist.transpose().tolist()[0])) 
    spamwriter.writerow(hist.transpose().tolist()[0])
    
    #np.savetxt(f, hist.transpose(), delimiter=';')
    #cv2.waitKey()
    #break
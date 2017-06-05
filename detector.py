"""
Descriptor: Use pretrained detector on images and shows/saves images with detections
"""

import cv2
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
import cPickle
import common
from cmath import rect
from shapely.geometry import Polygon

imagePath = '/home/adeykin/projects/parking/data/115000004/901000011_9/20170414_025323.jpg'
maskPath = '/home/adeykin/projects/parking/data/115000004/mask11_small.png'
paramsPath = '/home/adeykin/projects/parking/data/115000004/params11.txt'
classifierPath = '/home/adeykin/projects/parking/SVC_11_8_PosM_NegF_42.pkl'

size = 40,120
locations = ((10,20),)    
winSize = size
blockSize = (16,16)
blockStride = (8,8)
cellSize = (8,8)
nbins = 9

hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins)

with open(classifierPath, 'rb') as fid:
    classifier = cPickle.load(fid)    
img = cv2.imread(imagePath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
mask = cv2.imread(maskPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
refRects, refP, refAngles = common.loadParams(paramsPath)

outPoligon = [(0,0),
              (img.shape[1],0),
              (img.shape[1], img.shape[0]),
              (0,img.shape[0])]
imgPolygonShapely = Polygon(outPoligon)

for rectIndex in range(len(refRects)):
    rect = refRects[rectIndex]
    for angleIndex in range(len(refAngles)):
        angle = refAngles[angleIndex]
        for x in range(0, img.shape[1]-50, 8):
            for y in range(0, img.shape[0]-50, 8):
                rotRect = common.rotate(rect, angle)
                trRotRect = common.transpose(rotRect, np.asarray((x,y)) )
                
                if mask[y,x] != 255:
                    continue
                
                polygonShapely = Polygon(trRotRect)
                if not imgPolygonShapely.contains(polygonShapely):
                    continue
                
                crop = common.extractCrop(img, trRotRect, size)
                hist = hog.compute(crop)
                #print hist
                #print hist.shape
                pred = classifier.predict(np.transpose(hist))
                print pred
                
                if pred:
                    common.drawPoligons(img, [trRotRect.astype(dtype='int')], (255))
                
                    #imgS = cv2.resize(img, (img.shape[1]/2,img.shape[0]/2))
                    #cv2.imshow('hello', imgS)
                    #cv2.waitKey()
                
        cv2.imwrite('detect'+str(rectIndex)+'_'+str(angleIndex)+'.png', img)

#====================================
"""
refRects = [[(-65,-30),(-65,30),(65,30),(65,-30)],
            [(-55,-25),(-55,25),(55,25),(55,-25)],
            [(-45,-25),(-45,25),(45,25),(45,-25)],
            [(-45,-20),(-45,20),(45,20),(45,-20)]]
refOffsets = [(65,30),(55,25),(45,25),(45,20)]
    
refP = [380, 320, 280, 260]
refAngles = [80,-10,45,-45]

imagePath = '/home/adeykin/projects/parking/115000004/901000011_crop/20170327_121030.jpg'

with open('AdaBoost_1_full.pkl', 'rb') as fid:
    classifier = cPickle.load(fid)
    
imgOrig = cv2.imread(imagePath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
img = np.copy(imgOrig)

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

for angle in refAngles:
    for i in range(len(refOffsets)):
        imgLocal = np.copy(imgOrig)
        poligon = list(refRects[i])
        for j in range(4):
            point = poligon[j]
            point = common.rotateVector(angle, point[0], point[1])
            poligon[j] = int(point[0]), int(point[1])
            
            
        for y in range(50, img.shape[1]-50, 10):
            for x in range(50, img.shape[0]-50, 10):
                trPoligon = list(poligon)
                for j in range(4):
                    point = trPoligon[j]
                    point = point[0] + y, point[1] + x
                    trPoligon[j] = point
                #drawPoligons(img, [trPoligon], (255,0,0))
                
                crop = common.extractCrop(img, trPoligon, (100,200))                                   
                                   
                winStride = (8,8)
                padding = (8,8)
                locations = ((10,20),)
                hist = hog.compute(crop,winStride,padding,locations)
                
                hist = hist.transpose().tolist()[0]

                det = classifier.predict([hist])
                
                if det[0] == 1:
                    common.drawPoligons(img, [trPoligon], (255,0,0))
                    common.drawPoligons(imgLocal, [trPoligon], (255,0,0))
                    #cv2.imshow('hello', crop)
                    #cv2.waitKey()
            print 'angle = ' + str(angle) + '; index = ' +str(i) + '; y = ' + str(y)
        cv2.imwrite('local_' + str(angle) + '_' + str(i) + '.png', imgLocal)
cv2.imwrite('all.png', img)
cv2.imshow('hello', img)
cv2.waitKey()
"""

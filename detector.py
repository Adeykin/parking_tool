"""
Descriptor: Use pretrained detector on images and shows/saves images with detections
"""

import cv2
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
import cPickle

def getLine(poligon, index):
    return [poligon[index], poligon[(index+1)%4]]

def length(point0, point1):
    return math.sqrt( math.pow(point0[0]-point1[0], 2) + math.pow(point0[1]-point1[1], 2) )

#def shiftPoligon():

def linesLengths(poligon):
    lengths = range(4)
    for i in range(4):
        line = getLine(poligon,i)
        lengths[i] = length(line[0], line[1])
    return lengths

def getAngle(line):
    x = line[1][0] - line[0][0];
    y = line[1][1] - line[0][1];
    if y < 0:
        x = -1 * x
        y = -1 * y
    angle = np.arctan( float(y)/x )
    angle = angle * 180 / np.pi
    return angle;

def rotateVector(angle, x0=1, y0=0):
    radAngle = float(angle)*np.pi/180
    x = x0*np.cos(radAngle) - y0*np.sin(radAngle);
    y = x0*np.sin(radAngle) + y0*np.cos(radAngle);
    return (x,y)

def drawPoligons(img, poligons, color = (255,255,255)):
    for poligon in poligons:
        for i in range(4):
            line = getLine(poligon,i)
            cv2.line(img, line[0], line[1], color)
            
def extractCrop(img, poligonOld, size):
    poligon = np.asarray(poligonOld, dtype=np.float32)
    
    cropH, cropW = size
    cropSizeMat = np.asarray( [(0,0),(cropH,0),(cropH,cropW),(0,cropW)], dtype=np.float32 )
    
    #T = cv2.findHomography(poligon, cropSizeMat)
    T = cv2.getPerspectiveTransform(poligon,cropSizeMat)        
    #crop = cv2.perspectiveTransform(img, T)
    crop = cv2.warpPerspective(img, T, size)
    return crop
#======================================================================

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
            point = rotateVector(angle, point[0], point[1])
            poligon[j] = int(point[0]), int(point[1])
            
        for y in range(50, img.shape[1]-50, 10):
            for x in range(50, img.shape[0]-50, 10):
                trPoligon = list(poligon)
                for j in range(4):
                    point = trPoligon[j]
                    point = point[0] + y, point[1] + x
                    trPoligon[j] = point
                #drawPoligons(img, [trPoligon], (255,0,0))
                
                crop = extractCrop(img, trPoligon, (100,200))                                   
                                   
                winStride = (8,8)
                padding = (8,8)
                locations = ((10,20),)
                hist = hog.compute(crop,winStride,padding,locations)
                
                hist = hist.transpose().tolist()[0]

                det = classifier.predict([hist])
                
                if det[0] == 1:
                    drawPoligons(img, [trPoligon], (255,0,0))
                    drawPoligons(imgLocal, [trPoligon], (255,0,0))
                    #cv2.imshow('hello', crop)
                    #cv2.waitKey()
            print 'angle = ' + str(angle) + '; index = ' +str(i) + '; y = ' + str(y)
        cv2.imwrite('local_' + str(angle) + '_' + str(i) + '.png', imgLocal)
cv2.imwrite('all.png', img)
cv2.imshow('hello', img)
cv2.waitKey()
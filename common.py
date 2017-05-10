import numpy as np
import math
import cv2

def getLine(poligon, index):
    return [poligon[index], poligon[(index+1)%4]]

def length(point0, point1):
    return math.sqrt( math.pow(point0[0]-point1[0], 2) + math.pow(point0[1]-point1[1], 2) )

def linesLengths(poligon):
    lengths = range(4)
    for i in range(4):
        line = getLine(poligon,i)
        lengths[i] = length(line[0], line[1])
    return lengths

def getLongLines(poligon):
    lengths = linesLengths(poligon)
    idx = sorted(range(len(lengths)),key=lengths.__getitem__)
    return getLine(poligon, idx[2]), getLine(poligon, idx[3])

def getAngle(line):
    line = line[1] - line[0]
    if line[0] == 0:
        return 90
    angle = np.arctan( float(line[1])/line[0] )
    angle = angle * 180 / np.pi
    return angle

def perim(poligon):
    lengths = linesLengths(poligon)
    return sum(lengths)

def rotate(poligon, angle):
    assert(poligon.shape[1] == 2)
    angle = -angle * np.pi / 180
    c, s = np.cos(angle), np.sin(angle)
    M = np.matrix([[c, -s], [s, c]])
    return poligon * M

def transpose(poligon, value):
    assert( poligon.shape[1] == 2 )
    assert( value.shape == (2,) )
    return poligon + np.tile(value, poligon.shape[0]).reshape(poligon.shape[0], 2)

def drawPoligons(img, poligons, color = (255,255,255)):
    for poligon in poligons:
        cv2.polylines(img, [poligon.reshape((-1,1,2))], True, color)
        
def checkMaskContains(mask, poligon):
    cropH,cropW = 10,10
    cropSizeMat = np.asarray( [(0,0),(cropH,0),(cropH,cropW),(0,cropW)], dtype=np.float32 )
    T = cv2.getPerspectiveTransform(poligon.astype(dtype='float32'), cropSizeMat)
    
    crop = cv2.warpPerspective(mask, T, (cropH, cropW))
    whitePart = float(cv2.countNonZero(crop)) / 100
    return whitePart >= 0.9

def extractCrop(img, poligonOld, size):
    poligon = np.asarray(poligonOld, dtype=np.float32)
    
    cropH, cropW = size
    cropSizeMat = np.asarray( [(0,0),(cropH,0),(cropH,cropW),(0,cropW)], dtype=np.float32 )
    
    #T = cv2.findHomography(poligon, cropSizeMat)
    T = cv2.getPerspectiveTransform(poligon,cropSizeMat)        
    #crop = cv2.perspectiveTransform(img, T)
    crop = cv2.warpPerspective(img, T, size)
    return crop

def loadParams(fileName):
    file = open(fileName, 'r')
    lineRects = file.readline()
    lineAngles = file.readline()
    
    #parse rects
    rectsSides = lineRects.split(' ')
    assert(len(rectsSides) % 2 == 0 )
    rects = []
    perims = []
    for i in range(len(rectsSides)/2):
        s1, s2 = rectsSides[i*2:i*2+2]
        s1, s2 = int(s1),int(s2)
        rect = np.asarray([(-s1,-s2),(-s1,s2),(s1,s2),(s1,-s2)])
        rects.append(rect)
        
        #compute perim
        perim = sum(linesLengths(rect))
        perims.append(perim)    

    #parse angles
    angles = lineAngles.split(' ')
    angles = map(int, angles)
    
    
    
    return rects, perims, angles
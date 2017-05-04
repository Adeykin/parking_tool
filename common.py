import numpy as np
import math
import cv2

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
        
def drawAngles(img, refLocalCentres, refLocalAngles):
    for i in range(len(refLocalAngles)):
        center = refLocalCentres[i]
        angle = refLocalAngles[i]
        vec = rotateVector(angle)
        vec = (vec[0]*50, vec[1]*50)
        center = np.array(center).astype(int)
        vec = np.array(vec).astype(int)
        end = center+vec
        cv2.line(img, (center[0], center[1]), (end[0], end[1]), (0,255,0))
        
        
def extractCrop(img, poligonOld, size):
    poligon = np.asarray(poligonOld, dtype=np.float32)
    
    cropH, cropW = size
    cropSizeMat = np.asarray( [(0,0),(cropH,0),(cropH,cropW),(0,cropW)], dtype=np.float32 )
    
    #T = cv2.findHomography(poligon, cropSizeMat)
    T = cv2.getPerspectiveTransform(poligon,cropSizeMat)        
    #crop = cv2.perspectiveTransform(img, T)
    crop = cv2.warpPerspective(img, T, size)
    return crop
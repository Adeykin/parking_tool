"""
Description: visualize marked data in windows
Input: Images, list.txt
Output: original poligons, approximated poligons, orientation estimation
"""

import sys, os
import math
import numpy as np
import matplotlib.pyplot as plt
import cv2
import common
import markParser

if len(sys.argv) != 2:
    print "USAGE: python visualiser.py <listFile>"
    print "\t <listFile> - path to list.txt file with labels"
    quit()

listPath = sys.argv[1]
inputDir = os.path.dirname(listPath)

print 'listFile: ' + listPath
print 'inputDir: ' + inputDir

parser = markParser.MarkParser()
parser.load(listPath)

for mark in parser.marks:
    img = cv2.imread(inputDir + '/' + mark.imageName)    
    common.drawPoligons(img, mark.poligons, (255,0,0))
    h,w,d = img.shape
    img = cv2.resize(img, (w/2,h/2))
    cv2.imshow('hello', img)
    k = cv2.waitKey(0)
    if k == ord('q'):
        cv2.destroyAllWindows()
        quit()

"""
Description: visualize marked data in windows
Input: Images, list.txt
Output: original poligons, approximated poligons, orientation estimation
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import cv2
import common
import markParser

print "hello"

inputDir = "/home/adeykin/projects/parking/115000004/901000011_crop"
outputDir = "/home/adeykin/projects/parking/115000004/images/1/marked"
listPath = "/home/adeykin/projects/parking/115000004/images/1/outList.txt"

# TODO:
# 2) args
#    inputList*

parser = markParser.MarkParser()
parser.load(listPath)

for mark in parser.marks:
    img = cv2.imread(inputDir + '/' + mark.imageName)    
    common.drawPoligons(img, mark.poligons, (255,0,0))
    cv2.imshow('hello', img)
    k = cv2.waitKey(0)
    if k == ord('q'):
        cv2.destroyAllWindows()
        quit()

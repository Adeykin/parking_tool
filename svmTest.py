"""
Description: test pretrained classifier
"""

import sklearn
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import csv
import cPickle

inputPositive = '/home/adeykin/projects/parking/115000004/images/2/positive.csv'
inputNegative = '/home/adeykin/projects/parking/115000004/images/2/negative.csv'

positiveFile = open(inputPositive,'r')
negativeFile = open(inputNegative,'r')

negReader = csv.reader(negativeFile, delimiter=';')
neg = []
for row in negReader:
    neg.append(row)
    
posReader = csv.reader(positiveFile, delimiter=';')
pos = []
for row in posReader:
    pos.append(row)
    
X = neg + pos
Y = [0]*len(neg) + [1]*len(pos)

with open('AdaBoost_1_full.pkl', 'rb') as fid:
    classifier = cPickle.load(fid)

acc = classifier.score(X,Y)
print "Acc" + str(acc)

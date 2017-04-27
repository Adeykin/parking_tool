"""
Description: train an svm clessifier
"""

import sklearn
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import csv
import cPickle

inputPositive = '/home/adeykin/projects/parking/115000004/images/1/positive.csv'
inputNegative = '/home/adeykin/projects/parking/115000004/images/1/negativeExtend.csv'

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

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

classifier = AdaBoostClassifier()
classifier.fit(X_train, y_train)

print 'finish traning'

with open('AdaBoost_1_fullExtend.pkl', 'wb') as fid:
    cPickle.dump(classifier, fid)
    
acc = classifier.score(X_test,y_test)
print "Acc" + str(acc)
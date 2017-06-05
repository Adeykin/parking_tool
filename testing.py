import os, sys
import numpy as np
import csv
import cPickle
from itertools import islice, tee
import sklearn
import io

class Estimator:
    def __init__(self, classifier):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.classifier = classifier
        
    def appendData(self, dataset, y):
        y_fact = self.classifier.predict(dataset)
        posNum = y_fact.sum()
        negNum = len(y_fact) - posNum
        if y == 0:
            self.TN += negNum
            self.FP += posNum
        else:
            self.TP += posNum
            self.FN += negNum

    def prec(self):
        return float(self.TP)/(self.TP+self.FP)
    
    def acc(self):
        return float(self.TP+self.TN)/(self.TP+self.TN+self.FP+self.FN)
        
    def recall(self):
        return float(self.TP)/(self.TP+self.FN)
        
    def f1score(self):
        prec = self.prec()
        recall = self.recall()
        return 2.0*float(prec*recall)/(prec+recall)

def getChunk(infile, N=1000):
    while True:
        gen = islice(infile,N)
        it1, it2 = tee(gen)
        if next(it1,None) == None:
            break
        arr = np.genfromtxt(it2, dtype=None, delimiter=';')
        yield arr


def test(dataPath, estimator, y):
    f = open(dataPath, 'r')
    gen = getChunk(f)
    while True:
        try:
            arr = gen.next()
            #print "Log:" + str(y) + " read size: " + str(arr.shape)
            estimator.appendData(arr, y)
        except StopIteration:
            break

###### Main

if len(sys.argv) != 4:
    print 'USAGE: testing.py <classifierPath> <posPath> <negPath>'
    quit()
classifierPath = sys.argv[1]
posPath = sys.argv[2]
negPath = sys.argv[3]

with open(classifierPath, 'rb') as fid:
    classifier = cPickle.load(fid)
estimator = Estimator(classifier)

test(negPath, estimator, 0)
test(posPath, estimator, 1)

prec = str(estimator.prec())
acc = str(estimator.acc())
recall = str(estimator.recall())
f1score = str(estimator.f1score())
l = [classifierPath, posPath, negPath, prec, acc, recall, f1score]
print ';'.join(l)
"""
print estimator.prec()
print estimator.acc()
print estimator.recall()
print estimator.f1score()
"""

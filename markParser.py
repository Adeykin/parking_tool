import numpy as np
import common

class Mark:
    def __init__(self, imageName, poligons):
        self.imageName = imageName
        self.poligons = poligons

class MarkParser:
    def __init__(self):
        self.marks = []

    def load(self, file):
        self.marks = []
        listFile = open(file, 'r')
        for line in listFile:
            lineArr = line.split(' ')
            imgName = lineArr[0]
            lineArr = map(int,lineArr[1:])
            assert len(lineArr)%8 == 0
            number = len(lineArr) / 8
            localPoligons = []
            for i in range(number):
                offset = i*8;
                poligon = np.asarray(lineArr[offset:offset+8]).reshape(4,2)
                
                #detecting triangle
                lines = common.linesLengths(poligon.astype(dtype=int))
                if 0 in lines:
                    print "triangle"
                
                localPoligons.append(poligon)
            self.marks.append( Mark(imgName, localPoligons) )
    
    def save(self, file):
        listFile = open(file, 'w')
        for mark in self.marks:
            cells = []
            cells.append(mark.imageName)
            for poligon in mark.poligons:
                cells += poligon.reshape(1,8).astype(dtype=int).astype(dtype='str').tolist()[0]
            line = " ".join(cells)
            listFile.write( line + '\n' )
                    
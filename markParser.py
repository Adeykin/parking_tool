
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
                poligon = [(lineArr[offset+0], lineArr[offset+1]),
                           (lineArr[offset+2], lineArr[offset+3]),
                           (lineArr[offset+4], lineArr[offset+5]),
                           (lineArr[offset+6], lineArr[offset+7])]
                localPoligons.append(poligon)
            self.marks.append( Mark(imgName, localPoligons) )
    
    def save(self, file):
        listFile = open(file, 'w')
        for mark in self.marks:
            cells = []
            cells.append(mark.imageName)
            for pol in mark.poligons:
                for point in pol:
                    cells += map(str, list(point))
            line = " ".join(cells)
            listFile.write( line + '\n' )
                    
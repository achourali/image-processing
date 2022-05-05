import math

class Image:
    matrix=None
    type=""
    width=0
    height=0
    maxGray=0
    
    def __init__(self,pgmPath):
        file = open(pgmPath, 'rb')
        self.type = file.readline().decode().strip()
        line = file.readline()
        while chr(line[0]) == '#':
            line = file.readline()
        widthBinary, heightBinary = line.split()
        self.width, self.height = int(widthBinary), int(heightBinary)
        self.maxGray = int(file.readline())
        self.matrix = []
        if(self.type == "P5"):
            for i in range(self.height):
                row = list(file.read(self.width))
                self.matrix.append(row)
        elif(self.type == "P2"):
            for i in range(self.height):
                line = file.readline()
                row = line.split()
                row = list(map(int, row))
                self.matrix.append(row)
        
        file.close()
        
    def average(self):
        sum = 0
        for h in range(self.height):
            for w in range(self.width):
                sum += self.matrix[h][w]
        return sum / (self.width*self.height)
    
    
    def standard_deviation(self):
        average = self.average()
        sum = 0
        for h in range(self.height):
            for w in range(self.width):
                sum += (self.matrix[h][w] - average) ** 2
        return math.sqrt(sum / (self.width*self.height))
    
    
    def histogram(self):
        histogram = [0] * (self.maxGray + 1)
        for h in range(self.height):
            for w in range(self.width):
                histogram[self.matrix[h][w]] += 1
        return histogram
    
    
    def cumulated_histogram(self):
        histogram = self.histogram()
        cumulated_histogram = [0] * (self.maxGray + 1)
        cumulated_histogram[0] = histogram[0]
        for i in range(1, self.maxGray + 1):
            cumulated_histogram[i] = histogram[i] + cumulated_histogram[i - 1]
        return cumulated_histogram



        
class Image:
    matrix=None
    type=""
    width=0
    height=0
    max=0
    
    def __init__(self,pgmPath):
        file = open(pgmPath, 'rb')
        self.type = file.readline().decode().strip()
        line = file.readline()
        while chr(line[0]) == '#':
            line = file.readline()
        widthBinary, heightBinary = line.split()
        self.width, self.height = int(widthBinary), int(heightBinary)
        self.max = int(file.readline())
        self.matrix = []
        if(self.type == "P5"):
            for i in range(self.height):
                row = list(file.read(self.width))
                self.matrix.append(row)
        elif(self.type == "P2"):
            for i in range(height):
                line = file.readline()
                row = line.split()
                row = list(map(int, row))
                self.matrix.append(row)
        
        file.close()
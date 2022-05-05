import math
import numpy as np
import time
from random import randrange


class Image:
    matrix = None
    type = ""
    width = 0
    height = 0
    max_gray = 0

    def __init__(self, matrix=None, type="", width=0, height=0, max_gray=0):
        self.matrix = matrix
        self.type = type
        self.width = width
        self.height = height
        self.max_gray = max_gray

    def load_from_pgm(self, pgmPath):

        file = open(pgmPath, 'rb')
        self.type = file.readline().decode().strip()
        line = file.readline()
        while chr(line[0]) == '#':
            line = file.readline()
        width_binary, height_binary = line.split()
        self.width, self.height = int(width_binary), int(height_binary)
        self.max_gray = int(file.readline())
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
        histogram = [0] * (self.max_gray + 1)
        for h in range(self.height):
            for w in range(self.width):
                histogram[self.matrix[h][w]] += 1
        return histogram

    def cumulated_histogram(self):
        histogram = self.histogram()
        cumulated_histogram = [0] * (self.max_gray + 1)
        cumulated_histogram[0] = histogram[0]
        for i in range(1, self.max_gray + 1):
            cumulated_histogram[i] = histogram[i] + cumulated_histogram[i - 1]
        return cumulated_histogram

    def saturation_transformation(self, saturation_points):
        # points in an array of tuples (x,y)
        trans_x = [0]
        trans_y = [0]

        for point in saturation_points:
            x, y = point
            trans_x.append(x)
            trans_y.append(y)

        trans_x.append(self.max_gray)
        trans_y.append(self.max_gray)

        LUT = [0]*(self.max_gray+1)

        for g in range(self.max_gray+1):
            LUT[g] = int(np.interp(g, trans_x, trans_y))

        new_matrix = []

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(LUT[self.matrix[h][w]])
            new_matrix.append(row)

        new_image = Image(matrix=new_matrix, type="P2", width=self.width,
                          height=self.height, max_gray=self.max_gray)
        return new_image

    def save_to_pgm(self):

        f = open("samples/output/{0}.pgm".format(round(time.time())), "w")
        f.write("{0}\n{1} {2}\n{3}\n".format(
            self.type, self.width, self.height, self.max_gray))

        for h in range(self.height):
            f.write(' '.join([str(elem) for elem in self.matrix[h]])+'\n')
        f.close()

    def histogram_equalizer(self):

        cumulated_histogram = self.cumulated_histogram()
        LUT = [0] * (self.max_gray + 1)
        for i in range(self.max_gray + 1):
            LUT[i] = int(self.max_gray * cumulated_histogram[i] /
                         (self.height*self.width))
        new_matrix = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(LUT[self.matrix[h][w]])
            new_matrix.append(row)

        new_image = Image(matrix=new_matrix, type="P2", width=self.width,
                          height=self.height, max_gray=self.max_gray)
        return new_image

    def generate_random_noise(self):
        new_matrix = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                random_val = randrange(21)
                if(random_val == 0):
                    row.append(0)
                elif(random_val == 20):
                    row.append(255)
                else:
                    row.append(self.matrix[h][w])
            new_matrix.append(row)

        new_image = Image(matrix=new_matrix, type="P2", width=self.width,
                          height=self.height, max_gray=self.max_gray)
        return new_image

    def median_filter(self, size):
        if (size % 2 == 0):
            raise Exception('filter size must be odd')

        new_matrix = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                pixels = []

                for fh in range(h-size//2, h+size//2):
                    for fw in range(w-size//2, w+size//2):
                        if(fh < 0 or fh >= self.height or fw < 0 or fw >= self.width):
                            continue
                        else:
                            pixels.append(self.matrix[fh][fw])

                pixels.sort()
                median = pixels[len(pixels)//2]
                row.append(median)
            new_matrix.append(row)

        new_image = Image(matrix=new_matrix, type="P2", width=self.width,
                          height=self.height, max_gray=self.max_gray)
        return new_image

    def average_filter(self, size):
        if (size % 2 == 0):
            raise Exception('filter size must be odd')

        new_matrix = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                pixels = []

                for fh in range(h-size//2, h+size//2):
                    for fw in range(w-size//2, w+size//2):
                        if(fh < 0 or fh >= self.height or fw < 0 or fw >= self.width):
                            continue
                        else:
                            pixels.append(self.matrix[fh][fw])
                average = sum(pixels)/len(pixels)
                row.append(int(average))
            new_matrix.append(row)

        new_image = Image(matrix=new_matrix, type="P2", width=self.width,
                          height=self.height, max_gray=self.max_gray)
        return new_image

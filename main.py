from GUI import GUI
from Image import Image
# gui=GUI()


path1='samples/github.pgm'
path2="samples/feep.ascii.pgm"

image=Image(path1)
# print(image.average())
# print(image.standard_deviation())
# print(image.histogram())
# print(image.cumulated_histogram())

image.saturation_transformation([(3,0),(100,image.maxGray)])


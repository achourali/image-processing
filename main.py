from GUI import GUI
from Image import Image
# gui=GUI()


path1='samples/github.pgm'
path2="samples/feep.ascii.pgm"

image=Image()
image.load_from_pgm(path1)
# print(image.average())
# print(image.standard_deviation())
# print(image.histogram())
# print(image.cumulated_histogram())

newImageMatrix=image.saturation_transformation([(3,0),(100,image.maxGray)])
image.saveNewImage(newImageMatrix)


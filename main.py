from GUI import GUI
from Image import Image
# gui=GUI()


path1 = 'samples/github.pgm'
path2 = "samples/feep.ascii.pgm"

image = Image()
image.load_from_pgm(path1)
# print(image.average())
# print(image.standard_deviation())
# print(image.histogram())
# print(image.cumulated_histogram())

new_image = image.histogram_equalizer()
new_image.save_to_pgm()

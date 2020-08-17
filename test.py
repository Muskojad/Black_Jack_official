import numpy
import pygame

def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    #luminosity filter
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)
img = pygame.image.load(3_kier.png)
grayscale(img)
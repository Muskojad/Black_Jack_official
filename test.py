import pickle
import pygame

class favorite_color:
    def __init__(self):
        self.cos = 5
        #self.font = pygame.font.Font("OpenSans-Regular.ttf", 25)

fav = favorite_color()

pickle.dump( fav, open( "save.p", "wb" ) )
del fav
favorite = pickle.load( open( "save.p", "rb" ) )
fav = favorite
print(fav.cos)
import pygame
from rocket import Rocket

class Game(object):
    def __init__(self):
        self.ms_max = 50.0
        pygame.init()
        self.window = pygame.display.set_mode((1000, 700))
        self.time = 0.0
        self.clock = pygame.time.Clock()
        self.work = True
        self.kwadrat = pygame.Rect(10, 50, 134, 123)

        self.player = Rocket(self)

        while self.work:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.work = False
            # ograniczenie ilości klatek

            self.time += self.clock.tick()
            if self.time >= self.ms_max :
                self.time = 0.0
                self.tick()
            self.draw()


    def tick(self):
        self.window.fill((0, 0, 0))
        key_lib =  pygame.key.get_pressed()
        if key_lib[pygame.K_UP]:
            self.kwadrat.y -= 1
        if key_lib[pygame.K_DOWN]:
            self.kwadrat.y += 1

        if key_lib[pygame.K_LEFT]:
            self.kwadrat.x -= 1
        if key_lib[pygame.K_RIGHT]:
            self.kwadrat.x += 1


        self.player.tick()
    def draw(self):
        self.window.fill((0,0,0))
        pygame.draw.rect(self.window,(100,100,100),self.kwadrat)
        pygame.display.flip()

print("dziala2")
if __name__ == "__main__":
    print("dziala")
    klasa = Game()

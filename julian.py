import pygame
from pygame.locals import *
import time
import os

class Map(object):

    def __init__(self,size):
        self.window_size = size

class Player(object):

    def __init__(self,height,width,pos):
        self.height = height
        self.width = width
        self.pos = pos

class Model(object):

    def __init__(self,size,player,mmap):
        self.window_size = size
        self.player = player
        self.map = mmap

class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        pygame.draw.rect(self.screen, # Draw note block
                         (0,255,0),
                         pygame.Rect(0,
                                     851,
                                     1860,
                                     170))
        pygame.draw.rect(self.screen,
                         (0,0,255),
                         pygame.Rect(self.model.player.pos[0],
                                     self.model.player.pos[1],
                                     self.model.player.width,
                                     self.model.player.height))
        pygame.display.update()


class PyGameKeyboardController(object):

    def __init__(self,model):
        self.model = model

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.model.player.pos[0] -= 5
            return
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.model.player.pos[0] += 5
            return
            return
        return

if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    mmap = Map(size)
    player = Player(170,85,[0,680])
    model = Model(size,player,mmap)
    view = PyGameWindowView(size,model)
    controller = PyGameKeyboardController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        controller.handle_movement()
        view.draw()
        time.sleep(.001)

    pygame.quit()

import pygame
from pygame.locals import *
import time
import os

class Map(object):

    def __init__(self,size):
        self.window_size = size

class Player(object):

    def __init__(self,height):
        self.height = height

class Model(object):

    def __init__(self,size,player,mmap):
        self.window_size = size
        self.player = player
        self.map = mmap

class PyGameWindowView(object):

    def __init__(self,size):
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))

        pygame.display.update()


class PyGameKeyboardController(object):

    def __init__(self,model):
        self.model = model

if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    view = PyGameWindowView(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        view.draw()
        time.sleep(.001)

    pygame.quit()

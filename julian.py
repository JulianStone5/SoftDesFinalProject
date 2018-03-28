import pygame
from pygame.locals import *
import time
import os

class Map(object):

    def __init__(self):

class Player(object):

    def __init__(self):

class PyGameWindowView(object):

    def __init__(self):


class PyGameKeyboardController(object):

    def __init__(self):


if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        time.sleep(.001)

    pygame.quit()

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
        self.gravity = .1
        self.vy = 0
        self.jump1 = False
        self.jump2 = False

class Model(object):

    def __init__(self,size,player,mmap):
        self.window_size = size
        self.player = player
        self.map = mmap

    def grav_effect(self):
        self.player.pos[1] += self.player.vy
        self.player.vy += self.player.gravity
        if self.player.pos[1] + self.player.height >= 851:
            self.player.pos[1] = 851 - self.player.height
            self.player.vy = 0
            self.player.jump1 = False
            self.player.jump2 = False


class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        pygame.draw.rect(self.screen,
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

    def handle_jump(self):
        if not view.model.player.jump1:
            view.model.player.vy = -8
            view.model.player.jump1 = True
        elif not view.model.player.jump2:
            view.model.player.vy = -8
            view.model.player.jump2 = True
        return

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.model.player.pos[0] -= 5
            return
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.model.player.pos[0] += 5
            return

if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    mmap = Map(size)
    player = Player(170,85,[0,681])
    model = Model(size,player,mmap)
    view = PyGameWindowView(size,model)
    controller = PyGameKeyboardController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and (event.key == pygame.K_UP or
                                          event.key == pygame.K_w):
                controller.handle_jump()
        controller.handle_movement()
        model.grav_effect()
        view.draw()
        time.sleep(.001)

    pygame.quit()

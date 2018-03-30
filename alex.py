import pygame
from pygame.locals import *
import time
import os

class Map(object):

    def __init__(self,size):
        self.window_size = size
        self.floor = pygame.Rect(0, # defines the floor postion and size
                    851,
                    1860,
                    170)
class Player(object):

    def __init__(self,height,width,pos):
        self.height = height
        self.width = width
        self.pos = pos
        #define players pos and demision so rep as Rectangle and colltion and draw are easy
        self.hit_box = pygame.Rect(self.pos[0],
                    self.pos[1],
                    self.width,
                    self.height)
        self.gravity = .12
        self.vy = 8
        self.jump1 = False
        self.jump2 = False

class Model(object):

    def __init__(self,size,player,mmap):
        self.window_size = size
        self.player = player
        self.map = mmap

    def grav_effect(self):
        self.player.hit_box.y += self.player.vy # pos[1]  to y becasue syntax
        self.player.vy += self.player.gravity
        #if self.player.hit_box.y + self.player.height >= 851:
        if self.player.hit_box.colliderect(self.map.floor): # colition
            self.player.hit_box.y = 851 - self.player.height
            self.player.vy = 0
            self.player.jump1 = False
            self.player.jump2 = False


class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        pygame.draw.rect(self.screen, #this  draws the block
                         (0,255,0),
                         self.model.map.floor) #
                         # pygame.Rect(0,
                         #             851,
                         #             1860,
                         #             170))
        pygame.draw.rect(self.screen, #this draws the player
                         (0,0,255),
                         self.model.player.hit_box) # made short 
                         # pygame.Rect(self.model.player.pos[0],
                         #             self.model.player.pos[1],
                         #             self.model.player.width,
                         #             self.model.player.height))
        pygame.display.update()


class PyGameKeyboardController(object):

    def __init__(self,model):
        self.model = model

    def handle_jump(self,event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            if not self.model.player.jump1:
                self.model.player.vy = -8
                #self.model.player.hit_box.y += self.model.player.vy
                self.model.player.jump1 = True
                return
            if not self.model.player.jump2:
                self.model.player.vy = -8
                #self.model.player.hit_box.y += self.model.player.vy
                self.model.player.jump2 = True
                return
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.model.player.vy = 5
        return

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.model.player.hit_box.x -= 5 #change pos[0] to x because syntax
            return
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.model.player.hit_box.x += 5 # same as above
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
            controller.handle_jump(event)
        controller.handle_movement()
        model.grav_effect()
        view.draw()
        time.sleep(.001)

    pygame.quit()

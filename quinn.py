import pygame
from pygame.locals import *
import time
import os

class Map(pygame.sprite.Sprite):

    def __init__(self,size):
        #self.window_size = size
        self.block1 = pygame.Rect(0,
                    935,
                    255,
                    85)
        self.block2 = pygame.Rect(255,
                    765,
                    170,
                    255)
        self.block3 = pygame.Rect(595,
                    425,
                    255,
                    595)
        self.block4 = pygame.Rect(850,
                    595,
                    340,
                    425)
        self.block5 = pygame.Rect(1190,
                    510,
                    255,
                    510)
        self.block6 = pygame.Rect(1275,
                    680,
                    170,
                    340)
        self.block7 = pygame.Rect(1445,
                    595,
                    255,
                    425)
        #self.block_list = pygame.sprite.Group()
        self.blocks = [self.block1, self.block2,self.block3,self.block4,self.block5,self.block6,self.block7]
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
        for i in self.map.blocks:
            if self.player.hit_box.colliderect(i): # colition
                self.player.hit_box.y = i.y - self.player.height
                self.player.vy = 0
                self.player.jump1 = False
                self.player.jump2 = False


class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for i in self.model.map.blocks:
            pygame.draw.rect(self.screen,
                         (0,255,0), i)
        pygame.draw.rect(self.screen,
                         (0,0,255),
                         self.model.player.hit_box)
        pygame.display.update()


class PyGameKeyboardController(object):

    def __init__(self,model):
        self.model = model
        self.up_uncl = True # Ensures double jump only after key is released between jumps

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_w] and not keys[pygame.K_UP]:
            self.up_uncl = True # Verifies that the jump key has been unclicked
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.model.player.hit_box.x -= 5 #change pos[0] to x because syntax
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.model.player.hit_box.x += 5 # same as above
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if not self.model.player.jump1 and self.up_uncl:
                self.model.player.vy = -8 # Set up-velocity to initialize jump
                self.model.player.jump1 = True # Mark first jump
                self.up_uncl = False # Say that the jump key has been clicked
            elif not self.model.player.jump2 and self.up_uncl:
                self.model.player.vy = -8
                self.model.player.jump2 = True # Mark second jump
                self.up_uncl = False
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.model.player.vy = 5 # Move player down

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
        controller.handle_movement()
        model.grav_effect()
        view.draw()
        time.sleep(.001)

    pygame.quit()

    pygame.quit()

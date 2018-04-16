import pygame
from pygame.locals import *
from player import *

class Obstacle(Player):

    def __init__(self,x,y,width,height,ty):
        self.hit_box = pygame.Rect(x,y,width,height)
        self.is_main = False
        self.type = ty
        self.vx = 0
        self.vy = 0

class Enemy(Player):
    def __init__(self,x,y,width,height,ty=''):
        super(Enemy,self).__init__(x,y,width,height,False)
        self.type = ty
        if self.type == 'jump':
            self.vx = 0
            self.vy = -18
        else:
            self.vx = 4

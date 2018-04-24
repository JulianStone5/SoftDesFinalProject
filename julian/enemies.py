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

    def __init__(self,x,y,width,height,ty='',VstartX=0,VstartY=0,lives=1):
        super(Enemy,self).__init__(x,y,width,height,False)
        self.type = ty
        self.lives = lives
        self.vx = VstartX
        self.mov_right = False
        if self.type == 'jump':
            self.vy = -VstartY

class Elite(Enemy):

    def __init__(self,x,y,width,height,ty='elite',VstartX=2,VstartY=0,lives=3):
        super(Elite,self).__init__(x,y,width,height,ty,VstartX,VstartY,lives)

    def follow(self, player):
        midplayer = player.hit_box.x+player.hit_box.w//2
        midself = self.hit_box.x+self.hit_box.w//2
        if midplayer < midself:
            self.hit_box = self.hit_box.move(-self.vx,0)
            self.mov_right = False
        else:
            self.hit_box = self.hit_box.move(self.vx,0)
            self.mov_right = True

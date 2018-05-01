import pygame
import math
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

    def __init__(self,x,y,width,height,ty='elite',VstartX=1.5,VstartY=0,lives=3):
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

class Flyer(object):
    def __init__(self,points,width,height,is_main=False,lives=1):
        #define players pos and demision so rep as Rectangle and colltion and draw are easy
        self.points = points
        self.hit_box = pygame.Rect(self.points[0][0],self.points[0][1],width,height)
        self.speed = 1
        self.lives = 1
        self.mov_right = False
        self.i = 0
        self.v = 4

    def Fly_movement(self):
        if self.points[self.i][0] == self.points[(self.i+1) %4][0] and self.points[self.i][1] < self.points[(self.i+1)%4][1]: # down
            if self.hit_box.y > self.points[(self.i+1)%4][1]:
                self.i = (self.i +1) %4
            self.hit_box = self.hit_box.move(0,self.speed)
        elif self.points[self.i][0] == self.points[(self.i+1)%4][0] and self.points[self.i][1] > self.points[(self.i+1)%4][1]: # up
            if self.hit_box.y < self.points[(self.i+1)%4][1]:
                self.i = (self.i +1) %4
            self.hit_box = self.hit_box.move(0,-self.speed)

        elif self.points[self.i][1] == self.points[(self.i+1)%4][1] and self.points[self.i][0] < self.points[(self.i+1)%4][0]:
            if self.hit_box.x > self.points[(self.i+1)%4][0]:
                self.i = (self.i +1) %4
            self.hit_box = self.hit_box.move(self.speed,0)
        elif self.points[self.i][1] == self.points[(self.i+1)%4][1] and self.points[self.i][0] > self.points[(self.i+1)%4][0]:
            if self.hit_box.x < self.points[(self.i+1)%4][0]:
                self.i = (self.i +1) %4
            self.hit_box = self.hit_box.move(-self.speed,0)

    def collision(self,map,game_over,player):
        g=0
class shoot(object):
    def __init__(self,player,Flyer):
        self.x = Flyer.hit_box.x
        self.y = Flyer.hit_box.y
        self.a = player.hit_box.x - Flyer.hit_box.x
        self.b = player.hit_box.y - Flyer.hit_box.y
        self.hit_box = pygame.Rect(self.x,self.y,10,10)
        self.z = math.sqrt((self.a**2) + self.b**2)
        self.v = 2
        self.Vx = self.v*(self.a/self.z)
        self.Vy = self.v*(self.b/self.z)
    def update_bullet(self):
        self.hit_box = self.hit_box.move(self.Vx,self.Vy)
        #self.hit_box = self.hit_box.move(4,0)

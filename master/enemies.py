import pygame
from pygame.locals import *
from player import *
import time
import random
import math

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
            self.VstartY = VstartY

class Elite(Enemy):

    def __init__(self,x,y,width,height,ty='elite',VstartX=2,VstartY=0,lives=3):
        super(Elite,self).__init__(x,y,width,height,ty,VstartX,VstartY,lives)
        self.att_box = self.att_box = pygame.Rect(x+width-20,self.hit_box.h//2+17,50,20)
        self.t_att = time.time()
        self.t_last = time.time()
        self.prox = 800

    def follow(self, player):
        if self.hit_box.x > player.hit_box.x+player.hit_box.w:
            self.hit_box = self.hit_box.move(-self.vx,0)
            self.mov_right = False
        elif self.hit_box.x+self.hit_box.w < player.hit_box.x:
            self.hit_box = self.hit_box.move(self.vx,0)
            self.mov_right = True

    def attack(self):
        t_since_att = time.time()-self.t_att
        if t_since_att >.15:
            self.att_animation = False
            if self.attacking:
                self.t_last = time.time()
                self.attacking = False
        t_since_last = time.time()-self.t_last
        if not self.attacking and t_since_last > .5:
            r = random.random()
            if r < .008:
                self.attacking = True
                self.att_animation = True
                self.t_att = time.time()


class Flyer(object):
    def __init__(self,points,width,height,speed,shooting=False,is_main=False,lives=1):
        #define players pos and demision so rep as Rectangle and colltion and draw are easy
        self.points = points
        self.hit_box = pygame.Rect(self.points[0][0],self.points[0][1],width,height)
        self.speed = speed
        self.lives = 1
        self.mov_right = False
        self.shooting = shooting
        self.i = 0
        self.t = time.time()

    def Fly_movement(self):
        num = len(self.points)
        if self.points[self.i][0] == self.points[(self.i+1) % num][0] and self.points[self.i][1] < self.points[(self.i+1) % num][1]: # down
            if self.hit_box.y > self.points[(self.i+1) % num][1]:
                self.i = (self.i +1) % num
            self.hit_box = self.hit_box.move(0,self.speed)
        elif self.points[self.i][0] == self.points[(self.i+1) % num][0] and self.points[self.i][1] > self.points[(self.i+1) % num][1]: # up
            if self.hit_box.y < self.points[(self.i+1) % num][1]:
                self.i = (self.i +1) % num
            self.hit_box = self.hit_box.move(0,-self.speed)

        elif self.points[self.i][1] == self.points[(self.i+1) % num][1] and self.points[self.i][0] < self.points[(self.i+1) % num][0]:
            if self.hit_box.x > self.points[(self.i+1) % num][0]:
                self.i = (self.i +1) % num
            self.hit_box = self.hit_box.move(self.speed,0)
        elif self.points[self.i][1] == self.points[(self.i+1) % num][1] and self.points[self.i][0] > self.points[(self.i+1) % num][0]:
            if self.hit_box.x < self.points[(self.i+1) % num][0]:
                self.i = (self.i +1) % num
            self.hit_box = self.hit_box.move(-self.speed,0)

    def shoot(self,player):
        if time.time() - self.t > 2:
            dist = 0
            if self.hit_box.x > player.hit_box.x+player.hit_box.w:
                dist = self.hit_box.x-player.hit_box.x+player.hit_box.w
            elif self.hit_box.x+self.hit_box.w < player.hit_box.x:
                dist = player.hit_box.x-self.hit_box.x+self.hit_box.w
            if dist < 1000:
                self.t = time.time()
                return shoot(player,self)
        return None

class shoot(object):

    def __init__(self,player,enemy,width=20,height=20):
        self.x = enemy.hit_box.x
        self.y = enemy.hit_box.y
        self.a = player.hit_box.x - enemy.hit_box.x
        self.b = player.hit_box.y - enemy.hit_box.y
        self.hit_box = pygame.Rect(self.x,self.y,width,height)
        self.z = math.sqrt((self.a**2) + self.b**2)
        self.v = 3
        self.Vx = self.v*(self.a/self.z)
        self.Vy = self.v*(self.b/self.z)

    def update_bullet(self):
        self.hit_box = self.hit_box.move(self.Vx,self.Vy)
        #self.hit_box = self.hit_box.move(4,0)

class Boss(Elite):

    def __init__(self,x,y,width,height,ty='boss',VstartX=2,VstartY=0,lives=5):
        super(Boss,self).__init__(x,y,width,height,ty,VstartX,VstartY,lives)
        self.att_box = self.att_box = pygame.Rect(x+width-30,self.hit_box.h//2+17,75,30)
        self.prox = 2000

    def jump(self):
        if abs(self.vy) < .25 and not self.jump1:
            r = random.random()
            if r < .01:
                self.vy = -10
                self.jump1 = True

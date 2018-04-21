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
    def __init__(self,x,y,width,height,ty='',VstartX=0,VstartY=0):
        super(Enemy,self).__init__(x,y,width,height,False)
        self.type = ty
        if self.type == 'jump':
            self.vx = VstartX
            self.vy = -VstartY
        else:
            self.vx = VstartX

class Flyer(object):
    def __init__(self,x,y,width,height,speed,is_main=False):
        #define players pos and demision so rep as Rectangle and colltion and draw are easy
        self.hit_box = pygame.Rect(x,y,width,height)
        self.speed = speed
        # self.p1 = [2570, 1035]
        # self.p2 = [2820,1035]
        self.p1 = [10,800]
        self.p2 = [10,600]
        self.p3 = [1000,600]
        self.p4 = [1000,800]
        self.points = [self.p1, self.p2, self.p3, self.p4]
        print(speed)
        self.i = 0
        # print(self.points[self.i][0])
        # print(self.points[self.i][1])
        # print(self.points[(self.i+1)%4][0])
        # print(self.points[(self.i+1)%4][1])

    def Fly_movement(self):

        if self.points[self.i%4][0] == self.points[(self.i+1)%4][0]:

            if self.points[self.i%4][1] < self.points[(self.i+1)%4][1]:
                if self.hit_box.y > self.points[(self.i+1)%4][1]:
                    self.i = self.i +1
                else:
                    self.hit_box= self.hit_box.move(0,self.speed)
            if self.points[self.i%4][1] > self.points[(self.i+1)%4][1]:
                if self.hit_box.y < self.points[(self.i+1)%4][1]:
                    self.i = self.i +1
                else:
                    self.hit_box= self.hit_box.move(0,-self.speed)

        if self.points[self.i%4][1] == self.points[(self.i+1)%4][1]9,:

            if self.points[self.i%4][0] < self.points[(self.i+1)%4][0]:
                if self.hit_box.x < self.points[(self.i+1)%4][0]:
                    self.i = self.i +1
                else:
                    self.hit_box= self.hit_box.move(-self.speed,0)
            if self.points[self.i%4][0] > self.points[(self.i+1)%4][0]:
                if self.hit_box.x > self.points[(self.i+1)%4][0]:
                    self.i = self.i +1
                else:
                    self.hit_box= self.hit_box.move(self.speed,0)

        # else:
        #     mvx = ((self.p1[1]-self.p2[1]) / (self.p1[0]-self.p2[0])) * self.speed
        #     mvy = ((self.p1[0]-self.p2[0]) / (self.p1[1]-self.p2[1])) * self.speed
        #     self.hit_box= self.hit_box.move(mvx,mvy)

import pygame
from pygame.locals import *
from enemies import *

class Map(object):

    def __init__(self,size,level=0):
        self.size = size
        self.level = level
        self.levelChanged = False
        self.story_text = [("Your castle that you once defended has been consumed by the darkness...",
                            "It has created monsters and corrupted friends that now walk the castle...",
                            "You must stop the darkness from spreading…"),#Story before start
                           ("Before you is the shell of your old home...",
                            "The castle gates are torn apart by the darkness...",
                            "A ray of light must enter the heavy shadow..."),#Story after level 1
                           ("Your fellow knights have fallen victim to dark corruption...",
                            "With remorse, you must relieve them from this state...",
                            "Their spirits thank you, but there is still no time to mourn..."),#Story after level 2
                           ("This is it. You have reached the king's room...",
                            "You feel a powerful dark energy...",
                            "Prepare yourself..."),#Story after level 3
                           ("The darkness fades, your sword shines brighter...",
                            "The darkness slivers away form the light…",
                            "The Castle is enveloped by a brilliant light...")]#Story after level 4
        self.death_box = pygame.Rect(-1000,self.size[1],50000,50)
        self.blocks = [self.death_box]
        self.enemies = []
        self.bullet = []
        self.doors = []
        self.make_level()

    def level1(self):
        self.death_box = pygame.Rect(-1000,self.size[1],50000,50)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.starter_block]
        self.bullet = []
        self.enemies = []
        self.tutorial = []
        self.tutorial.append([self.blocks[-1].x+50,self.blocks[-1].y-500,"Use A/D or the arrow keys to move"])
        self.add_smaller_block()
        self.add_smaller_block()
        self.tutorial.append([self.blocks[-1].x,self.blocks[-1].y-400,"Use W or the UP arrow to jump"])
        self.add_smaller_block()
        self.add_smaller_block()
        self.tutorial.append([self.blocks[-1].x,self.blocks[-1].y-500,"You can double jump too!"])
        self.add_small_block()
        self.add_tall_block()
        self.add_tall_block()
        self.add_small_block()
        self.add_small_block()
        self.tutorial.append([self.blocks[-1].x,self.blocks[-1].y-400,"Beware of enemies!"])
        self.tutorial.append([self.blocks[-1].x,self.blocks[-1].y-350,'Press SPACE to attack!'])
        self.add_smaller_block()
        self.add_basic_enemy(self.blocks[-1].x+100,self.blocks[-1].y-125)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_tall_block()
        self.add_tall_block()
        self.add_chasm()
        self.add_tall_block()
        self.add_tall_block()
        self.add_chasm()
        self.add_jump_enemy(self.blocks[-1].x+90,self.blocks[-1].y-175)
        self.add_tall_block()
        self.add_tall_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_floating_down_block()
        self.add_wide_floating_down_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_floating_down_block()
        self.add_jump_enemy(self.blocks[-1].x+90,self.blocks[-1].y-175)
        self.add_floating_up_block()
        self.add_wide_floating_up_block()

    def level2(self):
        self.death_box = pygame.Rect(-1000,self.size[1],100000,50)
        self.ceiling_box = pygame.Rect(-200,-100,10000-120,200)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box]
        self.bullet = []
        for i in range(40):
            rect = pygame.Rect(i*252-200,-100,252,200)
            self.blocks.append(rect)
        self.blocks.append(self.starter_block)
        self.enemies = []
        self.doors = []
        self.add_small_block()
        self.add_thin_block()
        self.add_tall_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_basic_enemy(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_square(500,150,150)
        x = self.blocks[len(self.blocks)-2].x-185
        y = self.blocks[len(self.blocks)-2].y-185
        w = 385
        h = 385
        points = [[x,y],[x,y+h],[x+w,y+h],[x+w,y]]
        self.add_flyer(points,2,True)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_block()
        self.add_smaller_block()
        x = self.blocks[-1].x+self.blocks[-1].w//2
        y = 300
        points = [[x,y],[x,y+h]]
        self.add_flyer(points,4)
        self.add_smaller_block()
        self.add_smaller_block()
        x = self.blocks[-1].x+self.blocks[-1].w//2
        points = [[x,y+h],[x,y]]
        self.add_flyer(points,4)
        self.add_block()
        self.add_smaller_block()
        self.add_elite(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_door_lock()
        self.add_smaller_block()
        self.add_basic_enemy(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_square(450,350,100)
        self.add_smaller_block()
        self.add_smaller_block()
        x = self.blocks[-1].x+self.blocks[-1].w//2+150
        points = [[x,y+h],[x,y]]
        self.add_flyer(points,2,True)
        self.add_smaller_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_basic_enemy(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_square(450,350,100)
        x = self.blocks[len(self.blocks)-2].x-185
        y = self.blocks[len(self.blocks)-2].y-185
        w = 635
        h = 385
        points = [[x+w,y+h],[x+w,y],[x,y],[x,y+h]]
        self.add_flyer(points,4)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_square(450,350,100)
        x = self.blocks[len(self.blocks)-2].x-185
        y = self.blocks[len(self.blocks)-2].y-185
        points = [[x,y],[x,y+h],[x+w,y+h],[x+w,y]]
        self.add_flyer(points,4)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_smaller_block()
        x = self.blocks[-1].x+self.blocks[-1].w//2
        y = 300
        points = [[x,y],[x,y+h]]
        self.add_flyer(points,4)
        self.add_basic_enemy(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_smaller_block()
        self.add_smaller_block()
        x = self.blocks[-1].x+self.blocks[-1].w//2
        points = [[x,y+h],[x,y]]
        self.add_flyer(points,4)
        self.add_small_block()
        self.add_thin_block()
        self.add_chasm()
        self.add_jump_enemy(self.blocks[-1].x+90,self.blocks[-1].y-175,v=16)
        self.add_thin_block()
        self.add_smaller_block()
        self.add_square(450,400,75)
        self.add_basic_enemy(self.blocks[-2].x,self.blocks[-2].y-125)
        self.add_square_bump(400)
        self.add_smaller_block()
        self.add_elite(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_square(250,400,75)
        self.add_basic_enemy(self.blocks[-2].x+100,self.blocks[-2].y-125)
        self.add_square_bump(200)
        self.add_square(600,400,75)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_square(450,400,75)
        self.add_basic_enemy(self.blocks[-2].x+50,self.blocks[-2].y-125)
        self.add_square_bump(400)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_door_drop()
        self.add_elite(self.doors[-1].x+10,self.doors[-1].y-125)
        self.add_smaller_block()
        self.add_door_lock()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()

    def level3(self):
        self.death_box = pygame.Rect(-1000,self.size[1],1000000,50)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.starter_block]
        self.enemies = []
        self.doors = []
        self.add_small_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        x = self.blocks[-3].x
        y = self.blocks[-1].y-200
        w = 500
        points = [[x,y],[x+w,y]]
        self.add_flyer(points,2,True)
        self.add_floating_up_block()
        self.add_wide_floating_up_block()
        self.add_floating_down_block()
        self.add_floating_down_block()
        self.add_wide_floating_down_block()
        x = self.blocks[-1].x+self.blocks[-1].w//2
        y = self.blocks[-1].y - 700
        h = 385
        points = [[x,y],[x,y+h]]
        self.add_flyer(points,2,True)
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_floating_down_block()
        x = self.blocks[-3].x
        y = self.blocks[-1].y-700
        w = 500
        points = [[x,y],[x+w,y]]
        self.add_flyer(points,2)
        self.add_floating_down_block()
        self.add_floating_down_block()
        self.add_jump_enemy(self.blocks[-1].x+90,self.blocks[-1].y-175,v=16)
        self.add_wide_floating_up_block()
        self.add_wide_floating_up_block()
        self.add_square_bump(self.blocks[-1].y+self.blocks[-1].h-125,pos=-1)
        self.add_basic_enemy(self.blocks[-1].x+100,self.blocks[-1].y-125)
        self.add_wide_floating_down_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        x = self.blocks[-3].x-200
        y = self.blocks[-1].y-250
        w = 500
        points = [[x,y],[x+w,y]]
        self.add_flyer(points,2,True)
        x = x+250
        y = self.blocks[-1].y - 550
        h = 385
        points = [[x,y],[x,y+h]]
        self.add_flyer(points,2)
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_wide_floating_up_block()
        self.add_wide_floating_block()
        self.add_wide_floating_block()
        self.add_wide_floating_block()
        self.add_elite(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_wide_floating_block()
        self.add_wide_floating_block()
        self.add_door_lock()
        self.add_wide_floating_block()
        self.add_floating_down_block()
        self.add_floating_down_block()
        self.add_floating_down_block()
        self.add_floating_down_block()
        self.add_floating_down_block()
        self.add_last_box()
        self.add_tall_block()
        self.add_chasm()
        self.add_jump_enemy(self.blocks[-1].x+90,self.blocks[-1].y-175,v=17)
        self.add_tall_block()
        self.add_thin_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_floating_up_block()
        self.add_wide_floating_up_block()
        self.add_wide_floating_block()
        self.add_wide_floating_block()
        x = self.blocks[-1].x
        y = self.blocks[-1].y-600
        w = 500
        points = [[x,y],[x+w,y]]
        self.add_flyer(points,2,True,3)
        x = self.blocks[-1].x
        y = self.blocks[-1].y-700
        w = 500
        points = [[x+w,y],[x,y]]
        self.add_flyer(points,2,True,3)
        self.add_wide_floating_block()
        self.add_elite(self.blocks[-1].x,self.blocks[-1].y-125)
        self.add_wide_floating_block()
        self.add_wide_floating_block()
        self.add_door_lock()
        self.add_wide_floating_block()

    def level4(self):
        self.death_box = pygame.Rect(-1000,self.size[1],100000,50)
        self.death_box = pygame.Rect(-1000,self.size[1],100000,50)
        self.ceiling_box = pygame.Rect(-200,-100,10000-120,200)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box]
        for i in range(20):
            rect = pygame.Rect(i*252-200,-100,252,200)
            self.blocks.append(rect)
        self.blocks.append(self.starter_block)
        self.enemies = []
        self.add_small_block()
        self.add_thin_block()
        self.add_tall_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_boss(self.blocks[-1].x,self.blocks[-1].y-250)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_door_lock()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()

    def make_level(self):
        if self.level == 1:
            self.level1()
        elif self.level == 2:
            self.level2()
        elif self.level == 3:
            self.level3()
        elif self.level == 4:
            self.level4()

    def side_scroll(self,amount):
        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i].move(amount,0)
        for i in range(len(self.bullet)):
            self.bullet[i].hit_box = self.bullet[i].hit_box.move(amount,0)
        for i in range(len(self.doors)):
            self.doors[i] = self.doors[i].move(amount,0)
        for i in range(len(self.enemies)):
            self.enemies[i].hit_box = self.enemies[i].hit_box.move(amount,0)
            if type(self.enemies[i]) == Flyer:
                for j in range(len(self.enemies[i].points)):
                    self.enemies[i].points[j][0] += amount
        if self.level != 1:
            return
        for i in range(len(self.tutorial)):
            self.tutorial[i][0] += amount

    def vert_scroll(self,amount):
        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i].move(0,amount)
        for i in range(len(self.bullet)):
            self.bullet[i].hit_box = self.bullet[i].hit_box.move(0,amount)
        for i in range(len(self.doors)):
            self.doors[i] = self.doors[i].move(0,amount)
        for i in range(len(self.enemies)):
            self.enemies[i].hit_box = self.enemies[i].hit_box.move(0,amount)
            if type(self.enemies[i]) == Flyer:
                for j in range(len(self.enemies[i].points)):
                    self.enemies[i].points[j][1] += amount
        if self.level != 1:
            return
        for i in range(len(self.tutorial)):
            self.tutorial[i][1] += amount

    def add_block(self,width=250,height=500):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        y = last_block.y + last_block.h - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_tall_block(self,width=250,height=600):
        self.add_block(width,height)

    def add_thin_block(self, width=125, height=500):
        self.add_block(width,height)

    def add_small_block(self,width=250,height=250):
        self.add_block(width,height)

    def add_smaller_block(self,width=250,height=85):
        self.add_block(width,height)

    def add_chasm(self,width=250,height=50):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        block = pygame.Rect(x,self.size[1]+50,width,height)
        self.blocks.append(block)

    def add_square(self,y=500,width=150,height=150):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        block = pygame.Rect(x,y,width,height)
        self.blocks.insert(len(self.blocks)-1,block)

    def add_square(self,y=500,width=150,height=150):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        block = pygame.Rect(x,y,width,height)
        self.blocks.insert(len(self.blocks)-1,block)

    def add_square_bump(self,y=500,width=95,height=125,pos=-2):
        last_block = self.blocks[pos]
        x = last_block.x - width
        block = pygame.Rect(x,y,width,height)
        self.blocks.insert(len(self.blocks)-1,block)
        x = last_block.x + last_block.w
        block = pygame.Rect(x,y,width,height)
        self.blocks.insert(len(self.blocks)-1,block)

    def add_floating_up_block(self,width=200,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w + 70
        y = last_block.y - 200 - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_wide_floating_up_block(self,width=400,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w + 70
        y = last_block.y - 200 - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_floating_down_block(self,width=200,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w + 70
        y = last_block.y + 315 - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_wide_floating_down_block(self,width=400,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w + 70
        y = last_block.y + 315 - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_wide_floating_block(self,width=400,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        y = last_block.y
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_last_box(self,width=250,height=510):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        y = 510
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_door_lock(self,width=142,height=195):
        last_block = self.blocks[-1]
        x = last_block.x
        y = last_block.y-height
        block = pygame.Rect(x,y,width,height)
        self.doors.append(block)
        block = pygame.Rect(x,y-1000,width,1000)
        self.blocks.insert(len(self.blocks)-1,block)

    def add_door_drop(self,width=142,height=195):
        last_block = self.blocks[-1]
        x = last_block.x
        y = -200
        block = pygame.Rect(x,y,width,height)
        self.doors.append(block)
        block = pygame.Rect(x-100,y-100,100,100)
        self.blocks.insert(len(self.blocks)-1,block)
        block = pygame.Rect(x+width,y-100,100,100)
        self.blocks.insert(len(self.blocks)-1,block)

    def add_basic_enemy(self,x,y,width=85,height=125):
        enemy = Enemy(x,y,width,height,'basic',3)
        self.enemies.append(enemy)

    def add_jump_enemy(self,x,y,width=85,height=125,v=18):
        enemy = Enemy(x,y,width,height,'jump',0,v)
        self.enemies.append(enemy)

    def add_elite(self,x,y,width=85,height=125):
        enemy = Elite(x,y,width,height)
        self.enemies.append(enemy)

    def add_flyer(self,points,speed,shooting=False,st=2,width=85,height=85):
        enemy_fly = Flyer(points,width,height,speed,shooting,st)
        self.enemies.append(enemy_fly)

    def add_boss(self,x,y,width=128,height=188):
        enemy = Boss(x,y,width,height)
        self.enemies.append(enemy)

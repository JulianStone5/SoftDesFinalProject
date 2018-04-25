import pygame
from pygame.locals import *
from enemies import *

class Map(pygame.sprite.Sprite):

    def __init__(self,size,level=0):
        self.size = size
        self.level = level
        self.levelChanged = False
        self.story_text = [("Story Stuff...","Story Stuff...","Story Stuff..."),#Story before start
                           ("Story Stuff...","Story Stuff...","Story Stuff..."),#Story after level 1
                           ("Story Stuff...","Story Stuff...","Story Stuff..."),#Story after level 2
                           ("Story Stuff...","Story Stuff...","Story Stuff..."),#Story after level 3
                           ("Story Stuff...","Story Stuff...","Story Stuff...")]#Story after level 4
        self.death_box = pygame.Rect(-1000,self.size[1],50000,50)
        self.blocks = [self.death_box]
        self.enemies = []
        self.obstacles = []
        self.make_level()

    def level1(self):
        self.death_box = pygame.Rect(-1000,self.size[1],50000,50)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.starter_block]
        self.obstacles = []
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
        points = [[10,600],[1000,600],[1000,800],[10,800]]
        self.add_flyer(points,4)
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
        self.death_box = pygame.Rect(-1000,self.size[1],10000,50)
        self.ceiling_box = pygame.Rect(-200,-100,10000,200)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.ceiling_box,self.starter_block]
        self.obstacles = []
        self.enemies = []
        self.add_small_block()
        self.add_thin_block()
        self.add_tall_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_elite(self.blocks[-1].x+50, self.blocks[-1].y-125)
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_thin_block()
        self.add_chasm()
        self.add_thin_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()

    def level3(self):
        return

    def level4(self):
        return

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
        for i in range(len(self.obstacles)):
            self.obstacles[i].hit_box = self.obstacles[i].hit_box.move(amount,0)
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
        for i in range(len(self.obstacles)):
            self.obstacles[i].hit_box = self.obstacles[i].hit_box.move(0,amount)
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

    def add_last_box(self,width=250,height=510):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        y = 510
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_spikes(self,x,y,width=85,height=30):
        spikes = Obstacle(width,height,(x,y),'spikes')
        self.obstacles.append(spikes)

    def add_spring(self,x,y,width=85,height=30):
        spring = Obstacle(x,y,width,height,'spring')
        self.obstacles.append(spring)

    def add_basic_enemy(self,x,y,width=85,height=125):
        enemy = Enemy(x,y,width,height,'basic',3)
        self.enemies.append(enemy)

    def add_jump_enemy(self,x,y,width=85,height=125):
        enemy = Enemy(x,y,width,height,'jump',0,18)
        self.enemies.append(enemy)

    def add_elite(self,x,y,width=85,height=125):
        enemy = Elite(x,y,width,height)
        self.enemies.append(enemy)

    def add_flyer(self,points,speed,width=85,height=85):
        enemy_fly = Flyer(points,width,height,speed)
        self.enemies.append(enemy_fly)

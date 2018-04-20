import pygame
from pygame.locals import *
from enemies import *

class Map(pygame.sprite.Sprite):

    def __init__(self,size):
        self.size = size
        self.death_box = pygame.Rect(-1000,self.size[1],10000,50)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.starter_block]
        self.obstacles = []
        self.enemies = []
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_smaller_block()
        self.add_small_block()
        self.add_tall_block()
        self.add_tall_block()
        self.add_small_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_Flayer_enemy(1000,800,1)
        self.add_basic_enemy(self.blocks[-1].x+100,self.blocks[-1].y-125,4)
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



    def side_scroll(self,amount):
        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i].move(amount,0)
        for i in range(len(self.obstacles)):
            self.obstacles[i].hit_box = self.obstacles[i].hit_box.move(amount,0)
        for i in range(len(self.enemies)):
            self.enemies[i].hit_box = self.enemies[i].hit_box.move(amount,0)

    def vert_scroll(self,amount):
        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i].move(0,amount)
        for i in range(len(self.obstacles)):
            self.obstacles[i].hit_box = self.obstacles[i].hit_box.move(0,amount)
        for i in range(len(self.enemies)):
            self.enemies[i].hit_box = self.enemies[i].hit_box.move(0,amount)

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

    def add_chasm(self,width=255,height=50):
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

    def add_basic_enemy(self,x,y,v=4,width=85,height=125):
        enemy_basic = Enemy(x,y,width,height,'basic',v,0)
        self.enemies.append(enemy_basic)

    def add_jump_enemy(self,x,y,v=-18,width=85,height=125):
        enemy_jump = Enemy(x,y,width,height,'jump',0,v)
        self.enemies.append(enemy_jump)

    def add_Flayer_enemy(self,x,y,speed,width=85,height=85):
        enemy_fly = Flyer(x,y,width,height,speed)
        self.enemies.append(enemy_fly)

import pygame
from pygame.locals import *
import time
import os

class Map(pygame.sprite.Sprite):

    def __init__(self,size):
        self.size = size
        self.death_box = pygame.Rect(-1000,self.size[1],10000,50)
        self.starter_block = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.starter_block]
        self.obstacles = []
        self.add_small_block()
        self.add_block()
        self.add_chasm()
        self.add_block()
        self.add_block()
        self.add_small_block()
        self.add_small_block()
        self.add_block()
        self.add_thin_block()
        self.add_tall_block()
        self.add_tall_block()
        self.add_block()
        self.add_block()
        self.add_chasm()
        self.add_chasm()
        self.add_block()
        self.add_thin_block()
        self.add_block()
        self.add_small_block()
        self.add_smaller_block()
        self.add_box()
        self.add_box()
        self.add_box()
        self.add_box()
        self.add_down_box()
        self.add_down_box()


    def side_scroll(self,amount):
        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i].move(amount,0)
        for i in range(len(self.obstacles)):
            self.obstacles[i].hit_box = self.obstacles[i].hit_box.move(amount,0)


    def add_block(self,width=250,height=500):
        last_block = self.blocks[len(self.blocks)-1]
        x = last_block.x + last_block.w
        y = last_block.y + last_block.h - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_tall_block(self,width=250,height=700):
        self.add_block(width,height)

    def add_thin_block(self, width=125, height=500):
        self.add_block(width,height)

    def add_small_block(self,width=250,height=250):
        self.add_block(width,height)

    def add_smaller_block(self,width=250,height=125):
        self.add_block(width,height)

    def add_chasm(self,width=255,height=50):
        last_block = self.blocks[len(self.blocks)-1]
        x = last_block.x + last_block.w
        block = pygame.Rect(x,self.size[1]+50,width,height)
        self.blocks.append(block)

    def add_box(self,width=200,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        y = last_block.y - 100 - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_down_box(self,width=200,height=60):
        last_block = self.blocks[-1]
        x = last_block.x + last_block.w
        y = last_block.y + 150 - height
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
        spring = Obstacle((x,y),width,height,'spring')
        self.obstacles.append(spring)

    def add_roller(self,x,y,width=85,height=85):
        roller = Obstacle((x,y),width,height,'roller')
        self.obstacles.append(roller)

class Player(object):

    def __init__(self,pos,width,height,is_main=True):
        self.height = height
        self.width = width
        self.pos = pos
        #define players pos and demision so rep as Rectangle and colltion and draw are easy
        self.hit_box = pygame.Rect(self.pos[0],
                    self.pos[1],
                    self.width,
                    self.height)
        self.gravity = .165
        self.vy = 8
        self.vx = 4
        self.jump1 = False
        self.jump2 = False
        self.is_main = is_main

    def top_collision(self,i,p1,p2,p3,p4):
        if ((i.collidepoint(p1) and i.collidepoint(p2)) or # Collision on the top
            (i.collidepoint(p3) and i.collidepoint(p4)) and self.vy < 0):
            self.hit_box.y = i.y + i.h
            self.vy = -1

    def bottom_collision(self,i,p9,p10,p11,p12):
        if ((i.collidepoint(p9) and i.collidepoint(p10)) or # Collision on the bottom
            (i.collidepoint(p11) and i.collidepoint(p12)) and self.vy > 0):
            self.hit_box.y = i.y - self.height
            self.vy = 0
            self.jump1 = False
            self.jump2 = False

    def right_collision(self,i,p4,p6,p8,p12,p15,p16):
        if ((i.collidepoint(p4) and i.collidepoint(p6)) or # Collision on the right
            (i.collidepoint(p8) and i.collidepoint(p12)) or
            i.collidepoint(p15) or i.collidepoint(p16)):
            self.hit_box.x = i.x - self.width
            if not self.is_main:
                self.vx *= -1

    def left_collision(self,i,p1,p5,p7,p9,p13,p14):
        if ((i.collidepoint(p1) and i.collidepoint(p5)) or # Collision on the left
            (i.collidepoint(p7) and i.collidepoint(p9)) or
            i.collidepoint(p13) or i.collidepoint(p14)):
            self.hit_box.x = i.x + i.w
            if not self.is_main:
                self.vx *= -1

    def collision(self,mmap,game_over):
        """
        For collision detection, we make a set of three points for each corner
        of our player hitbox:

        1-2-------3-4
        -           -
        5           6
        -           -
        13          14
        -           -
        7           8
        -           -
        9-10-----11-12

        If certain combonations of these points intersect blocks on thee map,
        it means that the player is hitting blocks at certain regions.
        """
        if game_over and not self.is_main:
            self.gravity = 0
            self.vy = 0
            self.vx = 0
        self.hit_box.y += self.vy # pos[1] to y becasue syntax
        self.vy += self.gravity
        if not self.is_main:
            self.hit_box = self.hit_box.move(self.vx,0)
        if self.vy > 10:
            self.vy = 10
        if game_over:
            self.jump1 = True
            self.jump2 = True
            self.vx = 0
            return True
        # Make all key points
        p1 = self.hit_box.topleft
        p4 = self.hit_box.topright
        p9 = self.hit_box.bottomleft
        p12 = self.hit_box.bottomright
        p2 = (p1[0]+11,p1[1])
        p3 = (p4[0]-11,p4[1])
        p5 = (p1[0],p1[1]+11)
        p6 = (p4[0],p4[1]+11)
        p7 = (p9[0],p9[1]-11)
        p8 = (p12[0],p12[1]-11)
        p10 = (p9[0]+11,p9[1])
        p11 = (p12[0]-11,p12[1])
        p13 = (p5[0],p5[1]+50)
        p14 = (p7[0],p7[1]-50)
        p15 = (p6[0],p6[1]+50)
        p16 = (p8[0],p8[1]-50)
        for a in range(len(mmap.blocks)):
            i = mmap.blocks[a]
            if self.hit_box.colliderect(i) and not game_over: # collision
                if a == 0 and self.is_main:
                    return True
                self.top_collision(i,p1,p2,p3,p4)
                self.bottom_collision(i,p9,p10,p11,p12)
                self.right_collision(i,p4,p6,p8,p12,p15,p16)
                self.left_collision(i,p1,p5,p7,p9,p13,p14)
        return False

class Obstacle(Player):

    def __init__(self,pos,width,height,ty):
        super(Obstacle,self).__init__(pos,width,height,False)
        self.type = ty
        if self.type != 'roller':
            self.vx = 0
        else:
            self.vx = 3

class Model(object):

    def __init__(self,size,player,mmap):
        self.size = size
        self.player = player
        self.map = mmap
        self.game_over = False

    def collision(self):
        self.game_over = self.player.collision(self.map,self.game_over)
        for i in self.map.obstacles:
            i.collision(self.map,self.game_over)
            if self.player.hit_box.colliderect(i.hit_box) and not self.game_over:
                self.player.jump1 = False
                self.player.jump2 = False
                if i.type == 'spikes' or i.type == 'roller':
                    self.game_over = True
                    break
                if i.type == 'spring':
                    self.player.jump1 = True
                    self.player.vy = -12


class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for i in self.model.map.blocks:
            pygame.draw.rect(self.screen,(0,255,0), i)
        for i in self.model.map.obstacles:
            if i.type == 'spikes':
                pygame.draw.rect(self.screen,(160,160,160),i.hit_box)
            if i.type == 'spring':
                pygame.draw.rect(self.screen,(255,0,0),i.hit_box)
            if i.type == 'roller':
                pygame.draw.rect(self.screen,(255,0,255),i.hit_box)
        pygame.draw.rect(self.screen,(0,0,255),self.model.player.hit_box)
        if self.model.game_over:
            game_over_font = pygame.font.Font("freesansbold.ttf",50)
            game_over = game_over_font.render("GAME OVER",True,(255,0,0))
            restart = game_over_font.render('PRESS "SPACE" TO RESTART',True,(255,0,0))
            self.screen.blit(game_over, (size[0]//2-game_over.get_width()//2,
                                         size[1]//2-game_over.get_height()))
            self.screen.blit(restart, (size[0]//2-restart.get_width()//2, size[1]//2))
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
            if self.model.player.hit_box.x < self.model.size[0]/4:
                self.model.map.side_scroll(self.model.player.vx)
            else:
                self.model.player.hit_box.x -= self.model.player.vx#change pos[0] to x because syntax
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.model.player.hit_box.x > 3*self.model.size[0]/4:
                self.model.map.side_scroll(-1*self.model.player.vx)
            else:
                self.model.player.hit_box.x += self.model.player.vx # same as above
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
    player = Player((0,680),85,170)
    model = Model(size,player,mmap)
    view = PyGameWindowView(size,model)
    controller = PyGameKeyboardController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if model.game_over and event.type == KEYDOWN and event.key == pygame.K_SPACE:
                mmap = Map(size)
                player = Player((0,680),85,170)
                model = Model(size,player,mmap)
                view = PyGameWindowView(size,model)
                controller = PyGameKeyboardController(model)
        if player.hit_box.y < size[1] or not model.game_over:
            controller.handle_movement()
            model.collision()
        view.draw()
        time.sleep(.001)

    pygame.quit()

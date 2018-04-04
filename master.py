import pygame
from pygame.locals import *
import time
import os

class Map(pygame.sprite.Sprite):

    def __init__(self,size):
        self.size = size
        self.death_box = pygame.Rect(-1000,self.size[1],10000,50)
        self.block1 = pygame.Rect(0,935,320,85)
        self.blocks = [self.death_box,self.block1]
        self.add_block(255,255)
        self.add_block(255,595)
        self.add_chasm()
        self.add_block(600,595)
        self.add_block(700,400)
        self.add_block(600,595)
        self.add_block(255,970)

    def side_scroll(self,amount):
        for i in range(len(self.blocks)):
            self.blocks[i] = self.blocks[i].move(amount,0)

    def add_block(self,width=350,height=500):
        last_block = self.blocks[len(self.blocks)-1]
        x = last_block.x + last_block.w
        y = last_block.y + last_block.h - height
        if last_block.y > self.size[1]:
            y = self.size[1]-height
        block = pygame.Rect(x,y,width,height)
        self.blocks.append(block)

    def add_chasm(self,width=255,height=50):
        last_block = self.blocks[len(self.blocks)-1]
        x = last_block.x + last_block.w
        block = pygame.Rect(x,self.size[1]+50,width,height)
        self.blocks.append(block)

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
        self.gravity = .165
        self.vy = 8
        self.vx = 5
        self.jump1 = False
        self.jump2 = False

class Model(object):

    def __init__(self,size,player,mmap):
        self.size = size
        self.player = player
        self.map = mmap
        self.game_over = False

    def collision(self):
        """
        For collision detection, we make a set of three points for each corner
        of our player hitbox:

        1-2-------3-4
        -           -
        5           6
        -           -
        -           -
        -           -
        7           8
        -           -
        9-10-----11-12

        If certain combonations of these points intersect blocks on thee map,
        it means that the player is hitting blocks at certain regions.
        """
        self.player.hit_box.y += self.player.vy # pos[1] to y becasue syntax
        self.player.vy += self.player.gravity
        if self.player.vy > 10:
            self.player.vy = 10
        # Make all key points
        p1 = self.player.hit_box.topleft
        p4 = self.player.hit_box.topright
        p9 = self.player.hit_box.bottomleft
        p12 = self.player.hit_box.bottomright
        p2 = (p1[0]+11,p1[1])
        p3 = (p4[0]-11,p4[1])
        p5 = (p1[0],p1[1]+11)
        p6 = (p4[0],p4[1]+11)
        p7 = (p9[0],p9[1]-11)
        p8 = (p12[0],p12[1]-11)
        p10 = (p9[0]+11,p9[1])
        p11 = (p12[0]-11,p12[1])
        for a in range(len(self.map.blocks)):
            i = self.map.blocks[a]
            if self.player.hit_box.colliderect(i): # collision
                if a == 0:
                    self.game_over = True
                    self.player.hit_box.y = i.y
                    break
                if ((i.collidepoint(p9) and i.collidepoint(p10)) or # Collision on the bottom
                    (i.collidepoint(p11) and i.collidepoint(p12))):
                    if self.player.vy > 0:
                        self.player.hit_box.y = i.y - self.player.height
                        self.player.vy = 0
                        self.player.jump1 = False
                        self.player.jump2 = False
                if ((i.collidepoint(p1) and i.collidepoint(p2)) or # Collision on the top
                    (i.collidepoint(p3) and i.collidepoint(p4))):
                    self.player.hit_box.y = i.y + i.h
                if ((i.collidepoint(p4) and i.collidepoint(p6)) or # Collision on the right
                      (i.collidepoint(p8) and i.collidepoint(p12))):
                    self.player.hit_box.x = i.x - self.player.width
                if ((i.collidepoint(p1) and i.collidepoint(p5)) or # Collision on the left
                      (i.collidepoint(p7) and i.collidepoint(p9))):
                    self.player.hit_box.x = i.x + i.w


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
        if self.model.game_over:
            game_over_font = pygame.font.Font("freesansbold.ttf",50)
            game_over = game_over_font.render("GAME OVER",True,(255,0,0))
            restart = game_over_font.render('PRESS "SPACE" TO RESTART',True,(255,0,0))
            self.screen.blit(game_over, (size[0]//2-game_over.get_width()//2, size[1]//2-game_over.get_height()))
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
            if self.model.player.hit_box.x < self.model.size[0]/5:
                self.model.map.side_scroll(self.model.player.vx)
            else:
                self.model.player.hit_box.x -= self.model.player.vx #change pos[0] to x because syntax
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.model.player.hit_box.x > 4*self.model.size[0]/5:
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
    player = Player(170,85,[0,680])
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
                player = Player(170,85,[0,680])
                model = Model(size,player,mmap)
                view = PyGameWindowView(size,model)
                controller = PyGameKeyboardController(model)
        if not model.game_over:
            controller.handle_movement()
            model.collision()
        view.draw()
        time.sleep(.001)

    pygame.quit()

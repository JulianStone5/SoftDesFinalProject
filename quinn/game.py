import pygame
from pygame.locals import *
import time
import os
from map_layout import *

class Model(object):

    def __init__(self,size,player,mmap):
        self.size = size
        self.player = player
        self.map = mmap
        self.game_over = False

    def collision(self):
        vscroll = False
        scroll_prop = 1/8
        if self.player.hit_box.y < self.size[1]*scroll_prop and self.player.vy < 0 and not self.game_over:
            vscroll = True
            self.map.vert_scroll(-1*self.player.vy)
        elif self.player.hit_box.y+self.player.hit_box.h > self.size[1]*(1-scroll_prop) and self.player.vy > 0:
            if not self.game_over:
                if self.map.blocks[0].y > self.size[1]:
                    vscroll = True
                    self.map.vert_scroll(-1*self.player.vy)
                else:
                    self.map.vert_scroll(self.size[1]-self.map.blocks[0].y)
        self.game_over = self.player.collision(self.map,self.game_over,vscroll)
        for i in self.map.obstacles:
            if self.player.hit_box.colliderect(i.hit_box) and not self.game_over:
                self.player.jump1 = False
                self.player.jump2 = False
                if i.type == 'spikes':
                    self.game_over = True
                    break
                if i.type == 'spring':
                    self.player.jump1 = True # removes first jump
                    self.player.vy = -12
        for i in self.map.enemies:
            i.collision(self.map,self.game_over)
            if self.player.hit_box.colliderect(i.hit_box) and not self.game_over:
                self.game_over = True
                break


class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for i in self.model.map.blocks:
            if i == self.model.map.blocks[0]:
                pygame.draw.rect(self.screen,(0,0,0), i)
            else:
                pygame.draw.rect(self.screen,(0,255,0), i)
        for i in self.model.map.obstacles:
            if i.type == 'spikes':
                pygame.draw.rect(self.screen,(160,160,160),i.hit_box)
            if i.type == 'spring':
                pygame.draw.rect(self.screen,(255,0,0),i.hit_box)
        for i in self.model.map.enemies:
            pygame.draw.rect(self.screen,(255,255,255), i.hit_box)
        pygame.draw.rect(self.screen,(0,0,255),self.model.player.hit_box)
        if self.model.game_over:
            game_over_font = pygame.font.Font("freesansbold.ttf",50)
            game_over = game_over_font.render("GAME OVER",True,(255,0,0))
            restart = game_over_font.render('PRESS "ENTER" TO RESTART',True,(255,0,0))
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
    player = Player(0,680,85,170)
    model = Model(size,player,mmap)
    view = PyGameWindowView(size,model)
    controller = PyGameKeyboardController(model)
    pygame.mixer.init()
    pygame.mixer.music.load('track3.mp3')
    pygame.mixer.music.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if model.game_over and event.type == KEYDOWN and event.key == pygame.K_RETURN:
                mmap = Map(size)
                player = Player(0,680,85,170)
                model = Model(size,player,mmap)
                view = PyGameWindowView(size,model)
                controller = PyGameKeyboardController(model)
        if player.hit_box.y < size[1] or not model.game_over:
            controller.handle_movement()
            model.collision()
        view.draw()
        time.sleep(.001)

    pygame.quit()

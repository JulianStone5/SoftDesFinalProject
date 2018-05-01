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
        self.game_start = False
        self.start_screen = True
        self.t = time.time()

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
        self.game_over, self.map.levelChanged = self.player.collision(self.map,self.game_over,self.player,vscroll)
        for i in self.map.enemies:
            if type(i) != Flyer:
                i.collision(self.map,self.game_over,self.player)
            if type(i) == Flyer:
                i.Fly_movement()#self.map.enemies[i])

                if time.time()-self.t > 1.5:
                    fire = shoot(player,i)
                    self.map.bullet.append(fire)
                    self.t = time.time()
            if self.player.att_box.colliderect(i.hit_box) and not self.game_over:
                if self.player.attacking:
                    i.lives -= 1
                    if i.lives == 0:
                        self.map.enemies.remove(i)
                    self.player.attacking = False
            if self.player.hit_box.colliderect(i.hit_box) and not self.game_over:
                self.game_over = True
                break
        for i in self.map.bullet:

            i.update_bullet()
            if i.hit_box.colliderect(self.player.hit_box):
                self.game_over = True
                break 

class PyGameWindowView(object):

    def __init__(self,size,model):
        self.screen = pygame.display.set_mode(size)
        self.model = model
        self.size = size

    def draw(self,S,P,PA,E):
        window = pygame.Rect(0,0,self.size[0],self.size[1])
        self.screen.fill((0,0,0))
        for i in self.model.map.blocks:
            if i.colliderect(window) and i != self.model.map.blocks[0]:
                self.screen.blit(S,(i.x,i.y),(0,0,i.w,i.h))

        for i in self.model.map.enemies:
            if i.hit_box.colliderect(window):
                color = (255,0,255)
                if i.lives == 2:
                    color = (255,255,0)
                elif i.lives == 3:
                    color = (0,255,255)
                if not i.mov_right:
                    E = pygame.transform.flip(E,True,False)
                self.screen.blit(E,(i.hit_box.x,i.hit_box.y),(0,0,i.hit_box.w,i.hit_box.h))
        for i in self.model.map.bullet:
            pygame.draw.rect(self.screen, (255,255,255), i.hit_box )
        tut_font = pygame.font.Font("freesansbold.ttf",25)
        if self.model.map.level == 1:
            for i in self.model.map.tutorial:
                t = tut_font.render(i[2],True,(255,255,255))
                self.screen.blit(t,(i[0],i[1]))

        x = self.model.player.hit_box.x
        y = self.model.player.hit_box.y
        w = self.model.player.hit_box.w
        h = self.model.player.hit_box.h
        if not self.model.player.mov_right:
            P = pygame.transform.flip(P,True,False)
            PA = pygame.transform.flip(PA,True,False)


        if self.model.player.att_animation:
            #pygame.draw.rect(self.screen, (0,0,255), self.model.player.att_box)
            if not self.model.player.mov_right:
                x -= 50
            self.screen.blit(PA,(x,y),(0,0,w+60,h))
        else:
            self.screen.blit(P,(x,y),(0,0,w,h))

        if self.model.game_over:
            game_over_font = pygame.font.Font("freesansbold.ttf",50)
            game_over = game_over_font.render("GAME OVER",True,(255,0,0))
            restart = game_over_font.render('PRESS "ENTER" TO RESTART',True,(255,0,0))
            self.screen.blit(game_over, (self.size[0]//2-game_over.get_width()//2,
                                         self.size[1]//2-game_over.get_height()))
            self.screen.blit(restart, (self.size[0]//2-restart.get_width()//2, size[1]//2))

        pygame.display.update()

    def story(self,text,N):
        self.screen.fill((0,0,0))
        story = pygame.font.Font("freesansbold.ttf",50)
        start = False
        for i in range(len(text)):
            start = self.fade_in(story, text[i],10+i*400,10+i*300) or start
        begin = pygame.font.Font("freesansbold.ttf",30)
        if self.model.map.level == 0:
            self.screen.fill((0,0,0))
            self.screen.blit(N,((self.size[0]-N.get_width())//2,(self.size[1]-N.get_height())//2-200))
            pygame.display.update()
            start = self.fade_in(begin, 'Press ENTER to start',centered=True) or start
        else:
            start = self.fade_in(begin, 'Press ENTER to continue',1400,975) or start
        while not start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN and event.key == pygame.K_RETURN:
                    start = True

    def fade_in(self,f,text,x=10,y=10,color=(255,255,255),centered=False):
        p = f.render(text,True,color)
        if centered:
            x = self.size[0]//2-p.get_width()//2
            y = self.size[1]//2-p.get_height()//2
        surf = pygame.Surface(f.size(text))
        surf.blit(p,(0,0))
        for i in range(50):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN and event.key == pygame.K_RETURN:
                    self.model.map.levelChanged = True
            if self.model.map.levelChanged:
                return True
            surf.set_alpha(i)
            self.screen.blit(surf, (x,y))
            pygame.display.flip()
            time.sleep(.05)
            pygame.display.update()
        return False

class PyGameKeyboardController(object):

    def __init__(self,model):
        self.model = model
        self.up_uncl = True # Ensures double jump only after key is released between jumps
        self.att_uncl = True
        self.t = time.time()

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_w] and not keys[pygame.K_UP]:
            self.up_uncl = True # Verifies that the jump key has been unclicked
        if not keys[pygame.K_SPACE]:
            self.att_uncl = True # Verifies that the jump key has been unclicked
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.model.player.hit_box.x < self.model.size[0]/3:
                self.model.map.side_scroll(self.model.player.vx)
            else:
                self.model.player.hit_box.x -= self.model.player.vx #change pos[0] to x because syntax
            self.model.player.mov_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.model.player.hit_box.x+self.model.player.hit_box.w > 2*self.model.size[0]/3:
                self.model.map.side_scroll(-1*self.model.player.vx)
            else:
                self.model.player.hit_box.x += self.model.player.vx # same as above
            self.model.player.mov_right = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if not self.model.player.jump1 and self.up_uncl:
                self.model.player.vy = -9 # Set up-velocity to initialize jump
                self.model.player.jump1 = True # Mark first jump
                self.up_uncl = False # Say that the jump key has been clicked
            elif not self.model.player.jump2 and self.up_uncl:
                self.model.player.vy = -9
                self.model.player.jump2 = True # Mark second jump
                self.up_uncl = False
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.model.player.vy = 9 # Move player down
        if keys[pygame.K_SPACE]:
            if not self.model.player.attacking and self.att_uncl:
                self.t = time.time()
                self.model.player.attacking = True
                self.model.player.att_animation = True
                self.att_uncl = False
        if time.time()-self.t > .15:
            self.model.player.attacking = False
            self.model.player.att_animation = False


if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    mmap = Map(size)
    player = Player(0,680,85,125)
    model = Model(size,player,mmap)
    view = PyGameWindowView(size,model)
    controller = PyGameKeyboardController(model)
    pygame.display.set_mode(size)
    # pygame.mixer.init()
    # pygame.mixer.music.load('track1.mp3')
    # pygame.mixer.music.play()

    running = True
    name = pygame.image.load("dark_castle.png").convert()
    N = pygame.Surface(name.get_size(), pygame.HWSURFACE)
    N.blit(name,(0,0))
    N = pygame.transform.scale(N,(N.get_width()*2,N.get_height()*2))
    stone = pygame.image.load("stone.png").convert()
    S = pygame.Surface(stone.get_size(), pygame.HWSURFACE)
    S.blit(stone,(0,0))
    p = pygame.image.load("player.png").convert()
    P = pygame.Surface(p.get_size(), pygame.HWSURFACE)
    #P.set_alpha(128)
    P.blit(p,(0,0))
    P = pygame.transform.scale(P,(player.hit_box.w,player.hit_box.h))
    pa = pygame.image.load("playerAttack.png").convert()
    PA = pygame.Surface(pa.get_size(), pygame.HWSURFACE)
    #PA.set_alpha(128)
    PA.blit(pa,(0,0))
    PA = pygame.transform.scale(PA,(player.hit_box.w+50,player.hit_box.h))
    e = pygame.image.load("enemy.png").convert()
    E = pygame.Surface(e.get_size(), pygame.HWSURFACE)
    E.blit(e,(0,0))
    E = pygame.transform.scale(E,(85,125))

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if (model.game_over or mmap.level == 0) and event.type == KEYDOWN and event.key == pygame.K_RETURN:
                player = Player(0,680,85,125)
                mmap = Map(size,mmap.level)
                mmap.levelChanged = True
                model = Model(size,player,mmap)
                view = PyGameWindowView(size,model)
                controller = PyGameKeyboardController(model)
        if not mmap.levelChanged:
            view.story(mmap.story_text[mmap.level],N)
            mmap.level += 1
            mmap.make_level()
            mmap.levelChanged = True
            player.hit_box.x = 0
            player.hit_box.y = 680
        elif player.hit_box.y < size[1] or not model.game_over:
            controller.handle_movement()
            model.collision()
        if mmap.level != 0:
            view.draw(S,P,PA,E)
        time.sleep(.001)

    pygame.quit()

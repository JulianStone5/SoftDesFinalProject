import pygame
from pygame.locals import *

class Player(object):

    def __init__(self,x,y,width,height,is_main=True):
        #define players pos and demision so rep as Rectangle and colltion and draw are easy
        self.hit_box = pygame.Rect(x,y,width,height)
        self.gravity = .165
        self.vy = 8
        self.vx = 4
        self.jump1 = False #setting up for double jumps
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
            self.hit_box.y = i.y - self.hit_box.h
            self.vy = 0
            if not self.is_main:
                if self.type == 'jump':
                    self.vy = -18
            self.jump1 = False
            self.jump2 = False

    def right_collision(self,i,p4,p6,p8,p12,p15,p16):
        if ((i.collidepoint(p4) and i.collidepoint(p6)) or # Collision on the right
            (i.collidepoint(p8) and i.collidepoint(p12)) or
            i.collidepoint(p15) or i.collidepoint(p16)):
            self.hit_box.x = i.x - self.hit_box.w
            if not self.is_main:
                self.vx *= -1

    def left_collision(self,i,p1,p5,p7,p9,p13,p14):
        if ((i.collidepoint(p1) and i.collidepoint(p5)) or # Collision on the left
            (i.collidepoint(p7) and i.collidepoint(p9)) or
            i.collidepoint(p13) or i.collidepoint(p14)):
            self.hit_box.x = i.x + i.w
            if not self.is_main:
                self.vx *= -1

    def collision(self,mmap,game_over,vscroll=False):
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

        This will update the positions of players, enemies, and obstacles based
        on collision detection and it will return whether the game is over after
        the sets of collisions are found.
        """
        if game_over and not self.is_main: #Stop enemies when game ends
            self.gravity = 0
            self.vy = 0
            self.vx = 0
        if not vscroll:
            self.hit_box.y += self.vy # pos[1] to y becasue syntax
        self.vy += self.gravity
        if not self.is_main:
            self.hit_box = self.hit_box.move(self.vx,0) #So enemies can move without keypress
        if self.vy > 10: #Terminal velocity
            self.vy = 10
        if game_over: #Stops collision detection for player when game is over
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
                if a == 0 and self.is_main: # If player falls off screen
                    return True
                self.top_collision(i,p1,p2,p3,p4)
                self.bottom_collision(i,p9,p10,p11,p12)
                self.right_collision(i,p4,p6,p8,p12,p15,p16)
                self.left_collision(i,p1,p5,p7,p9,p13,p14)
        return False

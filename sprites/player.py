from pygame import *
import pygame
from sprites.entity import Entity


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill(Color("#0000FF"))
        self.rect = Rect(x, y, 32, 32)
        self.alive = True

    def update(self, up, down, left, right, running, objects):
        '''
        Controls the movement of the player on the map
        '''
        if up:
            # only jump if on the ground
            if self.onGround:
                self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 1
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.4
            # max falling speed
            if self.yvel > 10:
                self.yvel = 10
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, objects)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, objects)

    def collide(self, xvel, yvel, objects):
        '''
        Handles collions between the player and
        game objects like walls and platforms
        '''
        for b in objects.barriers:
            if pygame.sprite.collide_rect(self, b):
                if xvel > 0:
                    self.rect.right = b.rect.left
                if xvel < 0:
                    self.rect.left = b.rect.right
                if yvel > 0:
                    self.rect.bottom = b.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = b.rect.bottom
                    self.yvel += 0.5

    def collide_s():
        '''
        Handles collions between the player and
        enemies, coins and other game state
        changing things
        '''
        pass

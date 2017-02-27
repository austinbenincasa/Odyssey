from pygame import *
import pygame
from sprites.entity import Entity


class Spaceship(Entity):
    def __init__(self, x, y, win_width, win_height):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill(Color("#0000FF"))
        self.rect = Rect(x, y, 32, 32)
        self.alive = True
        self.fire_delay = 0
        self.WIN_WIDTH = win_width
        self.WIN_HEIGHT = win_height

    def update(self, up, down, left, right, objects):
        '''
        Controls the movement of the ship on the map
        '''
        if up:
            self.yvel = -7
        if down:
            self.yvel = 7
        if left:
            self.xvel = -7
        if right:
            self.xvel = 7
        if not(left or right):
            self.xvel = 0
        if not(up or down):
            self.yvel = 0

        # increment in x direction
        self.rect.left += self.xvel

        # check window bounds
        if self.rect.right >= self.WIN_WIDTH:
                self.rect.right = self.WIN_WIDTH
        if self.rect.left <= 0:
                self.rect.left = 0

        # do x-axis collisions
        self.collide(self.xvel, 0, objects)
        # increment in y direction
        self.rect.top += self.yvel

        # check window bounds
        if self.rect.bottom >= self.WIN_HEIGHT:
                self.rect.bottom = self.WIN_HEIGHT
        if self.rect.top <= 0:
                self.rect.top = 0

        # do y-axis collisions
        self.collide(0, self.yvel, objects)
        self.fire_delay += 1

    def collide(self, xvel, yvel, objects):
        '''
        Handles collions between the ship and
        game objects like enemy_spaceships and
        fired_lasers
        '''
        for e in objects.enemy_spaceships:
            if pygame.sprite.collide_rect(self, e):
                self.alive = False
                # trigger explosions
        for l in objects.fired_lasers:
            if pygame.sprite.collide_rect(self, l):
                self.alive = False
                # trigger explosions
        for a in objects.asteroids:
            if pygame.sprite.collide_rect(self, a):
                self.alive = False
                # trigger explosions

    def explosion(self):
        pass

    def fire_laser(self, objects):
        if self.fire_delay > 7:
            beam = Lasers(self.rect.right,self.rect.top,self.WIN_WIDTH)
            objects.fired_lasers.append(beam)
            objects.entities.add(beam)
            self.fire_delay = 0

class Lasers(Entity):
    def __init__(self,x,y, win_width):
        Entity.__init__(self)
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill(Color('#00FF00'))
        self.rect = Rect(x, y, 32, 32)
        self.active = True
        self.win_width = win_width
        self.type = ""

    def move(self):
        if not self.rect.left > self.win_width - 5:
            self.rect.left += 7
        else:
            self.active = False

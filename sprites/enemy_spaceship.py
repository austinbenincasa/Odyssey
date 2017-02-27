from pygame import *
import pygame
from sprites.entity import Entity
from random import randint


class Enemy_Spaceship(Entity):
    def __init__(self,x,y,win_width,win_height,speed):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill(Color("#0000FF"))
        self.rect = Rect(x, y, 32, 32)
        self.fire_count = 20
        self.win_width = win_width
        self.win_height = win_height
        self.alive = True
        self.speed = speed

    def move(self,objects):
        self.collisions(objects)
        if self.rect.left < -5:
            self.alive = False
        else:
            self.rect.left -= self.speed

    def collisions(self,objects):
        for l in objects.fired_lasers:
            if pygame.sprite.collide_rect(self, l):
                if l.type == "":
                    self.alive = False
                    objects.fired_lasers.remove(l)
                    objects.entities.remove(l)
                    objects.enemies_killed += 1

    def fire_lasers(self,objects):
        rand = randint(0,50)
        rand1 = randint(0,50)
        if rand == rand1:
            beam = self.create_laser(self.rect.left,self.rect.top)
            objects.fired_lasers.append(beam)
            objects.entities.add(beam)
            self.fire_count = 0

    def explosion(self):
        pass

    def create_laser(self,x,y):
        return Lasers(x,y)


class Lasers(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill(Color('#FF0000'))
        self.rect = Rect(x, y, 32, 32)
        self.active = True
        self.type = "enemy"

    def move(self):
        if not self.rect.left < -50:
            self.rect.left -= 7
        else:
            self.active = False

from sprites.entity import Entity
from pygame import *
from random import choice, randint

class Star(Entity):
    def __init__(self, x, y, win_width, win_height):
        super(Star,self).__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(self.rand_color())
        self.rect = Rect(x, y, 32, 32)
        self.win_width = win_width
        self.win_height = win_height

    def rand_color(self):
        selection = choice([1,2,3])
        if selection == 1:
            color = (100,100,100)
        elif selection == 2:
            color = (190,190,190)
        else:
            color = (255,255,255)
        return color

    def move(self,speed):
        if self.rect.left < -50:
            self.rand_color()
            self.rect.left = self.win_width
            self.rect.top = randint(0,self.win_height)
        else:
            self.rect.left -= speed

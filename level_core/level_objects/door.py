from sprites.entity import Entity
from pygame import *


class Door(Entity):
    def __init__(self, x, y):
        super(Door,self).__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#8B4513"))
        self.rect = Rect(x, y, 32, 32)

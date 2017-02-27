from sprites.entity import Entity
from pygame import *


class Asteroid(Entity):
    def __init__(self, x, y):
        super(Asteroid,self).__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#FFD700"))
        self.rect = Rect(x, y, 32, 32)

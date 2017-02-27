from sprites.entity import Entity
from pygame import *


class Wall(Entity):
    def __init__(self, x, y):
        super(Wall,self).__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#A9A9A9"))
        self.rect = Rect(x, y, 32, 32)

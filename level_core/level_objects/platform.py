from sprites.entity import Entity
from pygame import *

class Platform(Entity):
    def __init__(self, x, y):
        super(Platform,self).__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

from pygame import *
import pygame
from sprites.entity import Entity


class Alien(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)

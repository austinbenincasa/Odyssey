import pygame


class Event:
  '''
  Holding and handling all game events
  '''
  def __init__(self):
    self.events = pygame.event.get()

  def update(self):
    self.events = pygame.event.get()

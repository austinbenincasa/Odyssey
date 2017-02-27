import pygame
from pygame import *
from sprites.camera import Complex_Camera, Camera
from level_core.level_objects.wall import Wall
from level_core.level_objects.platform import Platform
from level_core.level_objects.door import Door
from level_core.level_objects.coin import Coin
from sprites.player import Player


class Platform_Controller(object):
    """
    This class handles the loading and unloaded of
    platforms in the game. It also handles most of
    the events that are recieved from the Engine
    that pertain to the level
    """
    def __init__(self,config):
        self.BLOCK_HEIGHT = config.BLOCK_HEIGHT
        self.BLOCK_WIDTH = config.BLOCK_WIDTH
        self.WIN_WIDTH = config.WIN_WIDTH
        self.WIN_HEIGHT = config.WIN_HEIGHT
        self.HALF_WIDTH =  config.HALF_WIDTH
        self.HALF_HEIGHT = config.HALF_HEIGHT
        self.objects = Objects()

    def load_platform(self,platform):
        '''
        Used to load new platforms, this is called
        from the GameEngine. Accepts a instance
        of a level class
        '''
        self.running = False
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.loaded_platform = platform
        self.platform_cleared = False
        self.platform_failed = False
        self.generate_objects()

    def unload_platform(self):
        '''
        Used to unload a platforms settings. This
        could be used to signal the end of the
        game or just the end of a level
        '''
        self.objects.reset()
        self.level_cleared = False

    def render_platform(self,screen):
        '''
        Draws all of the objects and player
        on the screen
        '''
        screen.fill((0,0,0))
        for e in self.objects.entities:
            screen.blit(e.image, self.camera.apply(e))

    def generate_objects(self):
        '''
        Creates and stores all the of the objects
        that are found in the loaded platform
        '''

        _map = self.loaded_platform.map
        x = y = 0
        for row in _map:
            for col in row:
                # walls
                if col == "w":
                    sprite = self.create_wall(x,y)
                    self.objects.barriers.append(sprite)
                # doors
                if col == "d":
                    sprite = self.create_door(x,y)
                    self.objects.collidable.append(sprite)
                # platforms
                if col == "p":
                    sprite = self.create_platform(x,y)
                    self.objects.barriers.append(sprite)
                # player position
                if col == "x":
                    ent = self.create_player(x,y)
                    self.player = ent
                    sprite = ent
                # coins
                if col == "c":
                    sprite = self.create_coin(x,y)
                    self.objects.collidable.append(sprite)

                x += self.BLOCK_WIDTH
                self.objects.entities.add(sprite)
            y += self.BLOCK_HEIGHT
            x = 0
        total_level_width  = len(_map[0])*32
        total_level_height = len(_map)*32
        self.camera = Camera(Complex_Camera,total_level_width,total_level_height)

    def event_handler(self,events):
        '''
        Handles all of the events mostly will involve
        moving the player around the platform
        '''

        for e in events:
            if e.type == KEYDOWN and e.key == K_UP:
                self.up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                self.down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                self.left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                self.right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.running = True
            if e.type == KEYUP and e.key == K_UP:
                self.up = False
            if e.type == KEYUP and e.key == K_DOWN:
                self.down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                self.right = False
            if e.type == KEYUP and e.key == K_LEFT:
                self.left = False


        self.player.update(self.up, self.down, self.left, self.right,
                            self.running, self.objects)
        self.special_collison()

    def special_collison(self):
        '''
        Checks if the player has collided with anything
        that is currently on the platform. This can be
        enemys, coins, and other various objects.
        '''
        for c in self.objects.collidable:
            if pygame.sprite.collide_rect(self.player, c):
                if isinstance(c, Coin):
                    self.objects.collidable.remove(c)
                    self.objects.entities.remove(c)
                if isinstance(c, Door):
                    self.platform_cleared = True

    def create_door(self,x,y):
        '''
        Creates a sprite object of type Wall
        '''
        return Door(x,y)
    def create_wall(self,x,y):
        '''
        Creates a sprite object of type Wall
        '''
        return Wall(x,y)
    def create_platform(self,x,y):
        '''
        Creates a sprite object of type Platform
        '''
        return Platform(x,y)
    def create_player(self,x,y):
        '''
        Creates a sprite object of type Player
        '''
        return Player(x,y)
    def create_coin(self,x,y):
        '''
        Creates a sprite object of type Coin
        '''
        return Coin(x,y)

    def create_alien(self):
        '''
        Creates a sprite object of type Alien
        '''
        pass

class Objects:
    """
    Holds all of the objects found on the
    platform
    """
    def __init__(self):
        self.entities = pygame.sprite.Group()
        self.barriers = []
        self.collidable = []
        self.enemies = []

    def reset(self):
        self.entities = pygame.sprite.Group()
        self.barriers = []
        self.collidable = []
        self.enemies = []

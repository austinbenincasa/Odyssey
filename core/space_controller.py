import pygame
from pygame import *
from level_core.level_objects.asteroid import Asteroid
from level_core.level_objects.star import Star
from sprites.spaceship import Spaceship
from sprites.enemy_spaceship import  Enemy_Spaceship
from sprites.camera import Complex_Camera, Camera
from random import randint


class Space_Controller(object):
    '''
    This class controls the space levels in the game.
    It handles the loading and unloaded of randomized
    solar systems in the game. It also handles most of
    the events that are recieved from the Engine that
    pertain the level
    '''
    def __init__(self,config):
        self.BLOCK_HEIGHT = config.BLOCK_HEIGHT
        self.BLOCK_WIDTH = config.BLOCK_WIDTH
        self.WIN_WIDTH = config.WIN_WIDTH
        self.WIN_HEIGHT = config.WIN_HEIGHT
        self.HALF_WIDTH =  config.HALF_WIDTH
        self.HALF_HEIGHT = config.HALF_HEIGHT
        self.max_stars = 45
        self.space_cleared = False
        self.space_failed = False
        self.objects = Objects()

    def move_space(self):
        '''
        Controls the auto scrolling of space this moves
        the location of stars, asteroids and enemy
        spaceships on the screen and their given speed.
        Also checks to see if they are still alive
        '''
        for s in self.objects.stars:
            s.move(self.space_speed)
        for l in self.objects.fired_lasers:
            if not l.active:
                self.objects.fired_lasers.remove(l)
                self.objects.entities.remove(l)
            else:
                l.move()
        for e in self.objects.enemy_spaceships:
            e.move(self.objects)
            e.fire_lasers(self.objects)
            if not e.alive:
                self.objects.enemy_spaceships.remove(e)
                self.objects.entities.remove(e)

        for a in self.objects.asteroids:
            a.move()
            if not a.live:
                self.objects.asteroids.remove(a)
                self.objects.entities.remove(a)


    def event_handler(self,events):
        '''
        Handles the movement,firing and
        aliveness of the spaceship
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
                self.firing = True
            if e.type == KEYUP and e.key == K_UP:
                self.up = False
            if e.type == KEYUP and e.key == K_DOWN:
                self.down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                self.right = False
            if e.type == KEYUP and e.key == K_LEFT:
                self.left = False
            if e.type == KEYUP and e.key == K_SPACE:
                self.firing = False

        if self.firing:
            self.spaceship.fire_laser(self.objects)

        self.spaceship.update(self.up, self.down, self.left, self.right, self.objects)

        if self.spaceship.alive == False:
            self.space_failed = True


    def load_space(self,level):
        '''
        Loads all of the configurations
        that space should abide by as well
        as
        '''
        self.firing = False
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space_speed = level.space_speed
        self.enemy_interval = level.enemy_interval
        self.enemy_interval_c = level.enemy_interval
        self.enemy_hardness = level.enemy_hardness
        self.level_duration = level.level_duration
        self.enemy_speed = level.enemy_speed
        #creating stars
        for i in range(self.max_stars):
            x = randint(0,self.WIN_WIDTH)
            y = randint(0,self.WIN_HEIGHT)
            star = self.create_star(x,y)
            self.objects.stars.append(star)
            self.objects.entities.add(star)


        # create spaceship
        ship = self.create_spaceship(self.WIN_WIDTH/2,self.WIN_HEIGHT/2)
        self.spaceship = ship
        self.objects.entities.add(ship)


        self.camera = Camera(Complex_Camera,self.WIN_WIDTH,self.WIN_HEIGHT)


    def unload_space(self):
        '''
        Resets the space controller to default
        settings. This helps clean up memory
        when the controller is not in use
        '''
        self.objects.reset()
        #self.camera = None
        #self.spaceship = None
        self.space_cleared = False
        self.space_failed = False


    def render_space(self,screen):
        '''
        Draws all the current entities on
        the screen
        '''
        screen.fill((0,0,0))
        for e in self.objects.entities:
            screen.blit(e.image, self.camera.apply(e))

        self.move_space()

        # decrement counters
        self.level_duration -= 1
        self.enemy_interval_c -= 1

        if self.enemy_interval_c == 0:
            ship = self.random_enemy_gen()
            self.objects.enemy_spaceships.append(ship)
            self.objects.entities.add(ship)
            self.enemy_interval_c = self.enemy_interval

        if self.level_duration == 0:
            self.space_cleared = True


    def random_enemy_gen(self):
        '''
        Generates random enemies for
        the level
        '''
        x = self.WIN_WIDTH + 5
        y = randint(0,self.WIN_HEIGHT)
        return self.create_enemy_spaceship(x,y)

    def random_asteroid_gen(self):
        '''
        Generates random asteroids for
        the level
        '''
        x = self.WIN_WIDTH + 5
        y = randint(0,self.WIN_HEIGHT)
        return self.create_asteroid(x,y,self.WIN_WIDTH,self.WIN_HEIGHT)

    def create_spaceship(self,x,y):
        return Spaceship(x,y,self.WIN_WIDTH,self.WIN_HEIGHT)


    def create_asteroid(self,x,y):
        return Asteroid(x,y)


    def create_star(self,x,y):
        return Star(x,y,self.WIN_WIDTH,self.WIN_HEIGHT)


    def create_enemy_spaceship(self,x,y):
        return Enemy_Spaceship(x,y,self.WIN_WIDTH,self.WIN_HEIGHT,self.enemy_speed)


class Objects:
    """
    Holds all of the objects found in
    space
    """
    def __init__(self):
        self.entities = pygame.sprite.Group()
        self.fired_lasers = []
        self.stars = []
        self.asteroids = []
        self.enemy_spaceships = []
        self.enemies_killed = 0


    def reset(self):
        self.entities = pygame.sprite.Group()
        self.fired_lasers = []
        self.stars = []
        self.asteroids = []
        self.enemy_spaceships = []
        self.enemies_killed = 0

import pygame
from core.event import Event
from core.platform_controller import Platform_Controller
from core.space_controller import Space_Controller
from level_core.levels.level1 import Level_1
from level_core.levels.level2 import Level_2
from level_core.levels.level3 import Level_3
from level_core.levels.level4 import Level_4


class Engine(object):
    '''
    The core controller of the game. It is what
    handles level changing, event handling, etc.
    This also manages platform_controller and
    space_controller
    '''
    def __init__(self,config):
        pygame.init()
        self.config = config
        self.running = True
        self.fullscreen = False
        self.framerate = config.framerate
        self.screen_height = config.WIN_HEIGHT
        self.screen_width = config.WIN_WIDTH
        self.screen_size = (self.screen_width,self.screen_height)
        self.run_menu = True
        self.run_fail_menu = False
        self.main_menu = MainMenu(config.WIN_WIDTH,config.WIN_HEIGHT)
        self.fail_menu = FailMenu(config.WIN_WIDTH,config.WIN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)
        # list of level instances
        self.levels = [
            Level_1(),
            Level_2(),
            Level_3(),
            Level_4()
        ]
        self.current_level = 0
        self.space_controller = Space_Controller(self.config)
        self.platform_controller = Platform_Controller(self.config)
        self.event = Event()
        pygame.event.set_allowed([
            pygame.QUIT,pygame.KEYDOWN,
            pygame.KEYUP])
        self.level_type = ""

    def run(self):
        '''
        Starts the game and begins handling events
        given the current levels type
        '''
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(self.framerate)

            self.event.update()
            self.event_handler(self.event.events)

            # handlers for specifc game states
            if self.level_type == "":
                if self.run_menu:
                    self.main_menu.render(self.screen)
                    self.main_menu_handler()
                elif self.run_fail_menu:
                    self.fail_menu.render(self.screen)
                    self.fail_menu_handler()
            else:
                if self.level_type == "platform":
                    self.platform_controller.camera.update(
                            self.platform_controller.player)
                    self.platform_controller.render_platform(self.screen)
                elif self.level_type == "space":
                    self.space_controller.camera.update(
                            self.space_controller.spaceship)
                    self.space_controller.render_space(self.screen)

            pygame.display.update()

    def event_handler(self,events):
        '''
        Recieves the game events and directs
        them to the current level for further
        handling
        '''
        # handling basic game events
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
        # calling specifc handlers for game state specific events
        if self.level_type == "":
            # in a menu state check what menu is loaded
            if self.run_menu:
                self.main_menu.event_handler(events)
            elif self.run_fail_menu:
                self.fail_menu.event_handler(events)
        else:
            # running a game level check what type of level
            if self.level_type == "platform":
                # check if level has finished
                if self.platform_controller.platform_cleared:
                    # is this the last level?
                    if (self.current_level + 1) >= len(self.levels):
                        self.exit()
                    else:
                        self.platform_controller.unload_platform()
                        self.change_level()

                elif self.platform_controller.platform_failed:
                    self.platform_controller.unload_platform()
                    self.level_type = ""
                    self.run_fail_menu = True
                    self.fail_menu.running = True

                self.platform_controller.event_handler(events)

            elif self.level_type == "space":
                if self.space_controller.space_cleared:
                    if (self.current_level + 1) >= len(self.levels):
                        # exiting this this for now
                        self.exit()
                    else:
                        self.space_controller.unload_space()
                        self.change_level()
                elif self.space_controller.space_failed:
                    # handle being dead maybe print exit screen
                    self.space_controller.unload_space()
                    self.level_type = ""
                    self.run_fail_menu = True
                    self.fail_menu.running = True

                self.space_controller.event_handler(events)


    def level_controller(self):
        '''
        This function handles how a level is played.
        That means deciding whether to pass the level to
        the platform controller or space controller
        '''
        level = self.levels[self.current_level]
        self.level_type = level.level_type

        if level.level_type == "space":
            self.space_controller.load_space(level)
        if level.level_type == "platform":
            self.platform_controller.load_platform(level)

    def main_menu_handler(self):
        '''
        Handles the selection that the user
        had made at the main menu
        '''
        if not self.main_menu.running:
            #replay level
            if self.main_menu.selection == 0:
                self.run_menu = False
                self.level_controller()
            # exit game
            elif self.main_menu.selection == 1:
                self.exit()

    def fail_menu_handler(self):
        '''
        Handles the selection that the user
        had made at the fail menu
        '''
        if not self.fail_menu.running:
            #replay level
            if self.fail_menu.selection == 0:
                self.run_fail_menu = False
                self.level_controller()
            #exit game
            elif self.fail_menu.selection == 1:
                self.exit()

    def exit(self):
        '''
        Exits out of the game
        '''
        self.running = False

    def change_level(self):
        '''
        Changes the levels of the game
        '''
        self.current_level = self.current_level + 1
        if self.level_type == "platform":
            self.platform_controller.unload_platform()
        else:
            self.space_controller.unload_space()
        self.level_controller()


# definitions for the games different menus
class MainMenu:
    '''
    Handles the events and drawing of the
    game's main menu screen
    '''
    def __init__(self,win_width,win_height):
        self.title_font = pygame.font.SysFont("monospace", 40)
        self.font = pygame.font.SysFont("monospace", 25)
        self.selection = 0
        self.win_width = win_width
        self.win_height = win_height
        self.running = True


    def event_handler(self,events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.selection = 0
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.selection = 1
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.running = False

    def render(self,screen):
        screen.fill((0,0,0))
        if self.selection == 0:
            self.title = self.title_font.render("Odyessy",1, (0,0,255))
            self.start = self.font.render("Start", 1, (0,0,255))
            self.end = self.font.render("Exit", 1, (255,255,255))
            screen.blit(self.title, (340,250))
            screen.blit(self.start, (self.win_width/2-15, self.win_height/2))
            screen.blit(self.end, (self.win_width/2-15, self.win_height/2 + 40))
        else:
            self.title = self.title_font.render("Odyessy",1, (0,0,255))
            self.start = self.font.render("Start", 1, (255,255,255))
            self.end = self.font.render("Exit", 1, (0,0,255))
            screen.blit(self.title, (340, 250))
            screen.blit(self.start, (self.win_width/2-15, self.win_height/2))
            screen.blit(self.end, (self.win_width/2-15, self.win_height/2 + 40))


class FailMenu:
    '''
    Handles the events and drawing of the
    game's Failed screen
    '''
    def __init__(self,win_width,win_height):
        self.font = pygame.font.SysFont("monospace", 25)
        self.title = pygame.font.SysFont("monospace", 30)
        self.selection = 0
        self.win_width = win_width
        self.win_height = win_height
        self.running = True


    def event_handler(self,events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.selection = 0
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.selection = 1
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.running = False

    def render(self,screen):
        screen.fill((0,0,0))
        if self.selection == 0:
            self.msg = self.title.render("You fucked up",1,(255,0,0))
            self.start = self.font.render("Replay", 1, (0,0,255))
            self.end = self.font.render("Exit", 1, (255,255,255))
            screen.blit(self.msg, (self.win_width/2-15, self.win_height/2 - 40))
            screen.blit(self.start, (self.win_width/2-15, self.win_height/2))
            screen.blit(self.end, (self.win_width/2-15, self.win_height/2 + 40))
        else:
            self.msg = self.title.render("You fucked up",1,(255,0,0))
            self.start = self.font.render("Replay", 1, (255,255,255))
            self.end = self.font.render("Exit", 1, (0,0,255))
            screen.blit(self.msg, (self.win_width/2-15, self.win_height/2 - 40))
            screen.blit(self.start, (self.win_width/2-15, self.win_height/2))
            screen.blit(self.end, (self.win_width/2-15, self.win_height/2 + 40))

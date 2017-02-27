from resources.game_config import Config
'''
Runs the engine which begins
running the game
'''

def run():
    from core.engine import Engine
    game_config = Config()
    GameEngine = Engine(game_config)
    GameEngine.run()

if __name__ in "__main__":
    run()

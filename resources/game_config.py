class Config:
    '''
    This class holds all of the
    games configuration options
    '''
    def __init__(self):
        self.BLOCK_HEIGHT = 32
        self.BLOCK_WIDTH = 32
        self.WIN_WIDTH = 800
        self.WIN_HEIGHT = 640
        self.HALF_WIDTH = int(self.WIN_WIDTH / 2)
        self.HALF_HEIGHT = int(self.WIN_HEIGHT / 2)
        self.framerate = 60

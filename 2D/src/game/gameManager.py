'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.configManager import ConfigManager

class GameManager():

    #singleton
    _instance = None
    
    #create and return de instance
    def __new__(cls):
        if cls._instance is None:  #check if already is one in place
            cls._instance = super(GameManager, cls).__new__(cls) #create if necessary
            cls._instance._initialized = False  
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None: 
            cls._instance = GameManager() #create instance  
        return cls._instance


    def __init__(self):
        if not self._initialized:
            pygame.mixer.music.load("../Sound/BSO/Credits.wav") #load by default the menu music
            pygame.mixer.music.play() #start the music
            ConfigManager().get_instance().load_fonts()
            self.screen = pygame.display.set_mode((ConfigManager().get_instance().get_width(), ConfigManager().get_instance().get_height()))  # screen size default 1280 x 720
            pygame.display.set_caption("Skelly & Soulie") #display name of the game on the edge of the window
            self.clock = pygame.time.Clock() # create a clock
            self._initialized = True # one is all done state is inicialized
            self.scene = None
            self.player = None
            self.enemy = None
    #load the necessary text that the game will be using from the json
   
    
    #change the resolution of the screen
    def change_resolution(self):
        self.screen = pygame.display.set_mode((ConfigManager().get_instance().get_width(), ConfigManager().get_instance().get_height())) 

    #functions to load different scenes
    def load_menu(self):
        if self.scene:
            self.scene.cleanup() 
        from ui.menu import Menu
        self.scene =  Menu()
        
    def load_options(self):
        if self.scene:
            self.scene.cleanup()
        from ui.options import Options
        self.scene = Options()
    
    def load_game(self, scene, sound):
        if self.scene:
            self.scene.cleanup()
        if self.player == None:
            from classes.player import Player
            self.player = Player(ConfigManager().get_instance().get_width()/2, ConfigManager().get_instance().get_height()/2)
        from game.game import Game
        self.scene = Game(scene, sound)

    def load_loading(self):
        if self.scene:
            self.scene.cleanup()
        from utils.load import Load
        self.scene =  Load()
        
    def load_credits(self):
        if self.scene:
            self.scene.cleanup()
        from views.credits import Credits
        self.scene =  Credits()
    
    def load_pause(self):
        from ui.pausa import Pausa
        Pausa()
                 
    def end_game(self):
        if self.scene:
            self.scene.cleanup()
        from views.gameOver import GameOver
        self.player = None
        self.scene =  GameOver()

    def load_start(self):
        if self.scene:
            self.scene.cleanup()
        from views.start import Start
        self.scene = Start(path = "1animation", sound = "../Sound/BSO/levels-_1_.wav", event = 1)
 
    

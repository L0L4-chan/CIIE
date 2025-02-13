'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys, utils.auxiliar as auxiliar 
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
            pygame.init()
            pygame.mixer.pre_init(44100,16,2,4096) #initialize the mixer (sound)
            pygame.mixer.init()
            pygame.mixer.music.load("../Sound/BSO/Credits.wav") #load by default the menu music
            pygame.mixer.music.play() #start the music
            self.config = ConfigManager()
            self.config.load_fonts()
            self.screen = pygame.display.set_mode((self.config.get_width(), self.config.get_height()))  # screen size default 1280 x 720
            pygame.display.set_caption("Skelly & Soulie") #display name of the game on the edge of the window
            self.clock = pygame.time.Clock() # create a clock
            self.running = True # bool for game loop
            self.change_texts(self.config.get_language()) # load text on the apropiate language
            self._initialized = True # one is all done state is inicialized

    #load the necessary text that the game will be using from the json
    #@param string language
    def change_texts(self, language):
        self.texts = auxiliar.load_json(f"../Dialog/{language}.json")
        self.btn_text = auxiliar.load_json(f"../ButtonText/{language}.json")
    
    
    #change the language configuration
    def change_language(self, language):
        self.textos = self.change_texts(language)
    
    #change the resolution of the screen
    def change_resolution(self):
        self.screen = pygame.display.set_mode((self.config.width, self.config.height)) 

    #functions to load different scenes
    def load_menu(self):
        from ui.menu import Menu
        self.scene =  Menu()
        
    def load_options(self):
        from ui.options import Options
        self.scene = Options()
    
    def load_game(self):
        from game import Game
        self.scene = Game()

    def load_pause(self):
        from ui.pausa import Pausa
        self.scene = Pausa()

    def load_loading(self):
        from utils.load import Load
        self.scene =  Load()
        
    def load_inventory(self):
        from inventory import Inventory
        self.scene = Inventory()

    def load_start(self):
        from views.start import Start
        self.scene = Start(path = "1animation", sound = "..\Sound/BSO/levels-_1_.wav", event = 1)

    # game loop
    def run(self):
        while self.running:
            self.scene.run()  # it will delegate on the scene loop

        pygame.quit()
        sys.exit()
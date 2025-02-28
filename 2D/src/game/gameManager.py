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
            ConfigManager().get_instance().load_fonts()
            self.screen = pygame.display.set_mode((ConfigManager().get_instance().get_width(), ConfigManager().get_instance().get_height()))  # screen size default 1280 x 720
            pygame.display.set_caption("Skelly & Soulie") #display name of the game on the edge of the window
            self.clock = pygame.time.Clock() # create a clock
            self._initialized = True # one is all done state is inicialized
            self.scene = None
            self.player = None
            self.enemy = None
            self.music = False
            self.music_on()
    
    def first_scene(self):
        from ui.menu import Menu
        self.scene = Menu()
    
    def music_on(self):
        if(not self.music):
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load("../Sound/BSO/Credits.wav")
                #pygame.mixer.music.play()
                self.music = True
   
    
    #change the resolution of the screen
    def change_resolution(self):
        self.screen = pygame.display.set_mode((ConfigManager().get_instance().get_width(), ConfigManager().get_instance().get_height())) 

    #functions to load different scenes
    def load_menu(self):
        if self.scene:
            self.scene.stop()
        self.music_on() 
        from ui.menu import Menu
        self.next_scene =  Menu()
        
        
    def load_options(self):
        if self.scene:
            self.scene.stop()
        from ui.options import Options
        self.next_scene = Options()
       
    
    def load_game(self, scene, sound, level):
        if self.scene:
            self.scene.stop()
        if self.player == None:    
            self.load_player(level)
        else:
            self.load_player(level, self.player.get_lifes())
        from game.game import Game
        self.next_scene = Game(scene, sound)
        

    def load_player(self, level, lifes=3):
        if level == 1:
            from classes.player import Player
            self.player = Player(ConfigManager().get_instance().get_width()/2, ConfigManager().get_instance().get_height()/2)    
        elif level == 2: 
            from classes.player1 import Player1
            self.player = Player1(ConfigManager().get_instance().get_width()/2, ConfigManager().get_instance().get_height()/2,lifes)
        else:
            from classes.player2 import Player2
            self.player = Player2(ConfigManager().get_instance().get_width()/2, ConfigManager().get_instance().get_height()/2,lifes)
    


    def load_loading(self):
        if self.scene:
            self.scene.stop()
        from utils.load import Load
        self.next_scene =  Load()
        
    def load_credits(self):
        if self.scene:
            self.scene.stop()
        self.music = False
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load("../Sound/BSO/Credits.wav")
        #pygame.mixer.music.play()
        from views.credits import Credits
        self.next_scene =  Credits()
        
    
    def load_pause(self):
        from ui.pausa import Pausa
        Pausa().run()
                 
    def end_game(self):
        if self.scene:
            self.scene.stop()
        from views.gameOver import GameOver
        self.player = None
        self.music = False
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load("../Sound/BSO/game_over.wav")
        #pygame.mixer.music.play()
        self.next_scene =  GameOver()
       

    def load_start(self, path):
        if self.scene:
            self.scene.stop()
        from views.start import Start
        self.next_scene = Start(path =path)
        
 
    def run(self):
        self.first_scene()
        while self.scene is not None:
            self.scene.run()
            
            # Verificar si la escena terminó
            if not self.scene.get_running():
                self.scene.cleanup()
                
                # Verificar si hay una nueva escena o salir
                if self.next_scene is not None:
                    self.scene = self.next_scene
                    self.next_scene = None
                else:
                    break 

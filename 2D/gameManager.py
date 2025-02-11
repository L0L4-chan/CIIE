'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys, auxiliar 


class GameManager():

    #singleton
    _instance = None

    #Variables
    WIDTH =  1280 #screen
    HEIGTH = 720 #screen
    FPS = 60 #frames per second
    ONGAME = False # in case of being on game
    PAUSE = False # in case of pause

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance._initialized = False  
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = GameManager()  
        return cls._instance


    def __init__(self):
        if not self._initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGTH))  # Tamaño por defecto, puede cambiarse
            pygame.display.set_caption("Skelly & Soulie")
            self.clock = pygame.time.Clock()
            self.running = True

            #default configuration 
            self.config = {
                "language" : "spanish",
                "difficulty" : "normal",
                #otras configuraciones a utilizar
            }

            self.change_texts(self.config["language"])
            self._initialized = True

    def change_texts(self, language):
        self.texts = auxiliar.load_json(f"Dialog/{language}.json")
        self.btn_text = auxiliar.load_json(f"ButtonText/{language}.json")

    def change_language(self, language):
        self.config["language"] = language
        self.textos = self.load_texts(language)

    def load_menu(self):
        from menu import Menu
        self.scene =  Menu()
        
    def load_options(self):
        from options import Options
        self.scene = Options()
    
    def load_game(self):
        from game import Game
        self.scene = Game()

    def load_pause(self):
        from pausa import Pausa
        self.scene = Pausa()

    def load_loading(self):
        from load import Load
        self.scene =  Load()
        
    def load_inventory(self):
        from inventory import Inventory
        self.scene = Inventory()

    def load_start(self):
        from start import Start
        self.scene = Start()

    def run(self):
        while self.running:
            self.scene.run()  

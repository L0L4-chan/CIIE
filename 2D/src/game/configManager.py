import pygame

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False  
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.language = "spanish"
            self.difficulty = 2
            self.width = 1280
            self.height = 720
            self.fps = 60
            self.artpath = "big"
            
            self.lettering = 48
            self.btn_lettering = 30

            self._initialized = True  

    def load_fonts(self):
       
        self.fonts_titles = pygame.font.Font("../Font/Cryptik/Cryptik.ttf", self.lettering)
        self.fonts_text =  pygame.font.SysFont("arial", self.btn_lettering)
        
        

    #setter
    def update_config(self, language = "spanish", difficulty = 2, width = 1280 ,height = 720, artpath = "big", lettering = 48, btn_lettering = 30):
        
        self.language = language
        self.difficulty = difficulty
        self.width = width
        self.height = height
        self.artpath = artpath     
        self.lettering = lettering
        self.btn_lettering = btn_lettering
            
    

    #getters
    def get_language(self):
        return self.language
    
    def get_difficukty(self):
        return self.difficulty
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_fps(self):
        return self.fps
    
    def get_artpath(self):
        return self.artpath

    def get_font_titlew(self):
        return self.fonts_titles
    
    def get_font(self):
        return self.fonts_text

    def get_size_ltt(self):
        return self.lettering
    
    def get_size_btn_ltt(self):
        return self.btn_lettering
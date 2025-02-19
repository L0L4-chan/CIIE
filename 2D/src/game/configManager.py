import pygame, utils.auxiliar

class ConfigManager:
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False  
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None: 
            cls._instance = ConfigManager() #create instance  
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.language = "spanish"
            self.difficulty = 2
            self.conf = utils.auxiliar.load_json("../config/1280x720.json")
            self.change_texts(self.language) # load text on the apropiate language
            self._initialized = True 
            self.fps = 60 

    def load_fonts(self):
       
        self.fonts_titles = pygame.font.Font("../Font/Cryptik/Cryptik.ttf",  self.conf["lettering"])
        self.fonts_text =  pygame.font.SysFont("arial",self.conf["btn_lettering"])
        self.font_dialog = pygame.font.SysFont("arial", (self.conf["btn_lettering"] // 2))
        

    #setter
    def update_config_lang(self, language):
        
        self.language = language
        self.change_language(language)
    
    def update_config_difficulty(self, difficulty):
        self.difficulty = difficulty
        
    def update_config_meassurement(self, path):
        self.conf = utils.auxiliar.load_json(path)
        self.load_fonts()    
     #@param string language
    def change_texts(self, language):
        self.texts = utils.auxiliar.load_json(f"../Dialog/{language}.json")
        self.btn_text = utils.auxiliar.load_json(f"../ButtonText/{language}.json")
    
    
    #change the language configuration
    def change_language(self, language):
        self.textos = self.change_texts(language)

    #getters
    def get_language(self):
        return self.language
    
    def get_difficulty(self):
        return self.difficulty
    
    def get_width(self):
        return self.conf["width"]
    
    def get_height(self):
        return self.conf["height"]
    
    def get_fps(self):
        return self.fps
    
    def get_artpath(self):
        return self.conf["art_path"]

    def get_font_title(self):
        return self.fonts_titles
    
    def get_font_dialog(self):
        return self.font_dialog
    
    def get_font(self):
        return self.fonts_text

    def get_size_ltt(self):
        return self.conf["lettering"]
    
    def get_size_btn_ltt(self):
        return self.conf["btn_lettering"]
    
    def get_text(self, key):
        return self.texts[key]
    
    def get_text_button(self, key):
        return self.btn_text[key]
    
    def get_player_W(self):
        return self.conf["pw"]
    
    def get_player_H(self):
        return self.conf["ph"]
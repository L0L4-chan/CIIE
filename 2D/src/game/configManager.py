import pygame, utils.auxiliar as auxiliar

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
            self.conf = auxiliar.load_json(auxiliar.get_path("config/1280x720.json"))
            self.change_texts(self.language) # load text on the apropiate language
            self._initialized = True 
            self.fps = 60
    def load_fonts(self):
        self.fonts_titles = pygame.font.Font(auxiliar.get_path("Font/Cryptik/Cryptik.ttf"),  self.conf["lettering"])
        self.fonts_text =  pygame.font.SysFont("arial",self.conf["btn_lettering"])
        self.font_dialog = pygame.font.SysFont("arial", (self.conf["btn_lettering"] // 2))
        

    #setter
    def update_config_lang(self, language):
        
        self.language = language
        self.change_language(language)
    
    def update_config_difficulty(self, difficulty):
        self.difficulty = difficulty
        
    def update_config_meassurement(self, path):
        self.conf = auxiliar.load_json(auxiliar.get_path(path))
        self.load_fonts()    
     #@param string language
    def change_texts(self, language):
        self.texts = auxiliar.load_json(auxiliar.get_path(f"Dialog/{language}.json"))
        self.btn_text = auxiliar.load_json(auxiliar.get_path(f"ButtonText/{language}.json"))
    
    
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
    
    def get_iconpath(self):
        return self.conf["icon_path"]
    
    def get_audiofxpath(self, name):
        return self.conf["audio_fx_path"] + name


    def get_audiobspath(self, name):
        return self.conf["audio_bs_path"] + name
    
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
    
    def get_player_Acc(self):
        return self.conf["Acc"]
    
    def get_player_speed(self):
        return self.conf["speed"]
    
    def get_player_jump(self):
        return self.conf["jump"]
    
    def get_player_fric(self):
        return self.conf["fric"]
    
    def get_player_posx(self, p):
        return self.conf[f"level{p}x"]
    
    
    def get_player_posy(self,p):
        return self.conf[f"level{p}y"]
    
    def get_stone_v(self):
        return self.conf["stone"]
    
    def get_stone_r(self):
        return self.conf["rev_stone"]
    

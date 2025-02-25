'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys 
from game.gameManager import GameManager
from game.configManager import ConfigManager
from ui.button import Button
class Options():

    
    def __init__(self):
        super().__init__() 
        self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/Options.jpg")
        self.screen_width = ConfigManager().get_instance().get_width()
        self.screen_height =  ConfigManager().get_instance().get_height()
        self.running = False
        self.font =  ConfigManager().get_instance().get_font_title()
        self.LANGUAGE = ConfigManager().get_instance().get_text_button(key ="LANGUAGE")
        self.op_1 = ConfigManager().get_instance().get_text_button(key ="galician")
        self.op_2 = ConfigManager().get_instance().get_text_button(key ="english")
        self.op_3 = ConfigManager().get_instance().get_text_button(key ="spanish")
        self.DIFFICULTY = ConfigManager().get_instance().get_text_button(key ="DIFFICULTY")
        self.easy = ConfigManager().get_instance().get_text_button(key ="easy")
        self.meddium= ConfigManager().get_instance().get_text_button(key ="medium")
        self.hard = ConfigManager().get_instance().get_text_button(key ="hard")
        self.RESOLUTION = ConfigManager().get_instance().get_text_button(key ="RESOLUTION")
        self.big = ConfigManager().get_instance().get_text_button(key ="big")
        self.small = ConfigManager().get_instance().get_text_button(key ="small")
        self. BACK = ConfigManager().get_instance().get_text_button(key ="BACK")
        self.screen = GameManager().get_instance().screen
        # Botones del menú
        self.new_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["galician"].checkForInput(pygame.mouse.get_pos()):
                   self.change_language("galician")
                if self.buttons["english"].checkForInput(pygame.mouse.get_pos()):
                   self.change_language( "english")
                if self.buttons["spanish"].checkForInput(pygame.mouse.get_pos()):
                   self.change_language("spanish")
                if self.buttons["easy"].checkForInput(pygame.mouse.get_pos()):
                   ConfigManager().get_instance().update_config_difficulty(1)
                if self.buttons["medium"].checkForInput(pygame.mouse.get_pos()):
                   ConfigManager().get_instance().update_config_difficulty(2)
                if self.buttons["hard"].checkForInput(pygame.mouse.get_pos()):
                   ConfigManager().get_instance().update_config_difficulty(3)
                if self.buttons["small"].checkForInput(pygame.mouse.get_pos()):                   
                   self.change_resolution("../config/720x405.json")
                if self.buttons["big"].checkForInput(pygame.mouse.get_pos()):
                   self.change_resolution("../config/1280x720.json")
                if self.buttons["BACK"].checkForInput(pygame.mouse.get_pos()):
                   self.running = False
                   GameManager().get_instance().load_menu()
                   
    
    def change_language(self,language): 
        ConfigManager().get_instance().update_config_lang(language)
        self.LANGUAGE = ConfigManager().get_instance().get_text_button(key ="LANGUAGE")
        self.op_1 = ConfigManager().get_instance().get_text_button(key ="galician")
        self.op_2 = ConfigManager().get_instance().get_text_button(key ="english")
        self.op_3 = ConfigManager().get_instance().get_text_button(key ="spanish")
        self.DIFFICULTY = ConfigManager().get_instance().get_text_button(key ="DIFFICULTY")
        self_easy = ConfigManager().get_instance().get_text_button(key ="easy")
        self.meddium= ConfigManager().get_instance().get_text_button(key ="medium")
        self.hard = ConfigManager().get_instance().get_text_button(key ="hard")
        self.RESOLUTION = ConfigManager().get_instance().get_text_button(key ="RESOLUTION")
        self.big = ConfigManager().get_instance().get_text_button(key ="big")
        self.small = ConfigManager().get_instance().get_text_button(key ="small")
        self. BACK = ConfigManager().get_instance().get_text_button(key ="BACK")
        self.new_buttons()
        
                   
    
    def change_resolution(self, path):
        ConfigManager().get_instance().update_config_meassurement(path)  
        self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/Options.jpg")
        self.screen_width = ConfigManager().get_instance().get_width()
        self.screen_height =  ConfigManager().get_instance().get_height() 
        GameManager().get_instance().change_resolution()
        self.new_buttons()


    def new_buttons(self):        
        self.buttons = {
            "galician": Button(pos=((self.screen_width/12)*5, (self.screen_height/10)*3), text_input= self.op_1),
            "english": Button(pos=((self.screen_width/12)*7, (self.screen_height/10)*3), text_input= self.op_2),
            "spanish": Button(pos=((self.screen_width/12)*9, (self.screen_height/10)*3), text_input= self.op_3 ),
            "easy": Button(pos=((self.screen_width/12)*5, (self.screen_height/10)*5), text_input= self.easy),
            "medium": Button(pos=((self.screen_width/12)*7, (self.screen_height/10)*5), text_input= self.meddium),
            "hard": Button(pos=((self.screen_width/12)*9, (self.screen_height/10)*5), text_input= self.hard ),
            "small": Button(pos=((self.screen_width/8)*4, (self.screen_height/10)*7), text_input= self.small),
            "big": Button(pos=((self.screen_width/8)*6, (self.screen_height/10)*7), text_input= self.big),
            "BACK": Button(pos=((self.screen_width/8)*5, (self.screen_height/10)*8), text_input=self. BACK )
            }
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        menu_text =self.font.render("OPTIONS", True, (255, 255, 255))
        self.screen.blit(menu_text, ((self.screen_width/8)*4, (self.screen_height/10)*1))
        language_text =self.font.render(self.LANGUAGE, True, (255, 255, 255))
        self.screen.blit(language_text, ((self.screen_width/8)*4, (self.screen_height/10)*2))
        difficulty_text =self.font.render(self.DIFFICULTY, True, (255, 255, 255))
        self.screen.blit(difficulty_text, ((self.screen_width/8)*4, (self.screen_height/10)*4))
        resolution_text =self.font.render(self.RESOLUTION, True, (255, 255, 255))
        self.screen.blit(resolution_text, ((self.screen_width/8)* 4, (self.screen_height/10)*6))
        
        for btn in self.buttons.values():
            btn.update(self.screen)

        pygame.display.update()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
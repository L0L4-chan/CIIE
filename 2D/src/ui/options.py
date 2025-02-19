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
        

        # Botones del menú
        self.new_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameManager().get_instance().running = False  
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["galician"].checkForInput(pygame.mouse.get_pos()):
                   ConfigManager().get_instance().update_config_lang("galician")
                   self.new_buttons()
                if self.buttons["english"].checkForInput(pygame.mouse.get_pos()):
                   ConfigManager().get_instance().update_config_lang( "english")
                   self.new_buttons()
                if self.buttons["spanish"].checkForInput(pygame.mouse.get_pos()):
                   ConfigManager().get_instance().update_config_lang("spanish")
                   self.new_buttons()
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
                   GameManager().get_instance().load_menu()
                    
    
    def change_resolution(self, path):
        ConfigManager().get_instance().update_config_meassurement(path)  
        self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/Options.jpg") 
        GameManager().get_instance().change_resolution()
        self.new_buttons()


    def new_buttons(self):        
        self.buttons = {
            "galician": Button(pos=((ConfigManager().get_instance().get_width()/12)*5, (ConfigManager().get_instance().get_height()/10)*3), text_input= ConfigManager().get_instance().get_text_button(key ="galician")),
            "english": Button(pos=((ConfigManager().get_instance().get_width()/12)*7, (ConfigManager().get_instance().get_height()/10)*3), text_input= ConfigManager().get_instance().get_text_button(key ="english")),
            "spanish": Button(pos=((ConfigManager().get_instance().get_width()/12)*9, (ConfigManager().get_instance().get_height()/10)*3), text_input= ConfigManager().get_instance().get_text_button(key ="spanish")),
            "easy": Button(pos=((ConfigManager().get_instance().get_width()/12)*5, (ConfigManager().get_instance().get_height()/10)*5), text_input= ConfigManager().get_instance().get_text_button(key ="easy")),
            "medium": Button(pos=((ConfigManager().get_instance().get_width()/12)*7, (ConfigManager().get_instance().get_height()/10)*5), text_input= ConfigManager().get_instance().get_text_button(key ="medium")),
            "hard": Button(pos=((ConfigManager().get_instance().get_width()/12)*9, (ConfigManager().get_instance().get_height()/10)*5), text_input= ConfigManager().get_instance().get_text_button(key ="hard")),
            "small": Button(pos=((ConfigManager().get_instance().get_width()/8)*4, (ConfigManager().get_instance().get_height()/10)*7), text_input= ConfigManager().get_instance().get_text_button(key ="small")),
            "big": Button(pos=((ConfigManager().get_instance().get_width()/8)*6, (ConfigManager().get_instance().get_height()/10)*7), text_input= ConfigManager().get_instance().get_text_button(key ="big")),
            "BACK": Button(pos=((ConfigManager().get_instance().get_width()/8)*5, (ConfigManager().get_instance().get_height()/10)*8), text_input= ConfigManager().get_instance().get_text_button(key ="BACK"))
            }
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    def render(self):
        GameManager().get_instance().screen.blit(self.bg, (0, 0))
        menu_text = ConfigManager().get_instance().get_font_title().render("OPTIONS", True, (255, 255, 255))
        GameManager().get_instance().screen.blit(menu_text, ((ConfigManager().get_instance().get_width()/8)*4, (ConfigManager().get_instance().get_height()/10)*1))
        language_text = ConfigManager().get_instance().get_font_title().render(ConfigManager().get_instance().get_text_button(key ="LANGUAGE"), True, (255, 255, 255))
        GameManager().get_instance().screen.blit(language_text, ((ConfigManager().get_instance().get_width()/8)*4, (ConfigManager().get_instance().get_height()/10)*2))
        difficulty_text = ConfigManager().get_instance().get_font_title().render(ConfigManager().get_instance().get_text_button(key ="DIFFICULTY"), True, (255, 255, 255))
        GameManager().get_instance().screen.blit(difficulty_text, ((ConfigManager().get_instance().get_width()/8)*4, (ConfigManager().get_instance().get_height()/10)*4))
        resolution_text = ConfigManager().get_instance().get_font_title().render(ConfigManager().get_instance().get_text_button(key ="RESOLUTION"), True, (255, 255, 255))
        GameManager().get_instance().screen.blit(resolution_text, ((ConfigManager().get_instance().get_width()/8)* 4, (ConfigManager().get_instance().get_height()/10)*6))
        
        for btn in self.buttons.values():
            btn.update(GameManager().get_instance().screen)

        pygame.display.update()

    def run(self):
        while GameManager().get_instance().running and GameManager().get_instance().scene == self:
            self.handle_events()
            self.update()
            self.render()
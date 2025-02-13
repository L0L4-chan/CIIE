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
        self.config = ConfigManager().get_instance() 
        self.gameManager = GameManager.get_instance()  
        self.bg = pygame.image.load(f"../Art/{self.config.get_artpath()}/background/Options.jpg")
        

        # Botones del menú
        self.new_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.running = False  
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["galician"].checkForInput(pygame.mouse.get_pos()):
                   self.config.update_config(language = "galician")
                   self.gameManager.change_language("galician")
                   self.new_buttons()
                if self.buttons["english"].checkForInput(pygame.mouse.get_pos()):
                   self.config.update_config(language = "english")
                   self.gameManager.change_language("english")
                   self.new_buttons()
                if self.buttons["spanish"].checkForInput(pygame.mouse.get_pos()):
                   self.config.update_config(language = "spanish")
                   self.gameManager.change_language("spanish")
                   self.new_buttons()
                if self.buttons["easy"].checkForInput(pygame.mouse.get_pos()):
                   self.config.update_config(difficulty =  1)
                if self.buttons["medium"].checkForInput(pygame.mouse.get_pos()):
                   self.config.update_config(difficulty =  2)
                if self.buttons["hard"].checkForInput(pygame.mouse.get_pos()):
                   self.config.update_config(difficulty =  3  ) 
                if self.buttons["small"].checkForInput(pygame.mouse.get_pos()):                   
                   self.change_resolution(width = 720, heigth = 405, ltt= 20, btn_ltt = 16, art ="small")
                if self.buttons["big"].checkForInput(pygame.mouse.get_pos()):
                   self.change_resolution(width = 1280, heigth = 720, ltt= 48, btn_ltt = 30, art ="big")
                if self.buttons["BACK"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.load_menu()
                    
    
    def change_resolution(self, width, heigth, ltt, btn_ltt, art):
        self.config.update_config(width=width, height=heigth, lettering=ltt, btn_lettering=btn_ltt, artpath=art ) 
        self.config.load_fonts() 
        self.bg = pygame.image.load(f"../Art/{self.config.get_artpath()}/background/Options.jpg") 
        self.gameManager.change_resolution()
        self.new_buttons()


    def new_buttons(self):        
        self.buttons = {
            "galician": Button(pos=((self.config.get_width()/12)*5, (self.config.get_height()/10)*3), text_input= self.gameManager.btn_text["galician"]),
            "english": Button(pos=((self.config.get_width()/12)*7, (self.config.get_height()/10)*3), text_input= self.gameManager.btn_text["english"]),
            "spanish": Button(pos=((self.config.get_width()/12)*9, (self.config.get_height()/10)*3), text_input= self.gameManager.btn_text["spanish"]),
            "easy": Button(pos=((self.config.get_width()/12)*5, (self.config.get_height()/10)*5), text_input= self.gameManager.btn_text["easy"]),
            "medium": Button(pos=((self.config.get_width()/12)*7, (self.config.get_height()/10)*5), text_input= self.gameManager.btn_text["medium"]),
            "hard": Button(pos=((self.config.get_width()/12)*9, (self.config.get_height()/10)*5), text_input= self.gameManager.btn_text["hard"]),
            "small": Button(pos=((self.config.get_width()/8)*4, (self.config.get_height()/10)*7), text_input= self.gameManager.btn_text["small"]),
            "big": Button(pos=((self.config.get_width()/8)*6, (self.config.get_height()/10)*7), text_input= self.gameManager.btn_text["big"]),
            "BACK": Button(pos=((self.config.get_width()/8)*5, (self.config.get_height()/10)*8), text_input= self.gameManager.btn_text["BACK"])
            }
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    def render(self):
        self.gameManager.screen.blit(self.bg, (0, 0))
        menu_text = self.config.get_font_titlew().render("OPTIONS", True, (255, 255, 255))
        self.gameManager.screen.blit(menu_text, ((self.config.get_width()/8)*4, (self.config.get_height()/10)*1))
        language_text = self.config.get_font_titlew().render(self.gameManager.btn_text["LANGUAGE"], True, (255, 255, 255))
        self.gameManager.screen.blit(language_text, ((self.config.get_width()/8)*4, (self.config.get_height()/10)*2))
        difficulty_text = self.config.get_font_titlew().render(self.gameManager.btn_text["DIFFICULTY"], True, (255, 255, 255))
        self.gameManager.screen.blit(difficulty_text, ((self.config.get_width()/8)*4, (self.config.get_height()/10)*4))
        resolution_text = self.config.get_font_titlew().render(self.gameManager.btn_text["RESOLUTION"], True, (255, 255, 255))
        self.gameManager.screen.blit(resolution_text, ((self.config.get_width()/8)* 4, (self.config.get_height()/10)*6))
        
        for btn in self.buttons.values():
            btn.update(self.gameManager.screen)

        pygame.display.update()

    def run(self):
        while self.gameManager.running and self.gameManager.scene == self:
            self.handle_events()
            self.update()
            self.render()
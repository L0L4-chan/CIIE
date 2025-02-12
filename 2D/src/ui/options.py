'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys 
from gameManager import GameManager
from src.ui.button import Button

class Options():

    
    def __init__(self):
        super().__init__()
        self.gameManager = GameManager.get_instance() 
        self.screen = self.gameManager.screen  
        self.bg = pygame.image.load(f"Art/{self.gameManager.artpath}/background/Options.jpg")
        self.font = pygame.font.SysFont('arial', self.gameManager.lettering) 
        

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
                   self.gameManager.config["language"] = "galician"
                   self.gameManager.change_language("galician")
                   self.new_buttons()
                if self.buttons["english"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.config["language"] = "english"
                   self.gameManager.change_language("english")
                   self.new_buttons()
                if self.buttons["spanish"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.config["language"] = "spanish"
                   self.gameManager.change_language("spanish")
                   self.new_buttons()
                if self.buttons["easy"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.config["difficulty"] = 1
                if self.buttons["medium"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.config["difficulty"] = 2
                if self.buttons["hard"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.config["difficulty"] = 3   
                if self.buttons["small"].checkForInput(pygame.mouse.get_pos()):
                   self.change_resolution(width = 720, heigth = 405, ltt= 30, btn_ltt = 20, art ="small")
                if self.buttons["big"].checkForInput(pygame.mouse.get_pos()):
                   self.change_resolution(width = 1280, heigth = 720, ltt= 48, btn_ltt = 30, art ="big")
                if self.buttons["BACK"].checkForInput(pygame.mouse.get_pos()):
                   self.gameManager.load_menu()
                    
    
    def change_resolution(self, width, heigth, ltt, btn_ltt, art):
        self.gameManager.WIDTH = width
        self.gameManager.HEIGTH = heigth
        self.gameManager.lettering = ltt
        self.gameManager.btn_lettering = btn_ltt
        self.gameManager.artpath = art
        self.font = pygame.font.SysFont('arial', self.gameManager.lettering)  
        self.bg = pygame.image.load(f"Art/{self.gameManager.artpath}/background/Options.jpg") 
        self.gameManager.change_resolution()
        self.new_buttons()


    def new_buttons(self):
        self.buttons = {
            "galician": Button(pos=((self.gameManager.WIDTH/8)*5, (self.gameManager.HEIGTH/10)*3), text_input= self.gameManager.btn_text["galician"],size = self.gameManager.btn_lettering),
            "english": Button(pos=((self.gameManager.WIDTH/8)*6, (self.gameManager.HEIGTH/10)*3), text_input= self.gameManager.btn_text["english"],size = self.gameManager.btn_lettering),
            "spanish": Button(pos=((self.gameManager.WIDTH/8)*7, (self.gameManager.HEIGTH/10)*3), text_input= self.gameManager.btn_text["spanish"],size = self.gameManager.btn_lettering),
            "easy": Button(pos=((self.gameManager.WIDTH/8)*5, (self.gameManager.HEIGTH/10)*5), text_input= self.gameManager.btn_text["easy"],size = self.gameManager.btn_lettering),
            "medium": Button(pos=((self.gameManager.WIDTH/8)*6, (self.gameManager.HEIGTH/10)*5), text_input= self.gameManager.btn_text["medium"],size = self.gameManager.btn_lettering),
            "hard": Button(pos=((self.gameManager.WIDTH/8)*7, (self.gameManager.HEIGTH/10)*5), text_input= self.gameManager.btn_text["hard"],size = self.gameManager.btn_lettering),
            "small": Button(pos=((self.gameManager.WIDTH/6)*4, (self.gameManager.HEIGTH/10)*7), text_input= self.gameManager.btn_text["small"],size = self.gameManager.btn_lettering),
            "big": Button(pos=((self.gameManager.WIDTH/6)*5, (self.gameManager.HEIGTH/10)*7), text_input= self.gameManager.btn_text["big"],size = self.gameManager.btn_lettering),
            "BACK": Button(pos=((self.gameManager.WIDTH/4)*3, (self.gameManager.HEIGTH/10)*8), text_input= self.gameManager.btn_text["BACK"],size = self.gameManager.btn_lettering),
        }
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        menu_text = self.font.render("OPTIONS", True, (255, 255, 255))
        self.screen.blit(menu_text, ((self.gameManager.WIDTH/6)*4, (self.gameManager.HEIGTH/10)*1))
        language_text = self.font.render(self.gameManager.btn_text["LANGUAGE"], True, (255, 255, 255))
        self.screen.blit(language_text, ((self.gameManager.WIDTH/6)*4, (self.gameManager.HEIGTH/10)*2))
        difficulty_text = self.font.render(self.gameManager.btn_text["DIFFICULTY"], True, (255, 255, 255))
        self.screen.blit(difficulty_text, ((self.gameManager.WIDTH/6)*4, (self.gameManager.HEIGTH/10)*4))
        resolution_text = self.font.render(self.gameManager.btn_text["RESOLUTION"], True, (255, 255, 255))
        self.screen.blit(resolution_text, ((self.gameManager.WIDTH/6)* 4, (self.gameManager.HEIGTH/10)*6))
        
        for btn in self.buttons.values():
            btn.update(self.screen)

        pygame.display.update()

    def run(self):
        while self.gameManager.running and self.gameManager.scene == self:
            self.handle_events()
            self.update()
            self.render()
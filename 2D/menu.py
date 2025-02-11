'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys , button
from gameManager import GameManager


class Menu():

    def __init__(self):
        super().__init__()
        self.gameManager = GameManager.get_instance() 
        self.screen = self.gameManager.screen  
        self.bg = pygame.image.load("Art/background/Menu.jpg")
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
                if self.buttons["play"].checkForInput(pygame.mouse.get_pos()):
                    self.gameManager.load_start()
                if self.buttons["load"].checkForInput(pygame.mouse.get_pos()):
                    self.gameManager.load_loading()
                if self.buttons["options"].checkForInput(pygame.mouse.get_pos()):
                    self.gameManager.load_options()
                if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                    self.gameManager.running = False
                    pygame.quit()
                    sys.exit()


        
    def new_buttons(self):
         self.buttons = {
            "play": button.Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8) *3), text_input= self.gameManager.btn_text["PLAY"],size = self.gameManager.btn_lettering),
            "load": button.Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8)*4), text_input= self.gameManager.btn_text["LOAD"], size = self.gameManager.btn_lettering),
            "options": button.Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8)*5), text_input= self.gameManager.btn_text["OPTIONS"],size = self.gameManager.btn_lettering),
            "quit": button.Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8)*6), text_input= self.gameManager.btn_text["QUIT"],size = self.gameManager.btn_lettering),
        }



    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        menu_text = self.font.render("MAIN MENU", True, (255, 255, 255))
        self.screen.blit(menu_text, (self.gameManager.WIDTH/14, (self.gameManager.HEIGTH/6)))
        
        for btn in self.buttons.values():
            btn.update(self.screen)

        pygame.display.update()

    def run(self):
        while self.gameManager.running and self.gameManager.scene == self:
            self.handle_events()
            self.update()
            self.render()
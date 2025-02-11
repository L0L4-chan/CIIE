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
        self.bg = pygame.image.load("Art/background/cementerio.PNG")
        self.font = pygame.font.SysFont('arial', 70) 

        # Botones del menú
        self.buttons = {
            "play": button.Button(pos=(200, 125), text_input= self.gameManager.btn_text["PLAY"]),
            "load": button.Button(pos=(200, 225), text_input= self.gameManager.btn_text["LOAD"]),
            "options": button.Button(pos=(200, 325), text_input= self.gameManager.btn_text["OPTIONS"]),
            "quit": button.Button(pos=(200, 425), text_input= self.gameManager.btn_text["QUIT"]),
        }

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

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        menu_text = self.font.render("MAIN MENU", True, (255, 255, 255))
        self.screen.blit(menu_text, (50, 25))
        
        for btn in self.buttons.values():
            btn.update(self.screen)

        pygame.display.update()

    def run(self):
        while self.gameManager.running and self.gameManager.scene == self:
            self.handle_events()
            self.update()
            self.render()
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
from ui.button import Button

class Menu():

    def __init__(self):
        super().__init__()
        self.gameManager = GameManager.get_instance() # access to the game manager
        self.screen = self.gameManager.screen  # get screen
        self.bg = pygame.image.load(f"Art/{self.gameManager.artpath}/background/Menu.jpg") #add background
        self.font = pygame.font.SysFont('arial', self.gameManager.lettering) # set letter size and style

        # Botones del menu
        self.new_buttons() #create buttons 

    # to handle events from the mouse input
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


    # create buttons    
    def new_buttons(self):
         self.buttons = {
            "play": Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8) *3), text_input= self.gameManager.btn_text["PLAY"],size = self.gameManager.btn_lettering),
            "load": Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8)*4), text_input= self.gameManager.btn_text["LOAD"], size = self.gameManager.btn_lettering),
            "options": Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8)*5), text_input= self.gameManager.btn_text["OPTIONS"],size = self.gameManager.btn_lettering),
            "quit": Button(pos=(self.gameManager.WIDTH/8, (self.gameManager.HEIGTH/8)*6), text_input= self.gameManager.btn_text["QUIT"],size = self.gameManager.btn_lettering),
        }


    # update buttons color in case the mouse is hovering on them
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    # rendering the screen
    def render(self):
        self.screen.blit(self.bg, (0, 0)) #background
        menu_text = self.font.render("MAIN MENU", True, (255, 255, 255)) #title letters to imagen
        self.screen.blit(menu_text, (self.gameManager.WIDTH/14, (self.gameManager.HEIGTH/6))) # add to buffer
        
        for btn in self.buttons.values(): #add the buttons
            btn.update(self.screen)

        pygame.display.update() # show

    # game loop 
    def run(self):
        while self.gameManager.running and self.gameManager.scene == self:
            self.handle_events()
            self.update()
            self.render()
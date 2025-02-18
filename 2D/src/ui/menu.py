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

class Menu():

    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/Menu.jpg") #add background


        # Botones del menu
        self.new_buttons() #create buttons 

    # to handle events from the mouse input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameManager().get_instance().running = False  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["play"].checkForInput(pygame.mouse.get_pos()):
                    GameManager().get_instance().load_start()
                if self.buttons["load"].checkForInput(pygame.mouse.get_pos()):
                    GameManager().get_instance().load_loading()
                if self.buttons["options"].checkForInput(pygame.mouse.get_pos()):
                    GameManager().get_instance().load_options()
                if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                    GameManager().get_instance().running = False


    # create buttons    
    def new_buttons(self):
         self.buttons = {
            "play": Button(pos=(ConfigManager().get_instance().get_width()/8, (ConfigManager().get_instance().get_height()/8) *3), text_input= ConfigManager().get_instance().get_text_button(key = "PLAY")),
            "load": Button(pos=(ConfigManager().get_instance().get_width()/8, (ConfigManager().get_instance().get_height()/8)*4), text_input= ConfigManager().get_instance().get_text_button(key ="LOAD")),
            "options": Button(pos=(ConfigManager().get_instance().get_width()/8, (ConfigManager().get_instance().get_height()/8)*5), text_input= ConfigManager().get_instance().get_text_button(key ="OPTIONS")),
            "quit": Button(pos=(ConfigManager().get_instance().get_width()/8, (ConfigManager().get_instance().get_height()/8)*6), text_input= ConfigManager().get_instance().get_text_button(key ="QUIT")),
        }


    # update buttons color in case the mouse is hovering on them
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    # rendering the screen
    def render(self):
        GameManager().get_instance().screen.blit(self.bg, (0, 0)) #background
        menu_text = ConfigManager().get_instance().get_font_title().render("MAIN MENU", True, (255, 255, 255)) #title letters to imagen
        GameManager().get_instance().screen.blit(menu_text, (ConfigManager().get_instance().get_width()/14, (ConfigManager().get_instance().get_height()/6))) # add to buffer
        
        for btn in self.buttons.values(): #add the buttons
            btn.update(GameManager().get_instance().screen)

        pygame.display.update() # show

    # game loop 
    def run(self):
        while GameManager().get_instance().running and GameManager().get_instance().scene == self:
            self.handle_events()
            self.update()
            self.render()
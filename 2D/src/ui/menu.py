'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame ,  utils.globals as globals, utils.auxiliar as auxiliar
from game.base import Base
from ui.button import Button

class Menu(Base):

    def __init__(self):
        super().__init__()
        """
        Constructor de la clase Menu.
        """
        self.bg = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/background/Menu.jpg")) #add background
        # Botones del menu
        self.new_buttons() #create buttons
        
    # to handle events from the mouse input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["play"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["play"].make_sound()
                    self.running = False
                    globals.game.load_start("st1.json") 
                if self.buttons["load"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["load"].make_sound()
                    self.running = False 
                    globals.game.load_loading()   
                if self.buttons["options"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["options"].make_sound()
                    self.running = False 
                    globals.game.load_options()
                if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["quit"].make_sound()
                    self.running = False  

    # create buttons    
    def new_buttons(self):
         self.buttons = {
            "play": Button(pos=(self.screen_width/8, (self.screen_height/8) *3), text_input=  globals.config.get_text_button(key = "PLAY")),
            "load": Button(pos=(self.screen_width/8, (self.screen_height/8)*4), text_input=  globals.config.get_text_button(key ="LOAD")),
            "options": Button(pos=(self.screen_width/8, (self.screen_height/8)*5), text_input=  globals.config.get_text_button(key ="OPTIONS")),
            "quit": Button(pos=(self.screen_width/8, (self.screen_height/8)*6), text_input=  globals.config.get_text_button(key ="QUIT")),
        }

    # update buttons color in case the mouse is hovering on them
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    # rendering the screen
    def render(self):
        self.screen.blit(self.bg, (0, 0)) #background
        menu_text =  globals.config.get_font_title().render("MAIN MENU", True, (255, 255, 255)) #title letters to imagen
        self.screen.blit(menu_text, (self.screen_width/14, (self.screen_height/6))) # add to buffer     
        for btn in self.buttons.values(): #add the buttons
            btn.render(self.screen)
        pygame.display.update() # show

    # Liberar recursos de imágenes y botones
    def cleanup(self):
        self.running = False 
        self.bg = None
        self.buttons.clear()
        self.screen = None
        # Forzar al recolector de basura a limpiar
        import gc
        gc.collect()
       
   

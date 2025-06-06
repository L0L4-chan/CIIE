'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.globals as globals, utils.auxiliar as auxiliar

from game.base import Base
from ui.button import Button
class Options(Base):

    
    def __init__(self):
        super().__init__() 
        """
        Constructor de la clase Options.
        """
        self.bg = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/background/Options.jpg"))
        self.font =   globals.config.get_font_title()
        self.LANGUAGE =  globals.config.get_text_button(key ="LANGUAGE")
        self.op_1 =  globals.config.get_text_button(key ="galician")
        self.op_2 =  globals.config.get_text_button(key ="english")
        self.op_3 =  globals.config.get_text_button(key ="spanish")
        self.DIFFICULTY =  globals.config.get_text_button(key ="DIFFICULTY")
        self.easy =  globals.config.get_text_button(key ="easy")
        self.meddium=  globals.config.get_text_button(key ="medium")
        self.hard =  globals.config.get_text_button(key ="hard")
        self.RESOLUTION =  globals.config.get_text_button(key ="RESOLUTION")
        self.big =  globals.config.get_text_button(key ="big")
        self.small =  globals.config.get_text_button(key ="small")
        self. BACK =  globals.config.get_text_button(key ="BACK")
        # Botones del menú
        self.new_buttons()

    # Manejo de eventos del mouse
    def handle_events(self):
        """
        Manejo de eventos del mouse.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["galician"].checkForInput(pygame.mouse.get_pos()):
                   self.buttons["galician"].make_sound()
                   self.change_language("galician")
                if self.buttons["english"].checkForInput(pygame.mouse.get_pos()):
                   self.buttons["english"].make_sound()
                   self.change_language( "english")
                if self.buttons["spanish"].checkForInput(pygame.mouse.get_pos()):
                   self.buttons["spanish"].make_sound()
                   self.change_language("spanish")
                if self.buttons["easy"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["easy"].make_sound()
                    globals.config.update_config_difficulty(1)
                if self.buttons["medium"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["medium"].make_sound()
                    globals.config.update_config_difficulty(2)
                if self.buttons["hard"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["hard"].make_sound()
                    globals.config.update_config_difficulty(3)
                if self.buttons["small"].checkForInput(pygame.mouse.get_pos()):
                   self.buttons["small"].make_sound()                   
                   self.change_resolution(auxiliar.get_path("config/720x405.json"))
                if self.buttons["big"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["big"].make_sound()
                    self.change_resolution(auxiliar.get_path("config/1280x720.json"))
                if self.buttons["BACK"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["BACK"].make_sound()
                    self.running = False
                    globals.game.load_menu()
                   
    # Cambiar el idioma
    def change_language(self,language): 
        """
        Cambia el idioma del juego.
        
        :param language: Idioma al que se cambia.
        Actualiza todas las variables dependientes de texto a la nueva configuración.
        """
        globals.config.update_config_lang(language)
        self.LANGUAGE =  globals.config.get_text_button(key ="LANGUAGE")
        self.op_1 =  globals.config.get_text_button(key ="galician")
        self.op_2 =  globals.config.get_text_button(key ="english")
        self.op_3 =  globals.config.get_text_button(key ="spanish")
        self.DIFFICULTY =  globals.config.get_text_button(key ="DIFFICULTY")
        self.easy =  globals.config.get_text_button(key ="easy")
        self.meddium=  globals.config.get_text_button(key ="medium")
        self.hard =  globals.config.get_text_button(key ="hard")
        self.RESOLUTION =  globals.config.get_text_button(key ="RESOLUTION")
        self.big =  globals.config.get_text_button(key ="big")
        self.small =  globals.config.get_text_button(key ="small")
        self. BACK =  globals.config.get_text_button(key ="BACK")
        self.new_buttons()
        
                   
   # manejo de cambio de resolución 
    def change_resolution(self, path):
        """
        Cambia la resolución del juego.
            
        :param path: Ruta del archivo de configuración de la resolución.
        Actualiza todas las variables dependientes de la resolución a la nueva configuración.
        """
        globals.config.update_config_meassurement(path)  
        self.bg = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/background/Options.jpg"))
        self.screen_width =  globals.config.get_width()
        self.screen_height =   globals.config.get_height() 
        globals.game.change_resolution()
        self.new_buttons()

    # Crear botones
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
    
    # Actualizar botones
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    # Dibujar en pantalla
    def render(self):
        self.screen.blit(self.bg, (0, 0))
        menu_text =self.font.render( globals.config.get_text_button(key="OPTIONS"), True, (255, 255, 255))
        self.screen.blit(menu_text, ((self.screen_width/8)*4, (self.screen_height/10)*1))
        language_text =self.font.render(self.LANGUAGE, True, (255, 255, 255))
        self.screen.blit(language_text, ((self.screen_width/8)*4, (self.screen_height/10)*2))
        difficulty_text =self.font.render(self.DIFFICULTY, True, (255, 255, 255))
        self.screen.blit(difficulty_text, ((self.screen_width/8)*4, (self.screen_height/10)*4))
        resolution_text =self.font.render(self.RESOLUTION, True, (255, 255, 255))
        self.screen.blit(resolution_text, ((self.screen_width/8)* 4, (self.screen_height/10)*6))
        
        for btn in self.buttons.values():
            btn.render(self.screen)

        pygame.display.update()

    # Liberar recursos
    def cleanup(self):
        # Liberar recursos
        self.running = False 
        self.bg = None
        self.buttons.clear()
        self.font = None
        self.LANGUAGE = None
        self.op_1 = None
        self.op_2 = None
        self.op_3 = None
        self.DIFFICULTY = None
        self.easy = None
        self.meddium = None
        self.hard = None
        self.RESOLUTION = None
        self.big = None
        self.small = None
        self.BACK = None
        
        # Forzar la recolección de basura
        import gc
        gc.collect()


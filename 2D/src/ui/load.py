'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


import pygame, os, utils.auxiliar as auxiliar ,  utils.globals as globals
from game.base import Base
from ui.button import Button

class Load(Base):
    
    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load(auxiliar.get_path(f"Art/{ globals.config.get_artpath()}/background/Menu.jpg"))  # Cambiar fondo
        self.buttons = {}  # Contenedor de botones
        self.process_saves_in_directory()  # Procesar archivos JSON para ver qué botones se crean
        self.new_buttons()  # Crear los botones

    # Manejo de eventos del mouse
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if "2" in self.buttons and self.buttons["2"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["2"].make_sound()
                    self.running = False
                    globals.game.load_player(2, self.get_player_lifes("level_2.json"))
                    globals.game.load_start("st2.json")
                if "3" in self.buttons and self.buttons["3"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["3"].make_sound()
                    self.running = False
                    globals.game.load_player(3, self.get_player_lifes("level_3.json"))
                    globals.game.load_start("st3.json")
                if "4" in self.buttons and self.buttons["4"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["4"].make_sound()
                    self.running = False
                    globals.game.load_player(3, self.get_player_lifes("level_4.json"))
                    globals.game.load_start("st4.json")
                if self.buttons["BACK"].checkForInput(pygame.mouse.get_pos()):
                    self.buttons["BACK"].make_sound()
                    self.running = False
                    globals.game.load_menu()

    # Crear botones solo si los archivos existen
    def new_buttons(self):
        self.buttons["BACK"] = Button(pos=(self.screen_width / 2, (self.screen_height / 8) * 6),
                                      text_input= globals.config.get_text_button(key="BACK"))

    # Procesar los archivos JSON en el directorio de guardado
    def process_saves_in_directory(self):
        for filename in os.listdir(auxiliar.get_path("save")):
            if filename.lower().endswith('.json'):
                if filename == "level_2.json":
                    self.buttons["2"] = Button(pos=(self.screen_width / 6, (self.screen_height / 8) * 3),
                                        text_input= globals.config.get_text_button(key="2"))
                elif filename == "level_3.json":
                    self.buttons["3"] = Button(pos=(self.screen_width / 6, (self.screen_height / 8) * 4),
                                        text_input= globals.config.get_text_button(key="3"))
                elif filename == "level_4.json":
                    self.buttons["4"] = Button(pos=(self.screen_width / 6, (self.screen_height / 8) * 5),
                                            text_input= globals.config.get_text_button(key="BATTLE"))

    # Conseguir el número de vidasque tenia el jugador cuando guardo
    def get_player_lifes(self, level_file):
        info = auxiliar.load_json(auxiliar.get_path(f"save/{level_file}")) 
        return info["player_lifes"] 
    
    # Actualizar color de los botones si el mouse pasa sobre ellos
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.changeColor(mouse_pos)

    # Renderizar la pantalla
    def render(self):
        self.screen.blit(self.bg, (0, 0))  # Fondo
        menu_text =  globals.config.get_font_title().render( globals.config.get_text_button(key="LOAD"), True, (255, 255, 255))  # Título
        self.screen.blit(menu_text, (self.screen_width / 2, 50))  # Añadir al buffer
        for btn in self.buttons.values():  # Renderizar los botones
            btn.render(self.screen)

        pygame.display.update()  # Mostrar

    # Limpiar recursos
    def cleanup(self):
        self.running = False
        self.bg = None
        self.buttons.clear()
        self.screen = None
        import gc
        gc.collect()

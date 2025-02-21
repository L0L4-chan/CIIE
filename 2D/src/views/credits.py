'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame
import utils.auxiliar as aux
from game.gameManager import GameManager
from game.configManager import ConfigManager

class Credits:
    def __init__(self, screen):
        super().__init__()
        self.credits = aux.load_json(".../Credits/credits.json")  # Carga los créditos
        self.index = 0  # Índice del crédito actual
        self.last_update_time = pygame.time.get_ticks()  # Tiempo del último cambio
        self.running = False #bool que controla el bucle
        self.font = ConfigManager().get_instance().get_font_title()  # Fuente del texto
        self.run(screen)

    def run(self, screen):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time > 40000: # Verifica es hora de cambiar el texto
                self.index += 1  # Cambia de crtextoédito
                self.last_update_time = current_time

            # Dibujar fondo y texto
            screen.fill((0, 0, 0))  # Fondo negro
            text_surface = self.font.render(self.credits[self.index], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()  # Actualiza la pantalla
            
            if self.index >= 100 : #cambiar por el indice final de los creditos
                self.running = False  # Acabamos. podemos comprobar que haya pasado algun tiempo

        #Al finalizar 
        GameManager().get_instance().running = False

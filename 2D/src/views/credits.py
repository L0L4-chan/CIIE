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
from game.configManager import ConfigManager
from game.base import Base
from game.gameManager import GameManager

class Credits(Base):
    def __init__(self):
        super().__init__()
        self.credits = aux.load_json("../Credits/credits.json")  # Carga los créditos
        self.index = 0  # Índice del crédito actual (Asegúrate de que comience desde 0 o el índice adecuado)
        self.last_update_time = pygame.time.get_ticks()  # Tiempo del último cambio
        self.font = ConfigManager().get_instance().get_font_title()  # Fuente del texto
        self.lines = self.credits[self.index].split('\n')  # Dividir el primer crédito en líneas por saltos de línea

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time > 10000:  # Verifica si es hora de cambiar el texto
                self.index += 1  # Cambia de crédito
                self.last_update_time = current_time
                if self.index < len(self.credits):
                    self.lines = self.credits[self.index].split('\n')  # Dividir el nuevo crédito en líneas

            # Dibujar fondo y texto
            self.screen.fill((0, 0, 0))  # Fondo negro
            y_offset = self.screen.get_height() // 4  # Posición inicial en Y para dibujar el texto

            # Dibujar cada línea de texto
            for line in self.lines:
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += text_rect.height + 10  # Incrementar la posición Y para la siguiente línea

            pygame.display.flip()  # Actualiza la pantalla

            if self.index >= len(self.credits):  # Asegúrate de que el índice no se pase de la longitud de los créditos
                self.running = False  # Terminamos, si hemos mostrado todos los créditos

        GameManager().get_instance().scene_end()
        GameManager().get_instance().load_menu()
        

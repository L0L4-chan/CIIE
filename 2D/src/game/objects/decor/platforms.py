'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame 

class Platforms(pygame.sprite.Sprite):
    
    def __init__(self, x=0, y=0, width=0, height=0):
        """
        Constructor de la clase Platform.

        :param x: Posición inicial en X.
        :param y: Posición inicial en Y.
        :param width: Ancho de la plataforma.
        :param height: Alto de la plataforma.
        :return: None
        """
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.on_screen = False
        self.height = height
        self.width = width
        self.init_surf()
    
    
    def init_surf(self):
        """
        Inicializa la superficie de la plataforma.
        """
        # Se crea una superficie transparente, ignorando cualquier imagen o textura.
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))  # Color totalmente transparente      
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
              
    def draw(self, screen, position =[0,0]):
        """
        Dibuja la plataforma en pantalla.   
        Se creara de forma individualizada en las subclases.
        """
        pass  
"""
    #PRUEBA PARA COMPROBAR Y TESTEAR POSICIÓN PLATAFORMAS

    def init_surf(self):
        # Creamos una superficie sin canal alfa
        self.surf = pygame.Surface((self.width, self.height))
        # Rellenamos la superficie con un color rojo liso (RGB: 255, 0, 0)
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
              
    def draw(self, screen, position=[0, 0]):
        screen.blit(self.surf, position)

"""      
   
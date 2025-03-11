'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, random

class Platforms(pygame.sprite.Sprite):
    
    def __init__(self, x=0, y=0, width=0, height=0):
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.on_screen = False
        self.height = height
        self.width = width
        self.init_surf()
    
    
    def init_surf(self):
        # Se crea una superficie transparente, ignorando cualquier imagen o textura.
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))  # Color totalmente transparente      
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
              
    def draw(self, screen, position =[0,0]):
        pass  
   
    #PRUEBA PARA COMPROBAR Y TESTEAR POSICIÓN PLATAFORMAS
    def init_surf(self):
        # Creamos una superficie sin canal alfa
        self.surf = pygame.Surface((self.width, self.height))
        # Rellenamos la superficie con un color rojo liso (RGB: 255, 0, 0)
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
              
    def draw(self, screen, position=[0, 0]):
        screen.blit(self.surf, position)

    
    
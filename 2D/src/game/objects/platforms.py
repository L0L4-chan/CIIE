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
    
    def __init__(self, x=0, y=0, width=0, height=18, path=None):
        super().__init__()
        self.height = height
        self.x_pos = x
        self.y_pos = y
        self.on_screen = False
        if width == 0:
            width = random.randint(50, 120)
        
        # Se crea una superficie transparente, ignorando cualquier imagen o textura.
        self.surf = pygame.Surface((width, self.height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))  # Color totalmente transparente
        
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def update(self, screen):
        # Al ser invisible, no se dibuja nada.
        # Si en algún momento se requiere debug, se puede descomentar la siguiente línea
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        pass

        
 
    
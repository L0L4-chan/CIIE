'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.objects.oneuse import OneUse

class Lives(OneUse):
    def __init__(self, path , x, y):
        super().__init__(path)
        self.rect = pygame.Rect(x, y,self.image.get_width(), self.image.get_height())

        
    
    def update(self, screen):
        self.draw(screen)
    
    
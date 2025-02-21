'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame


class OneUse(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.spritesheet = pygame.image.load(path)
        self.surf = self.spritesheet
        self.inUse = False
        
    def active(self, x, y):
        self.inUse = True
        self.x_pos = x
        self.y_pos = y


    def get_inUse(self):
        return self.inUse
        
    def draw(self, screen):
        screen.blit(self.surf,self.rect.topleft)
        
    
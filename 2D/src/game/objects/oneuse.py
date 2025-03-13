'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame,  utils.globals as globals


class OneUse(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.spritesheet = pygame.image.load(f"../Art/{ globals.config.get_artpath()}/{path}")
        self.image = self.spritesheet
        self.rect = self.image.get_rect()
        self.inUse = False
        self.on_screen = False
        
    def active(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height())
        
    def set_use(self):
        self.inUse = not self.inUse    

    def get_inUse(self):
        return self.inUse
        
    def draw(self, screen, position):
        if self.inUse:
            screen.blit(self.image ,position)
        
    
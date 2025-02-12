'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, random
from game.gameManager import GameManager

class Platform(pygame.sprite.Sprite):
    
    
    def __init__(self, x = 0, y = 0, width = 0, path = None ):
        super().__init__() 
        self.gameManager = GameManager.get_instance()

        self.height = 18
        self.x_pos = x
        self.y_pos = y
        if width == 0:
            width = random.randint(50, 120)

        if path is None:
            self.surf = pygame.Surface((width, self.height))
            self.surf.fill((255,0,0))
        
        else:
            self.image = pygame.image.load(path)
            self.surf = pygame.transform.scale(self.image, (width, self.height))
        
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
        
        
    def update(self, screen):
	    screen.blit(self.surf,self.rect.topleft) 
       

        
 
    
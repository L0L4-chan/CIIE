'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.configManager import ConfigManager

class Stone(pygame.sprite.Sprite):
    
    #funcion de inicializacion de plataformas (modificar para pasar la altura por parametros cuando se tengan los escenarios)
    def __init__(self, path):
        super().__init__() 
        self.height = 20
        self.width = 20
        self.image = pygame.image.load(path)
        self.inUse = False

    def active(self, x, y ,direction ):
        self.inUse = True
        self.speed = 10 * 1 if direction else -8
        self.x_pos = x
        self.y_pos = y
        self.surf = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))


    def get_inUse(self):
        return self.inUse

    #funcion de dibujado   
    def update(self, screen, object = None):
        if(self.inUse):
            self.rect.x += self.speed
            if(self.rect.x > ConfigManager.get_instance().get_width() or (self.rect.x + self.width)<= 0):
                self.inUse = False
            #manejo de collisiones 
            hits = pygame.sprite.spritecollide(self, object, False)
            if hits:
                self.inUse = False #desaparecera por lo tanto 
            screen.blit(self.surf,self.rect.topleft)
            
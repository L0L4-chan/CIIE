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
from game.objects.oneuse import OneUse

class Stone(OneUse):
    
    #funcion de inicializacion de plataformas (modificar para pasar la altura por parametros cuando se tengan los escenarios)
    def __init__(self, path):
        super().__init__(path) 
        self.height = ConfigManager.get_instance().get_player_H()/5
        self.width = ConfigManager.get_instance().get_player_H()/5
        
        
    def active(self, x, y ,direction ):
        self.speed = 10 * 1 if direction else -8
        super().active(x,y)
        self.surf = pygame.transform.scale(self.spritesheet, (self.width, self.height))
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))

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
            super().draw(screen)
            
'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar
from game.objects.oneuse import OneUse

class Prize(OneUse):
    def __init__(self,x,y,path):
       super().__init__(path)
       super().active(x,y, 1)
       self.width = self.spritesheet.get_width()
       self.height = self.spritesheet.get_height()
       self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
       self.counter = 0
       self.sound = pygame.mixer.Sound(auxiliar.get_path("Sound/FX/Prize.wav")) #por si alguno no tiene sonido
       self.sound.set_volume(0.5)
        
    
    
    def update(self,  object = None):
        if self.inUse:
            self.counter += 1
            if self.counter >= 100:
                self.inUse = False
                self.rect.topleft = (0,0)
                self.counter = 0
                
            
                
        
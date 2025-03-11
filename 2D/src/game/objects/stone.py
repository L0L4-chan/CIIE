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
    def __init__(self):
        super().__init__("stone/001.png") 
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.counter = 3
        
        
    def active(self, x, y ,direction ):
        self.speed = 10 * 1 if direction else -8
        super().active(x,y)
        self.image = pygame.transform.scale(self.spritesheet, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.set_use()
        
    def hit(self):
        self.set_use()  
        if not self.inUse:
            self.stand_by() 
     
    def stand_by(self): 
        self.rect.topleft = (-100, -100)  # La sacamos de la pantalla
        self.speed = 0
        
    def update(self, object = None):
        if(self.inUse):
            self.rect.x += self.speed
            self.counter -= 1
            if not self.on_screen and self.counter <= 0:
                self.inUse = False
                self.stand_by()
                self.counter = 3
                
 
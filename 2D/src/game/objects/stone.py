'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.globals as globals
from game.objects.oneuse import OneUse


class Stone(OneUse):
    
    #funcion de inicializacion de plataformas (modificar para pasar la altura por parametros cuando se tengan los escenarios)
    def __init__(self):
        self.path = "stone/001.png"
        super().__init__(self.path) 
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.counter = 3
        self.speed_d = globals.config.get_stone_v()
        self.rev_speed= globals.config.get_stone_r()
        
        
    def active(self, x, y ,direction ):
        self.speed = self.speed_d * 1 if direction else - self.rev_speed
        self.image = pygame.transform.scale(self.spritesheet, (self.width, self.height))
        super().active(x,y)
        self.set_use()

        
    def hit(self):
        self.set_use()
        self.stand_by()
        self.counter = 3
     
    def stand_by(self): 
        self.rect.topleft = (0,0)  # La sacamos de la pantalla
        self.speed = 0
        
    def update(self, object = None):
        if(self.inUse):
            self.rect.x += self.speed
            self.counter -= 1
            if not self.on_screen and self.counter <= 0:
                self.hit()
                self.counter = 3
                
 
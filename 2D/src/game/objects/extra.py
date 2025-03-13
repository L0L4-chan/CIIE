'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.objects.prize import Prize

class Extra(Prize):
    def __init__(self,x,y):
       super().__init__(x,y, "prize/003.png")
       self.sound = pygame.mixer.Sound("../Sound/FX/Life.wav")
       self.sound.set_volume(0.5)
       self.to_pick= True
    
    def being_pick(self):
        self.to_pick = False
        
    def get_can_pick(self):
        return self.to_pick   
    
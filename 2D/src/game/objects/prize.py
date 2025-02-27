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

class Prize(OneUse):
    def __init__(self,x,y,path):
       super().__init__(path)
       super().active(x,y)
       self.counter = 0
        
    
    def update(self,  object = None):
        if self.inUse:
            self.counter += 1
            if self.counter >= 300:
                self.inUse = False
                
            
                
        
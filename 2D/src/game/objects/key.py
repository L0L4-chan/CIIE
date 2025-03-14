'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar
from game.objects.prize import Prize

class Key(Prize):
    def __init__(self,x,y):
       super().__init__(x,y, "prize/002.png")
       self.sound = pygame.mixer.Sound(auxiliar.get_path("Sound/FX/OpenChest.wav"))
       self.sound.set_volume(0.5)
       
    def update(self,  object = None):
        pass
                
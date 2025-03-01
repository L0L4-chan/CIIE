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

class Key(Prize):
    def __init__(self,x,y):
       super().__init__(x,y, "prize/002.png")
       #self.sound = pygame.mixer.Sound("../Sound/FX/OpenChest.wav")
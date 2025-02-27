'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.objects.lifes import Lifes

class Keys(Lifes):
    def __init__(self, x, y):
        super().__init__(path=("avatar/keys.png"))
        
    
    
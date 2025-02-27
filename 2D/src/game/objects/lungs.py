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

class Lungs(Prize):
    def __init__(self,x,y):
       super().__init__(x,y, "prize/001.png")

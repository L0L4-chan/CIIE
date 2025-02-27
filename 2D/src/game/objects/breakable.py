'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.objects.platforms import Platforms

class Breakable(Platforms):
     def __init__(self, x = 0, y = 0, width = 0, height = 18 ):
        super().__init__(x,y,width, height)
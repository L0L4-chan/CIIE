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

class Lasso(OneUse):
    def __init__(self, path):
        super().__init__(path) 
        self.height = 20
        self.width = 20
        self.image = pygame.image.load(path)
        self.inUse = False
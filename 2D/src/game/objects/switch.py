
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
vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Switch(OneUse):
    def __init__(self, path):
        super().__init__(path)
       
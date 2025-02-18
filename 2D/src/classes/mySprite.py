'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, os
from game.configManager import ConfigManager
vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class MySprite(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
    
    def update(self):
        print("Todo")
        
    def draw(self): 
        print("Todo")
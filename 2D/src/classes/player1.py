'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame
from classes.player import Player

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player1(Player):
    def __init__(self, x, y, lifes = 3):
        super().__init__(x,y)
        self.lifes = lifes
        self.shield = False 
        self.frames.update({"shield": [(( self.width* 13 ) + ( i * self.width), 0) for i in range(2)]})
        self.action_map.update({pygame.K_a: self.handle_shield})
        
    def handle_shield(self):
            self.current_action = "shield"
            self.shield = True
            
    def draw(self):
        if self.current_action == "shield" and self.index >= self.end_index:
            self.shield = False
            self.shield_counter = 0
        super().draw()    
        
       
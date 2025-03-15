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
        self.action_map.update({pygame.K_w: self.handle_shield})
        self.animation_map.update({"shield": self.animation_shield})
        
    def handle_shield(self):
        if not self.shield:
            self.current_action = "shield"
            self.shield = True
            self.index = 0
     
    def move(self):
        super().move()
        if self.current_action != "shield":
            self.shield= False 
            
    def animation_shield(self):
        if self.index >= self.end_index:
            self.shield = False
            self.current_action = "idle"
            self.index = 0
   
        
    def to_die(self):
        if not self.shield:
            super().to_die()
        self.shield = False
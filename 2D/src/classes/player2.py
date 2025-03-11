'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame

from game.objects.heart import Heart
from classes.player1 import Player1

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player2(Player1):
    def __init__(self, x, y, lifes = 3):
        super().__init__(x,y, lifes)        
        self.bombing = False 
        self.frames.update( {"bomb": [( self.width * 9 + (i * self.width), 0) for i in range(4)]})
        self.heart = Heart()
        self.bomb_counter = 300
        self.action_map.update({pygame.K_s: self.handle_bomb})
        self.group.add(self.heart)
        
    def handle_bomb(self):
        if self.bomb_counter >= 300:
            self.current_action = "bomb"
            self.bombing = True
            self.index = 0
            self.bomb_counter = 0
    
    def render(self):
        if self.current_action == "bomb" and self.index >= self.end_index-1:
            self.bombing = False
            self.explode()
        super().render()
    
    def move(self):
        if not self.bombing:
            super().move()
    
        
    def explode(self):
        if(self.direction):
            heart_x = self.pos.x + (self.rect.width * self.direction)
        else:
            heart_x = self.pos.x - (self.rect.width)
        heart_y = self.rect.y + ((self.height) /2)
        self.heart.active(x= int( heart_x), y = int(heart_y), direction= self.direction)
        self.bomb_counter = 0 
    
    def update(self):
        self.bomb_counter +=1
        super().update()
        
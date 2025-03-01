
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
from game.objects.decor.platforms import Platforms
from game.objects.decor.door import Door

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Switch(Platforms):
    def __init__(self, x, y, door_x, door_y):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/pushbutton/boton.PNG")
        self.width = self.spritesheet.get_width()/2
        self.height = self.spritesheet.get_height()
        self.frames = {"position": [(i * self.width, 0, self.width, self.height) for i in range(2)]}
        super().__init__(x,y, self.width, self.height)
        self.time = 300
        self.counter = 0
        self.door = Door(door_x, door_y)
        self.pressed = False
         
    def init_surf(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
          
    def change_position(self):
        if not self.pressed:
            self.surf = self.spritesheet.subsurface(self.frames["position"][1][0], self.frames["position"][1][1],self.width, self.height)   
            self.rect.y += (self.height / 2)
            self.door.switch_position()
            self.counter = 0
            self.pressed = True
        
    def reset(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect.y -= (self.height / 2)
        self.door.reset_back()
        self.counter = 0
        self.pressed = False
    
    def update(self):
        self.counter += 1
        if self.pressed and self.counter >= self.time:
            self.reset()
            
    def get_door(self):
        return self.door
       
    def draw(self, screen, position):
        if self.on_screen:
            screen.blit(self.surf,position) 
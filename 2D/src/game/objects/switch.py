
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
from game.objects.platforms import Platforms
from game.objects.door import Door

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Switch(Platforms):
    def __init__(self, x, y, door_x, door_y, door_w, door_h):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/pushbutton/boton.PNG")
        self.width = self.spritesheet.get_width()/2
        self.height = self.spritesheet.get_height()
        super().__init__(x,y, self.width, self.height)
        self.time = 300
        self.counter = 0
        self.on_screen = True
        self.door = Door(door_x, door_y, door_w, door_h)
        self.pressed = False
        self.frames = {
                "position": [(i * self.width, 0, self.width, self.height) for i in range(2)]  # 
            }
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
          
    def change_position(self):
        self.image = self.spritesheet.subsurface(self.frames["position"][1][0], self.frames["position"][1][1],self.width, self.height)   
        self.door.switch_position()
        self.counter = 0
        self.pressed = True
        
    
    def update(self, screen):
        self.counter += 1
        if self.pressed and self.counter >= self.time:
            self.door.switch_position()
            self.counter = 0
            self.pressed = False

        if self.on_screen:
            screen.blit(self.surf,self.rect.topleft)       
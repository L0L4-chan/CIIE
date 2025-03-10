import pygame, random
import math
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional

class Ghost(Enemy):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/ghost/sprite_sheet.png")
        super().__init__(x,y, (self.spritesheet.get_width() / 5), self.spritesheet.get_height(), False )
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(2)],
            "death": [((self.width * 2) + (i * self.width), 0) for i in range(3)]
        }
        self.frame_rate = 16
        self.move_distance = 0  # Distancia recorrida en una dirección

    def move(self):
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y* self.speed * 5
        self.move_distance += abs(self.vel.x * self.speed)

        if self.move_distance >= 100:
            self.vel.x = -self.vel.x  # Cambiar de dirección
            self.move_distance = 0

        if self.pos.x > self.screen_width - self.rect.width or self.pos.x < 0:
            self.vel.x = -self.vel.x  # Cambiar de dirección en X
        
        if self.pos.y > 300 or self.pos.y < 100:
            self.vel.y = -self.vel.y

        
        self.rect.center = self.pos

    
   

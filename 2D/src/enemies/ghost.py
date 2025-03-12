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

    #funcion que gestiona el movimiento
    def move(self):
        self.set_objective()
        distance_x = self.objective[0] - self.rect.x
        if distance_x < 0:
            self.direction = -1
        else:
            self.direction = 1
            
        if abs(distance_x) < 800 or abs(distance_x) > 50:
            self.vel.x = self.direction * self.speed
        
        # añadir movimiento de subida y bajada
        random_y_adjustment = random.randint(-1, 1)
        self.vel.y =  random_y_adjustment * self.speed
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        self.update_rect()
        


    
   

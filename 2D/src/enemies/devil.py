'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame,   utils.globals as globals
from classes.enemy import Enemy
from game.objects.stone import Stone


vec = pygame.math.Vector2  # 2 for two dimensional

class Devil(Enemy):
    
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(f"../Art/{ globals.config.get_artpath()}/devil/devil_spritesheet.png")
        super().__init__(x,y, (self.spritesheet.get_width() /6), self.spritesheet.get_height(), False )
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(4)],
            "death": [((self.width * 4 )+(i * self.width), 0) for i in range(2)]
        }
        self.frame_rate = 16
        self.move_distance = 0  # Distancia recorrida en una dirección
        self.frame_rate = 16
        self.projectiles = Stone()
        self.group.add(self.projectiles)
        self.direction = 0
        self.lifes = 1
    #funcion que gestiona el movimiento
    
    def move(self):
        self.set_objective()
        distance_x = self.objective[0] - self.rect.x
        distance_y = self.objective[1] - self.rect.y
        if distance_x < 0:
            self.direction = -1
        else:
            self.direction = 1
        if abs(distance_x) < 200:
            if abs(distance_y) < 10:
                self.shoot()
            else:
                self.vel.y = self.speed * (1 if distance_y > 0 else -1)
                self.pos.y += self.vel.y
        else:
            self.vel.x = self.speed * self.direction
            self.pos.x += self.vel.x
            
        self.update_rect()
            
        
    #funcion para disparo
    def shoot(self):
        aux = 0
        if self.direction > 0:
            stone_x = self.pos.x + (self.rect.width * self.direction)
            aux = 1
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = self.rect.y + (self.height / 2)
        if self.projectiles.get_inUse():
            return False
        else:
            self.projectiles.active(x=stone_x, y=stone_y, direction=aux)
            return True
     
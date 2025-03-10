import pygame, math
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional


class Bug(Enemy):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/bug/spritesheet.png")
        super().__init__(x,y, (self.spritesheet.get_width() /6), self.spritesheet.get_height(), False )
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(2)],
            "death": [(self.width * 4) ]
        }
        self.frame_rate = 16
        self.move_distance = 0  # Distancia recorrida en una dirección

    def move(self):
        # Movimiento del insecto: se mueve en un patrón circular
        self.pos.x += math.cos(pygame.time.get_ticks() * 0.005) * self.speed * 10
        self.pos.y += math.sin(pygame.time.get_ticks() * 0.005) * self.speed * 10

        self.rect.center = self.pos
        




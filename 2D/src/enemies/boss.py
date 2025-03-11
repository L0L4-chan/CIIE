import pygame,  math
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional


class Boss(Enemy):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/boss/spritesheet.png")

        super().__init__(x, y, (self.spritesheet.get_width() / 7), self.spritesheet.get_height(), False)
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(3)],
            "attack":  [((self.width * 3 )+(i * self.width), 0) for i in range(4)],
            "death": [((self.width * 7 )+(i * self.width), 0) for i in range(2)]
        }
        
        

    def move(self):
        # Movimiento del jefe: se mueve lentamente y hace un patrón en zig-zag
        self.pos.x += math.sin(pygame.time.get_ticks() / 300) * self.speed  # Movimiento en zig-zag
        self.pos.y += self.vel.y * self.speed

        # Rebotar en los límites de la pantalla
        if self.pos.x > self.screen_width - self.rect.width or self.pos.x < 0:
            self.vel.y = -self.vel.y  # Cambiar la dirección en Y si toca los bordes horizontales

        if self.pos.y > self.screen_height - self.rect.height or self.pos.y < 0:
            self.vel.y = -self.vel.y  # Cambiar la dirección en Y si toca los bordes verticales

        self.rect.center = self.pos

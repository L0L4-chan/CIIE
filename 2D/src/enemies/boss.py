import pygame,  math
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional


class Boss(Enemy):
    def __init__(self, x, y):
        self.surf = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/boss/spritesheet.png")
        self.rect = self.surf.get_rect()
        super().__init__(x, y)
        print("estoy en ", x , y )
        
        

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

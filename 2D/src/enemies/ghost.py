import pygame, random
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional

class Ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/ghost/ghost_1.png")  # Imagen del murciélago
        self.rect = self.surf.get_rect()

    def move(self):
        # Movimiento del fantasma: se mueve suavemente en líneas rectas en diagonal
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed

        # Cambia de dirección cada cierto tiempo
        self.frame_counter += 1
        if self.frame_counter >= self.change_direction_interval:
            self.vel.x = random.choice([1, -1])  # Cambia dirección en X aleatoriamente
            self.vel.y = random.choice([1, -1])  # Cambia dirección en Y aleatoriamente
            self.frame_counter = 0  # Reiniciar contador

        self.rect.center = self.pos

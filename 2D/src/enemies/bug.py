import pygame, sys , random
from src.classes.enemy import Enemy
from src.game.gameManager import GameManager
vec = pygame.math.Vector2 #2 for two dimensional


class Bug(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load(f"Art/{self.gameManager.artpath}/enemy/bug.png")  # Imagen del bicho
        self.rect = self.surf.get_rect()

    def move(self):
        # Movimiento del bicho: se mueve en un patrón oscilante rápido hacia los lados
        self.pos.x += math.sin(pygame.time.get_ticks() / 100) * self.speed * 2  # Oscilación rápida

        # Limitar el movimiento dentro de la pantalla
        if self.pos.x > self.gameManager.WIDTH - self.rect.width:
            self.pos.x = self.gameManager.WIDTH - self.rect.width
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.center = self.pos

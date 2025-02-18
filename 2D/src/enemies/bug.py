import pygame, math
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional


class Bug(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load(f"../img/1280x720/bug/bug_1.png")
        self.rect = self.surf.get_rect()

    def move(self):
        # Movimiento del bicho: se mueve en un patrón oscilante rápido hacia los lados
        self.pos.x += math.sin(pygame.time.get_ticks() / 100) * self.speed * 2  # Oscilación rápida

        # Limitar el movimiento dentro de la pantalla
        if self.pos.x > ConfigManager().get_instance().get_width() - self.rect.width:
            self.pos.x =  ConfigManager().get_instance().get_width() - self.rect.width
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.center = self.pos

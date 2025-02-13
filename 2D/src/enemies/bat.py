import pygame, sys , random
from src.classes.enemy import Enemy
from src.game.gameManager import GameManager
vec = pygame.math.Vector2 #2 for two dimensional

class Bat(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load(f"../img/1280x720/bat/bat.png")  # Imagen del murciélago
        self.rect = self.surf.get_rect()

    def move(self):
        # Movimiento del murciélago: se mueve hacia los lados de manera oscilante
        self.pos.x += self.vel.x * self.speed
        self.pos.y += pygame.math.sin(pygame.time.get_ticks() / 500) * self.speed  # Movimiento oscilante hacia arriba y abajo

        # Limitar el movimiento dentro de la pantalla
        if self.pos.x > self.config.get_width() - self.rect.width:
            self.vel.x = -abs(self.vel.x)  # Rebotar a la izquierda
        if self.pos.x < 0:
            self.vel.x = abs(self.vel.x)  # Rebotar a la derecha
        if self.pos.y > self.config.get_height() - self.rect.height:
            self.pos.y =self.config.get_height() - self.rect.height  # Evitar que se salga por abajo
        if self.pos.y < 0:
            self.pos.y = 0  # Evitar que se salga por arriba

        self.rect.center = self.pos

import pygame
from classes.enemy import Enemy
vec = pygame.math.Vector2 #2 for two dimensional
class Devil(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load(f"../img/1280x720/devil/devil_1.png") 
        self.rect = self.surf.get_rect()

    def move(self):
        # Movimiento del diablo: se mueve en líneas rectas y cambia de dirección al llegar a los bordes
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed

        # Rebotar en los límites de la pantalla
        if self.pos.x >  self.config.get_width() - self.rect.width or self.pos.x < 0:
            self.vel.x = -self.vel.x  # Cambia la dirección en X

        if self.pos.y >  self.config.get_height() - self.rect.height or self.pos.y < 0:
            self.vel.y = -self.vel.y  # Cambia la dirección en Y

        self.rect.center = self.pos

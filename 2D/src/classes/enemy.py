'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, sys , random
from game.gameManager import GameManager
vec = pygame.math.Vector2 #2 for two dimensional

class Enemy(pygame.sprite.Sprite):
    #variables
    ACC = 0.5
    FRIC = -0.12


    #constructor
    def __init__(self,type, x, y):
        super().__init__()
        self.gameManager = GameManager.get_instance()
        self.surf = pygame.image.load(f"img/1280x720/bat/bat_1.png")
        
        self.rect = self.surf.get_rect()
        self.pos = vec(x, y)  # Posición inicial
        self.vel = vec(1, 1)  # Movimiento inicial en la diagonal positiva (abajo a la derecha)
        self.speed = 2  # Velocidad de movimiento
        self.change_direction_interval = 60  # Intervalo para cambiar de dirección (en frames)
        self.frame_counter = 0  # Contador de frames para cambiar dirección

    def move(self):
        # Movimiento en la dirección actual
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed

        # Cambiar la dirección después de un número de frames
        self.frame_counter += 1
        if self.frame_counter >= self.change_direction_interval:
            self.vel.x = -self.vel.x  # Cambiar dirección en X (de derecha a izquierda o viceversa)
            self.vel.y = -self.vel.y  # Cambiar dirección en Y (de arriba a abajo o viceversa)
            self.frame_counter = 0  # Reiniciar el contador de frames

        # Limitar el movimiento dentro de la pantalla
        if self.pos.x > self.gameManager.WIDTH - self.rect.width:
            self.vel.x = -abs(self.vel.x)  # Rebotar a la izquierda
        if self.pos.x < 0:
            self.vel.x = abs(self.vel.x)  # Rebotar a la derecha
        if self.pos.y > self.gameManager.HEIGTH - self.rect.height:
            self.vel.y = -abs(self.vel.y)  # Rebotar hacia arriba
        if self.pos.y < 0:
            self.vel.y = abs(self.vel.y)  # Rebotar hacia abajo

        # Actualizar la posición del enemigo
        self.rect.center = self.pos

    def update(self):
        self.move()
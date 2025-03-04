'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Imagen y rectángulo del enemigo (será sobrescrito por las subclases)
        self.surf = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/bat/bat_spritesheet.png")
        self.rect = self.surf.get_rect()
        self.pos = vec(x, y)  # Posición inicial
        self.vel = vec(1, 1)  # Movimiento inicial genérico
        self.speed = 2  # Velocidad de movimiento
        self.change_direction_interval = 60  # Intervalo para cambiar de dirección (en frames)
        self.frame_counter = 0  # Contador de frames para cambiar dirección
        #almacenamos en variables locales para limitar llamadas
        self.screen_width = ConfigManager().get_instance().get_width()
        self.screen_height =  ConfigManager().get_instance().get_height()

    def move(self):
        # Movimiento genérico (será modificado por las subclases)
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed

        # Limitar el movimiento dentro de la pantalla
        if self.pos.x >self.screen_width - self.rect.width:
            self.vel.x = -abs(self.vel.x)  # Rebotar a la izquierda
        if self.pos.x < 0:
            self.vel.x = abs(self.vel.x)  # Rebotar a la derecha
        if self.pos.y > self.screen_height - self.rect.height:
            self.vel.y = -abs(self.vel.y)  # Rebotar hacia arriba
        if self.pos.y < 0:
            self.vel.y = abs(self.vel.y)  # Rebotar hacia abajo

        # Actualizar la posición del enemigo
        self.rect.center = self.pos

    def update(self):
        self.move()

    def draw(self):
        # Seleccionamos la imagen actual de la animación
        action_frames = self.frames[self.current_action]  # Lista de fotogramas para la acción actual
        frame = action_frames[self.index]  # Obtenemos el fotograma actual

        # Cargamos la imagen del sprite de acuerdo con la acción actual
        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], 64, 64))  # Usamos el tamaño de los fotogramas (64x64 por ejemplo)

        # Si la dirección es izquierda, reflejamos la imagen
        if self.vel.x < 0:  # Si se mueve hacia la izquierda
            sprite_image = pygame.transform.flip(sprite_image, True, False)

        # Establecer la superficie para dibujar
        self.surf = sprite_image

        # Actualizamos el temporizador de la animación
        self.animation_timer += 1
        if self.animation_timer > self.frame_rate:
            self.index += 1
            if self.index >= len(action_frames):
                self.index = 0  # Volver al principio de la animación si se ha acabado
            self.animation_timer = 0


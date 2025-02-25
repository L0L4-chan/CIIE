'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame

class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = pygame.math.Vector2(0, 0)
        # Margenes en píxeles según los porcentajes:
        self.left_margin = screen_width * 0.25
        self.right_margin = screen_width * 0.25
        self.top_margin = screen_height * 0.25
        self.bottom_margin = screen_height * 0.15

    def update(self, target):
        """
        Ajusta el offset de la cámara para mantener al 'target' (por ejemplo, el jugador)
        dentro de la zona segura.
        """
        # Posición del target en pantalla (en coordenadas del mundo menos el offset)
        player_screen_x = target.rect.centerx - self.offset.x
        player_screen_y = target.rect.centery - self.offset.y

        dx = 0
        dy = 0

        # Verificar si el jugador se acerca a la izquierda o derecha
        if player_screen_x < self.left_margin:
            dx = player_screen_x - self.left_margin
        elif player_screen_x > self.screen_width - self.right_margin:
            dx = player_screen_x - (self.screen_width - self.right_margin)

        # Verificar si el jugador se acerca a la parte superior o inferior
        if player_screen_y < self.top_margin:
            dy = player_screen_y - self.top_margin
        elif player_screen_y > self.screen_height - self.bottom_margin:
            dy = player_screen_y - (self.screen_height - self.bottom_margin)

        # Actualizar el offset de la cámara
        self.offset.x += dx
        self.offset.y += dy

        # Limitar el offset para que la cámara no muestre áreas fuera del mundo
        self.offset.x = max(0, min(self.offset.x, self.world_width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.world_height - self.screen_height))

    def apply(self, rect):
        """
        Devuelve una copia de 'rect' desplazada según el offset de la cámara.
        """
        return rect.move(-self.offset.x, -self.offset.y)


'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
vec = pygame.math.Vector2


class Entity(pygame.sprite.Sprite):
    """
    Clase base para todas las entidades (players, enemigos, utensilios, objetos, etc.)
    que comparten la lógica básica de movimiento y resolución de colisiones
    verticales y horizontales.
    """
    def __init__(self, x, y, width, height):
        super().__init__()
        # Posición, velocidad y aceleración de la entidad.
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.width = width
        self.height = height
        # Se crea el rectángulo de colisión usando la posición (topleft) y dimensiones.
        self.rect = pygame.Rect(x, y, width, height)
        # Flag para saber si está saltando.
        self.jumping = False

    def resolve_collisions(self, collidables, vertical_margin=10):
        """
        Resuelve las colisiones genéricas en los ejes horizontal y vertical.
        """
        # --- Resolución de colisiones horizontales ---
        hits = pygame.sprite.spritecollide(self, collidables, False)
        for hit in hits:
            if hasattr(hit, 'rect'):
                # Calcula la diferencia entre la parte inferior de la entidad y el tope del objeto.
                vertical_gap = abs(self.rect.bottom - hit.rect.top)
                # Si el gap es mayor que el margen (es decir, no está casi aterrizando)
                if vertical_gap > vertical_margin:
                    # Si se mueve a la derecha y choca con el lado izquierdo del objeto...
                    if self.vel.x > 0 and self.rect.right > hit.rect.left and self.rect.left < hit.rect.left:
                        self.rect.right = hit.rect.left
                        self.pos.x = self.rect.centerx
                        self.vel.x = 0
                    # Si se mueve a la izquierda y choca con el lado derecho del objeto...
                    elif self.vel.x < 0 and self.rect.left < hit.rect.right and self.rect.right > hit.rect.right:
                        self.rect.left = hit.rect.right
                        self.pos.x = self.rect.centerx
                        self.vel.x = 0

        # --- Resolución de colisiones verticales ---
        hits = pygame.sprite.spritecollide(self, collidables, False)
        for hit in hits:
            if hasattr(hit, 'rect'):
                # Calcula el solapamiento horizontal.
                horizontal_overlap = min(self.rect.right, hit.rect.right) - max(self.rect.left, hit.rect.left)
                if horizontal_overlap > 0:
                    # Si la entidad cae y su parte inferior choca con el tope del objeto...
                    if self.vel.y > 0 and self.rect.bottom > hit.rect.top and self.rect.top < hit.rect.top:
                        self.rect.bottom = hit.rect.top + 1
                        self.pos.y = self.rect.bottom
                        self.vel.y = 0
                        self.jumping = False
                    # Si la entidad sube y su parte superior choca con la parte inferior del objeto...
                    elif self.vel.y < 0 and self.rect.top < hit.rect.bottom and self.rect.bottom > hit.rect.bottom:
                        self.rect.top = hit.rect.bottom
                        self.pos.y = self.rect.bottom
                        self.vel.y = 0

    def update_rect(self):
        """
        Actualiza el rectángulo de colisión basado en la posición actual.
        """
        self.rect.midbottom = self.pos
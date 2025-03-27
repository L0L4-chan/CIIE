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
    
    #region __init__
    def __init__(self, x, y, width, height):
        """
        Constructor de la clase Entity, inicializa los atributos básicos de la entidad.

        :param x: Posición X de la entidad.
        :param y: Posición Y de la entidad.
        :param width: Ancho de la entidad.
        :param height: Alto de la entidad.
        """
        super().__init__()
        # Posición, velocidad y aceleración de la entidad.
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.respawn_x = x
        self.respawn_y = y
        self.speed = 0
        self.width = width
        self.height = height
        self.direction = 1  # 1: derecha, -1: izquierda
        # Se crea el rectángulo de colisión usando la posición (topleft) y dimensiones.
        self.rect = pygame.Rect(x, y, width, height)
        # Flag para saber si está saltando.
        self.jumping = False
        # Variables para animación.
        self.index = 0
        self.end_index = 0
        self.animation_timer = 0
        self.frame_rate = 10
        self.index = 0
        self.group = pygame.sprite.Group()
        self.animation_map = {
            "idle": self.other_animation,
            "walk": self.other_animation,         
         }
        self.current_action = "idle"
    #endregion

    #region other_animation
    def other_animation(self):  
        """
        Función que gestiona la animación del personaje, reinicia el índice si es necesario.

        :return: None
        """
        if self.index >= self.end_index:
           self.index = 0
    #endregion

    #region resolve_collisions
    def resolve_collisions(self, hit, vertical_margin=0):
        """
        Resuelve las colisiones de la entidad con otros objetos (plataformas u otros).

        :param hit: Objeto con el que la entidad ha colisionado.
        :param vertical_margin: Margen vertical para la resolución de colisiones.
        :return: None
        """
        # --- Resolución de colisiones horizontales ---
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
    #endregion

    #region render
    def render(self): 
        """
        Dibuja la animación de la entidad en función de su acción actual.

        :return: None
        """
        self.action_frames = self.frames[self.current_action]
        self.end_index = len(self.action_frames)
        if self.animation_timer > self.frame_rate: 
            if self.current_action in self.animation_map:
                action = self.animation_map[self.current_action]
                if action:
                    action()
            frame = self.action_frames[self.index]
            sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], self.width, self.height))
            if self.direction < 0:
                sprite_image = pygame.transform.flip(sprite_image, True, False)
            self.surf = sprite_image
            self.animation_timer = 0
            self.index += 1
    #endregion

    #region update_rect
    def update_rect(self):
        """
        Actualiza el rectángulo de colisión basado en la posición actual de la entidad.

        :return: None
        """
        self.rect.midbottom = self.pos
    #endregion

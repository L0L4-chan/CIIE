'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame

from game.objects.heart import Heart
from classes.player1 import Player1

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player2(Player1):

    #region __init__
    def __init__(self, x, y, lifes=3):
        """
        Constructor de Player2, inicializa atributos específicos.

        :param x: Posición x inicial.
        :param y: Posición y inicial.
        :param lifes: Número de vidas iniciales.
        :return: None
        """
        super().__init__(x, y, lifes)        
        self.bombing = False 
        self.frames.update({"bomb": [(self.width * 9 + (i * self.width), 0) for i in range(4)]})
        self.heart = Heart()
        self.bomb_counter = 300
        self.action_map.update({pygame.K_e: self.handle_bomb})
        self.animation_map.update({"bomb": self.animation_bomb})
        self.group.add(self.heart)
    #endregion

    #region handle_bomb
    def handle_bomb(self):
        """
        Maneja la acción de la bomba. Activa la animación si es posible.

        :return: None
        """
        if self.bomb_counter >= 300:
            self.current_action = "bomb"
            self.bombing = True
            self.index = 0
            self.bomb_counter = 0
    #endregion

    #region animation_bomb
    def animation_bomb(self):
        """
        Controla la animación de la bomba. 
        Cambia de estado al finalizar la animación.

        :return: None
        """
        if self.index >= self.end_index:
            self.bombing = False
            self.explode()
            self.current_action = "idle"
            self.index = 0
    #endregion

    #region move
    def move(self):
        """
        Controla el movimiento del personaje mientras no esté bombardeando.

        :return: None
        """
        if not self.bombing:
            super().move()
    #endregion

    #region explode
    def explode(self):
        """
        Lanza el corazón explosivo en la dirección del personaje.

        :return: None
        """
        if self.direction:
            heart_x = self.pos.x + (self.rect.width * self.direction)
        else:
            heart_x = self.pos.x - (self.rect.width)
        heart_y = self.rect.y + (self.height / 2)
        self.heart.set_Platform(self.platform)
        self.heart.active(x=int(heart_x), y=int(heart_y), direction=self.direction)
        self.bomb_counter = 0
    #endregion

    #region update
    def update(self):
        """
        Actualiza el estado del personaje, incluyendo el contador de bomba.

        :return: None
        """
        self.bomb_counter += 1
        super().update()
    #endregion

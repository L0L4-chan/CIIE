'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from classes.player import Player

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player1(Player):

    #region __init__
    def __init__(self, x, y, lifes=3):
        """
        Constructor de Player1.

        :param x: Posición x inicial.
        :param y: Posición y inicial.
        :param lifes: Número de vidas iniciales.
        :return: None
        """
        super().__init__(x, y)
        self.lifes = lifes
        self.shield = False 
        self.frames.update({"shield": [((self.width * 13) + (i * self.width), 0) for i in range(2)]})
        self.action_map.update({pygame.K_w: self.handle_shield})
        self.animation_map.update({"shield": self.animation_shield})
    #endregion

    #region handle_shield
    def handle_shield(self):
        """
        Maneja la activación del escudo.

        :return: None
        """
        if not self.shield:
            self.current_action = "shield"
            self.shield = True
            self.index = 0
    #endregion

    #region move
    def move(self):
        """
        Movimiento del personaje, desactiva el escudo si no está en animación de escudo.

        :return: None
        """
        super().move()
        if self.current_action != "shield":
            self.shield = False
    #endregion

    #region animation_shield
    def animation_shield(self):
        """
        Animación de escudo. Cuando finaliza, vuelve al estado idle.

        :return: None
        """
        if self.index >= self.end_index:
            self.shield = False
            self.current_action = "idle"
            self.index = 0
    #endregion

    #region to_die
    def to_die(self):
        """
        Controla la muerte del personaje. Si tiene escudo, no muere.

        :return: None
        """
        if not self.shield:
            super().to_die()
        self.shield = False
    #endregion

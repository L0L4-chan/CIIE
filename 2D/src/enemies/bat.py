'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, random, utils.globals as globals, utils.auxiliar as auxiliar
from classes.enemy import Enemy

vec = pygame.math.Vector2  # 2 for two dimensional

class Bat(Enemy):
    
    #region __init__
    def __init__(self, x, y):
        """
        Constructor de la clase Bat.

        :param x: Posición inicial en X.
        :param y: Posición inicial en Y.
        :return: None
        """
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{globals.config.get_artpath()}/bat/spritesheet.png"))
        super().__init__(x, y, (self.spritesheet.get_width() / 7), self.spritesheet.get_height(), False)
        self.vel = vec(globals.config.get_player_Acc() * 2, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = globals.config.get_player_Acc()
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(4)],
            "death": [((self.width * 4) + (i * self.width), 0) for i in range(3)]
        }
        self.lifes = 2
    #endregion

    #region move
    def move(self):
        """
        Gestiona el movimiento del murciélago.

        Cambia la dirección en X para perseguir al jugador, 
        y añade un pequeño movimiento aleatorio en Y para simular que vuela.
        
        :return: None
        """
        self.set_objective()
        distance_x = self.objective[0] - self.rect.x
        if distance_x < 0:
            self.direction = -1
        else:
            self.direction = 1

        if abs(distance_x) < self.screen_width / 2 or abs(distance_x) > self.screen_width / 40:
            self.vel.x = self.direction * self.speed

        # Añadir movimiento de subida y bajada aleatorio
        random_y_adjustment = random.randint(-5, 5)
        self.vel.y = random_y_adjustment * self.speed
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.update_rect()
    #endregion

    #region check_respawn
    def check_respawn(self):
        """
        Reinicia las vidas al hacer respawn.

        :return: None
        """
        super().check_respawn()
        self.lifes = 2
    #endregion

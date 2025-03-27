'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.objects.oneuse import OneUse

class Lifes(OneUse):
    #region __init__
    def __init__(self, x, y,path=("avatar/life.png")):
        """
        Inicializa la clase Lifes.

        Carga la imagen de la vida y configura el rect.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param path: Ruta de la imagen. Por defecto es ("avatar/life.png").
        """
        super().__init__(path)
        self.rect = pygame.Rect(x, y,self.image.get_width(), self.image.get_height())
        self.set_use()
    #endregion
               
    #region draw
    def draw(self, screen):
        """
        Dibuja la vida en la pantalla.

        Llama al método draw de la clase padre (OneUse) para dibujar la imagen en la posición definida por el rectángulo.

        :param screen: Superficie de la pantalla donde dibujar.
        :return: None
        """
        super().draw(screen = screen, position=self.rect.topleft)
    #endregion
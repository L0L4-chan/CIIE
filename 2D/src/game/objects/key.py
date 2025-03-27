'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame ,  utils.globals as globals, utils.auxiliar as auxiliar
from game.objects.prize import Prize

class Key(Prize):
    #region __init__
    def __init__(self,x,y):
        """
        Inicializa la clase Key.

        Carga la imagen de la llave y el sonido.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        """
        super().__init__(x,y, "prize/002.png")
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("OpenChest.wav")))
        self.sound.set_volume(0.5)
    #endregion
       
    #region update
    def update(self,  object = None):
        """
        Actualiza el estado de la llave.

        No realiza ninguna acción en este caso.

        :param object:  No utilizado, se mantiene por compatibilidad.
        :return: None
        """
        pass
    #endregion
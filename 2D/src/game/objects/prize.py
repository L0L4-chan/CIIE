'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame ,  utils.globals as globals, utils.auxiliar as auxiliar
from game.objects.oneuse import OneUse

class Prize(OneUse):
    #region __init__
    def __init__(self,x,y,path):
        """
        Inicializa la clase Prize.

        Carga la imagen del premio, define dimensiones, y establece el rectángulo y sonido.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param path: Ruta de la imagen del premio.
        """
        super().__init__(path)
        super().active(x,y, 1)
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.counter = 0
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("Prize.wav"))) #por si alguno no tiene sonido
        self.sound.set_volume(0.5)
    #endregion
        
    #region update
    def update(self,  object = None):
        """
        Actualiza el estado del premio.

        Incrementa un contador y desactiva el premio después de un cierto tiempo.

        :param object:  No utilizado, se mantiene por compatibilidad.
        :return: None
        """
        if self.inUse:
            self.counter += 1
            if self.counter >= 100:
                self.inUse = False
                self.rect.topleft = (0,0)
                self.counter = 0
    #endregion
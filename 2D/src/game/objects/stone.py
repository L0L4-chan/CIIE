'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.globals as globals
from game.objects.oneuse import OneUse


class Stone(OneUse):
    #region __init__
    def __init__(self):
        """
        Inicializa la clase Stone.

        Carga la imagen de la piedra, define dimensiones y velocidad inicial.
        """
        self.path = "stone/001.png"
        super().__init__(self.path) 
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.counter = 3
        self.speed_d = globals.config.get_stone_v()      
    #endregion
        
    #region active
    def active(self, x, y ,direction ):
        """
        Activa la Stone.

        Establece la posición, dirección, aplica ajustes visuales y activa el objeto para su uso.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param direction:  Dirección en la que se moverá la piedra (1 para derecha, -1 para izquierda).
        :return: None
        """
        self.speed = self.speed_d *  direction 
        self.image = pygame.transform.scale(self.spritesheet, (self.width, self.height))
        super().active(x,y, direction)
        self.set_use()
    #endregion

    #region hit
    def hit(self):
        """
        Gestiona el impacto de la Stone.

        Desactiva la piedra y la mueve fuera de la pantalla. Restablece el contador.
        """
        self.set_use()
        self.stand_by()
        self.counter = 3
    #endregion
     
    #region stand_by
    def stand_by(self): 
        """
        Mueve la Stone fuera de la pantalla (en la esquina superior izquierda) y detiene su movimiento.
        """
        self.rect.topleft = (0,0)  # La sacamos de la pantalla
        self.speed = 0
    #endregion

    #region update
    def update(self, object = None):
        """
        Actualiza el estado de la Stone en cada frame.

        Mueve la piedra horizontalmente, gestiona el contador y la desactiva si sale de la pantalla.

        :param object: No utilizado, se mantiene por compatibilidad con la señal.
        :return: None
        """
        if(self.inUse):
            self.rect.x += self.speed
            self.counter -= 1
            if not self.on_screen and self.counter <= 0:
                self.hit()
                self.counter = 3
    #endregion
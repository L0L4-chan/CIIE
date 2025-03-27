'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame,  utils.globals as globals, utils.auxiliar as auxiliar


class OneUse(pygame.sprite.Sprite):
    #region __init__
    def __init__(self, path):
        """
        Inicializa la clase OneUse.

        Carga la spritesheet, crea la imagen y define atributos iniciales.

        :param path: Ruta de la imagen a cargar.
        """
        super().__init__()
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/{path}"))
        self.image = self.spritesheet
        self.rect = self.image.get_rect()
        self.inUse = False
        self.on_screen = False
    #endregion
        
    #region active
    def active(self, x, y, direction):
        """
        Activa el objeto.

        Establece la posición y ajusta el rectángulo.

        :param x: Posición horizontal.
        :param y: Posición vertical.
        :param direction: Dirección (usualmente para indicar la dirección de movimiento, no se usa en esta función).
        :return: None
        """
        self.x_pos = x
        self.y_pos = y
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height())
    #endregion
        
    #region set_use
    def set_use(self):
        """
        Cambia el estado de uso del objeto.

        Invierte el valor de `inUse`.

        :return: None
        """
        self.inUse = not self.inUse
    #endregion
    
    #region get_inUse
    def get_inUse(self):
        """
        Obtiene el estado de uso del objeto.

        :return: True si el objeto está en uso, False en caso contrario.
        :rtype: bool
        """
        return self.inUse
    #endregion
        
    #region draw
    def draw(self, screen, position):
        """
        Dibuja el objeto en la pantalla.

        Dibuja la imagen en la posición especificada si el objeto está en uso.

        :param screen: Superficie de la pantalla donde dibujar.
        :param position: Posición donde dibujar la imagen.
        :return: None
        """
        if self.inUse:
            screen.blit(self.image ,position)
    #endregion
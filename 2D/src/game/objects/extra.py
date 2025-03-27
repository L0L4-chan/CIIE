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

class Extra(Prize):
    def __init__(self,x,y):
       super().__init__(x,y, "prize/003.png")
       self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("Life.wav")))
       self.sound.set_volume(0.5)
       self.to_pick= True
    
    #region set_use
    def set_use(self):
        """
        Cambia el estado de uso del premio y el estado de "ser recogido".

        Invierte el valor de `inUse` y `to_pick`.

        :return: None
        """
        self.inUse = not self.inUse  
        self.to_pick = not self.to_pick
    #endregion
    
    #region being_pick
    def being_pick(self):
        """
        Establece el premio como "no recogible".

        Establece el atributo `to_pick` a `False`.

        :return: None
        """
        self.to_pick = False
    #endregion
        
    #region get_can_pick
    def get_can_pick(self):
        """
        Obtiene el estado de "ser recogido" del premio.

        :return: True si el premio se puede recoger, False en caso contrario.
        :rtype: bool
        """
        return self.to_pick
    #endregion